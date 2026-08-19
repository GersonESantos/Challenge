from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from document_loader import Chunk, processar_pdf, selecionar_pdfs_por_texto
from gemini_analyzer import DEFAULT_MODEL, analisar_notas_fiscais

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_PDFS = BASE_DIR / "pdf"

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))


def resumir_chunk(chunk: Chunk, limite: int = 300) -> str:
    texto = chunk.texto.strip()
    if len(texto) <= limite:
        return texto
    return f"{texto[:limite].rstrip()}..."


def listar_pdfs() -> list[str]:
    PASTA_PDFS.mkdir(parents=True, exist_ok=True)
    return sorted(pasta_pdf.name for pasta_pdf in PASTA_PDFS.glob("*.pdf"))


@app.get("/")
def index():
    pdfs = listar_pdfs()
    return render_template(
        "index.html",
        pdfs=pdfs,
        selecionados=None,
        chunks=None,
        erro=None,
        analise_resultado=None,
        modelo_padrao=DEFAULT_MODEL,
    )


@app.post("/processar")
def processar():
    pdfs = listar_pdfs()
    texto_busca = request.form.get("texto_busca", "").strip()
    arquivo_existente = request.form.get("arquivo_existente", "").strip()
    upload = request.files.get("pdf_upload")

    arquivos_selecionados: list[Path] = []
    erro = None

    if upload and upload.filename:
        destino = PASTA_PDFS / Path(upload.filename).name
        destino.parent.mkdir(parents=True, exist_ok=True)
        upload.save(destino)
        arquivos_selecionados = [destino]
        pdfs = listar_pdfs()
    elif arquivo_existente:
        arquivo = PASTA_PDFS / arquivo_existente
        if arquivo.exists():
            arquivos_selecionados = [arquivo]
        else:
            erro = "O PDF selecionado não foi encontrado na pasta pdf/."
    elif texto_busca:
        arquivos_selecionados = selecionar_pdfs_por_texto(PASTA_PDFS, texto_busca)
        if not arquivos_selecionados:
            erro = "Nenhum PDF encontrado com esse texto."
    else:
        erro = "Envie um PDF, escolha um arquivo existente ou informe um texto de busca."

    chunks_por_arquivo: list[dict[str, object]] = []
    for pdf_path in arquivos_selecionados:
        chunks = processar_pdf(pdf_path)
        chunks_por_arquivo.append(
            {
                "nome": pdf_path.name,
                "total": len(chunks),
                "chunks": [
                    {
                        "id": chunk.id,
                        "pagina": chunk.pagina,
                        "texto": resumir_chunk(chunk),
                    }
                    for chunk in chunks[:5]
                ],
            }
        )

    return render_template(
        "index.html",
        pdfs=pdfs,
        selecionados=chunks_por_arquivo,
        chunks=chunks_por_arquivo,
        erro=erro,
        analise_resultado=None,
        modelo_padrao=DEFAULT_MODEL,
    )


@app.post("/analisar")
def analisar():
    pdfs = listar_pdfs()

    if request.is_json:
        dados = request.get_json(silent=True) or {}
        pergunta = dados.get("pergunta", "").strip()
        arquivo_selecionado = dados.get("arquivo", "").strip()
        modelo = dados.get("modelo", "").strip() or DEFAULT_MODEL
    else:
        pergunta = request.form.get("pergunta", "").strip()
        arquivo_selecionado = request.form.get("arquivo_analise", "").strip()
        modelo = request.form.get("modelo", "").strip() or DEFAULT_MODEL

    arquivos_alvo = [arquivo_selecionado] if arquivo_selecionado else None

    resultado = analisar_notas_fiscais(
        pergunta=pergunta,
        pasta_pdfs=PASTA_PDFS,
        arquivos_selecionados=arquivos_alvo,
        modelo=modelo,
    )

    if request.is_json or request.headers.get("Accept") == "application/json":
        return jsonify(resultado), (200 if resultado.get("sucesso") else 400)

    return render_template(
        "index.html",
        pdfs=pdfs,
        selecionados=None,
        chunks=None,
        erro=resultado.get("erro"),
        analise_resultado=resultado,
        modelo_padrao=DEFAULT_MODEL,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)