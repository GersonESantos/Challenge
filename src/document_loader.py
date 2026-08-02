from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Chunk:
    id: int
    pagina: int
    texto: str


def load_pdf_text(pdf_path: str | Path) -> str:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    reader = PdfReader(str(path))
    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        cleaned = text.strip()
        if cleaned:
            pages.append(cleaned)

    return "\n\n".join(pages)


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    normalized = " ".join(text.split())
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunks.append(normalized[start:end])
        if end == len(normalized):
            break
        start = end - overlap

    return chunks


def selecionar_pdfs_por_texto(pasta_pdfs: str | Path, texto_busca: str) -> list[Path]:
    pasta = Path(pasta_pdfs)
    if not pasta.exists():
        raise FileNotFoundError(f"Folder not found: {pasta}")

    texto_normalizado = texto_busca.strip().lower()
    if not texto_normalizado:
        return []

    selecionados: list[Path] = []
    for pdf_path in sorted(pasta.glob("*.pdf")):
        try:
            conteudo = load_pdf_text(pdf_path)
        except Exception:
            continue

        if texto_normalizado in conteudo.lower():
            selecionados.append(pdf_path)

    return selecionados


def processar_pdf(pdf_path: str | Path, chunk_size: int = 1000, overlap: int = 150) -> list[Chunk]:
    caminho = Path(pdf_path)
    reader = PdfReader(str(caminho))
    chunks: list[Chunk] = []
    chunk_id = 1

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        if not page_text:
            continue

        page_chunks = split_text(page_text, chunk_size=chunk_size, overlap=overlap)
        for chunk_text in page_chunks:
            chunks.append(Chunk(id=chunk_id, pagina=page_number, texto=chunk_text))
            chunk_id += 1

    return chunks
