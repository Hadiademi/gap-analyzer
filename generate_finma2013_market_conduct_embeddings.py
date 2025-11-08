#!/usr/bin/env python3
"""
Utility script to generate embeddings for the FINMA Circular 2013/8
"Market conduct rules" document.

This script parses the DOCX source, extracts structured articles together
with their margin numbers, generates embeddings with the existing
`embed_articles` helper, and saves the enriched dataset as an Excel file.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

import pandas as pd
from docx import Document  # python-docx

from modules.embed_open_source import embed_articles


DOC_PATH = Path("Data/Document/Circular 2013 8 Market conduct rules.docx")
RAW_OUTPUT_PATH = Path("Data/Finma_EN/splitted/finma2013_market_conduct_raw.xlsx")
EMB_OUTPUT_PATH = Path("Data/Finma_EN/splitted/finma2013_market_conduct_embeddings.xlsx")


ROMAN_TOKENS = set("IVXLCDM")
LETTER_SECTIONS = {chr(code) for code in range(ord("A"), ord("Z") + 1)}


def clean_text(text: str) -> str:
    """
    Normalise whitespace and stray characters.
    """
    if text is None:
        return ""
    text = (
        text.replace("\xa0", " ")
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .strip()
    )
    # Collapse multiple whitespaces
    return " ".join(text.split())


def looks_like_roman(token: str) -> bool:
    token = token.upper()
    return bool(token) and all(ch in ROMAN_TOKENS for ch in token)


def looks_like_letter_section(token: str) -> bool:
    token = token.upper()
    return len(token) == 1 and token in LETTER_SECTIONS


def normalise_margin(text: str) -> str:
    text = clean_text(text).replace(" ", "")
    # Preserve trailing * indicators while normalising dashes
    text = text.replace("--", "-")
    return text


def is_margin(text: str) -> bool:
    if not text:
        return False
    text = normalise_margin(text)
    # Accept values such as 1, 1-2, 3*, 65*-67*, etc.
    return bool(re.match(r"^\d+\*?(?:[-–]\d+\*?)?$", text))


def extract_entries(doc_path: Path) -> pd.DataFrame:
    """
    Parse the DOCX document and build a DataFrame with Title/SubTitle/Margin/Text.
    """
    document = Document(doc_path)

    entries: List[dict] = []
    current_title: Optional[str] = "Circular 2013/8 Market conduct rules"
    current_subtitle: Optional[str] = ""

    for table_idx, table in enumerate(document.tables):
        # Skip the addressee grid (table 0) and the index overview (table 1).
        if table_idx <= 1:
            continue

        for row in table.rows:
            cell_texts = [clean_text(cell.text) for cell in row.cells]
            if not any(cell_texts):
                continue

            margin_value: Optional[str] = None
            content_cells: List[str] = []

            # Extract margin number (usually the last non-empty cell containing digits)
            for cell_text in reversed(cell_texts):
                if margin_value is None and is_margin(cell_text):
                    margin_value = normalise_margin(cell_text)
                    continue
                content_cells.insert(0, cell_text)

            # Remove helper headers
            content_cells = [value for value in content_cells if value not in {"", "Margin no.", "Margin no"}]
            if not content_cells and margin_value:
                continue

            heading_candidate = content_cells[0] if content_cells else ""
            heading_token = heading_candidate.split()[0].rstrip(".") if heading_candidate else ""

            # Update heading context when no margin is present
            if margin_value is None and heading_candidate:
                if looks_like_roman(heading_token):
                    current_title = heading_candidate
                    current_subtitle = ""
                    continue
                if looks_like_letter_section(heading_token):
                    current_subtitle = heading_candidate
                    continue
                # Fallback: treat as additional text without margin
                # (rare case where content is missing a margin number)

            if margin_value:
                text_content = " ".join(content_cells).strip()
                if not text_content:
                    continue

                entries.append(
                    {
                        "Title": current_title or "",
                        "SubTitle": current_subtitle or "",
                        "Margin": margin_value,
                        "Text": text_content,
                    }
                )

    df = pd.DataFrame(entries)
    if df.empty:
        raise ValueError("No entries extracted from the document.")

    # Ensure required columns exist for embed_articles helper
    df["Sub_Subtitle"] = ""
    return df


def main() -> None:
    if not DOC_PATH.exists():
        raise FileNotFoundError(f"Document not found: {DOC_PATH}")

    print("Parsing Circular 2013/8 Market conduct rules...")
    df_raw = extract_entries(DOC_PATH)
    print(f"   Extracted {len(df_raw)} rows")

    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    EMB_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_raw.to_excel(RAW_OUTPUT_PATH, index=False)
    print(f"   Saved raw structured data to {RAW_OUTPUT_PATH}")

    print("Generating embeddings with all-MiniLM-L6-v2...")
    embeddings_df = embed_articles(df_raw)

    combined = pd.concat(
        [df_raw.drop(columns=["Sub_Subtitle"]), embeddings_df],
        axis=1,
    )
    combined.to_excel(EMB_OUTPUT_PATH, index=False)
    print(f"   Saved embeddings to {EMB_OUTPUT_PATH}")

    print("\nDone! New regulation file is ready.")


if __name__ == "__main__":
    main()

