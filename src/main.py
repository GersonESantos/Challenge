from __future__ import annotations

from pathlib import Path

from document_loader import load_pdf_text, split_text


BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "pdf" / "documento.pdf"


def main() -> None:
    text = load_pdf_text(PDF_PATH)
    chunks = split_text(text)

    print(f"PDF carregado: {PDF_PATH.name}")
    print(f"Total de chunks: {len(chunks)}")

    if not chunks:
        print("Nenhum texto foi extraído do PDF.")
        return

    print("\nPrévia do primeiro chunk:\n")
    print(chunks[0][:500])


if __name__ == "__main__":
    main()