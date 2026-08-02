"""
main.py

Ponto de entrada do projeto Alura Agent.

Fluxo desta etapa:
1. Pede ao usuário um texto de referência (que pode ser parte ou o
   conteúdo inteiro de um dos PDFs).
2. Varre a pasta "pdf/" e seleciona apenas os PDFs cujo conteúdo
   contém esse texto.
3. Processa (extrai texto + divide em chunks) somente os PDFs
   selecionados.

Nas próximas etapas do desafio, este arquivo evoluirá para:
- gerar embeddings dos chunks
- indexar os chunks para busca
- receber perguntas do usuário e responder usando o conteúdo do PDF
"""

from pathlib import Path

from document_loader import selecionar_pdfs_por_texto, processar_pdf

# Pasta onde ficam os PDFs (C:\Repo2026\Challenge\pdf)
PASTA_PDFS = Path(__file__).resolve().parent.parent / "pdf"


def main():
    texto_busca = input(
        "Digite um trecho (ou o conteúdo inteiro) de um dos PDFs para selecioná-lo: "
    ).strip()

    if not texto_busca:
        print("Nenhum texto informado. Encerrando.")
        return

    print(f"\nBuscando PDFs em '{PASTA_PDFS}' que contenham o texto informado...\n")

    pdfs_selecionados = selecionar_pdfs_por_texto(str(PASTA_PDFS), texto_busca)

    if not pdfs_selecionados:
        print("Nenhum PDF encontrado com esse texto.")
        return

    print(f"{len(pdfs_selecionados)} PDF(s) selecionado(s):")
    for pdf in pdfs_selecionados:
        print(f" - {pdf.name}")

    for pdf in pdfs_selecionados:
        print(f"\n=== Processando: {pdf.name} ===")
        chunks = processar_pdf(str(pdf))
        print(f"Total de chunks gerados: {len(chunks)}")

        print("Prévia dos primeiros chunks:")
        for chunk in chunks[:3]:
            print(f"\n--- Chunk {chunk.id} (página {chunk.pagina}) ---")
            print(chunk.texto[:300])


if __name__ == "__main__":
    main()