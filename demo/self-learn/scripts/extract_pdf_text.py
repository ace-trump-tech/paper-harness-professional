#!/usr/bin/env python3
"""Extract a bounded, page-marked local text copy for each downloaded PDF."""

from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "papers" / "raw"
TEXT_DIR = ROOT / "papers" / "text"


def extract(pdf_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n===== PAGE {number} =====\n\n{text.strip()}\n")

    output = TEXT_DIR / f"{pdf_path.stem}.txt"
    output.write_text("".join(pages), encoding="utf-8")
    print(f"{pdf_path.name}: {len(reader.pages)} pages -> {output.name}")


def main() -> None:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    for pdf_path in sorted(RAW_DIR.glob("*.pdf")):
        try:
            extract(pdf_path)
        except Exception as exc:  # Keep the raw source and surface failures explicitly.
            print(f"{pdf_path.name}: extraction failed: {exc}")


if __name__ == "__main__":
    main()
