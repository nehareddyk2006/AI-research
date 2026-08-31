
import pymupdf
import re


# Maximum amount of text we need for Gemini.
MAX_TEXT_CHARS = 15000

# Safety limit so extremely large PDFs don't get processed forever.
MAX_PAGES = 30


def extract_pdf(file):

    pdf = pymupdf.open(
        stream=file.read(),
        filetype="pdf"
    )

    text_parts = []

    pages_to_process = min(len(pdf), MAX_PAGES)

    for page_index in range(pages_to_process):

        page = pdf[page_index]

        page_text = page.get_text()

        if page_text:
            text_parts.append(page_text)

        # Stop extracting once we have enough text.
        current_length = sum(
            len(part) for part in text_parts
        )

        if current_length >= MAX_TEXT_CHARS:
            break

    text = "\n".join(text_parts)

    # Keep the text bounded.
    text = text[:MAX_TEXT_CHARS]

    pages = len(pdf)

    words = len(text.split())

    reading_time = max(1, words // 200)

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    title = "Untitled Paper"

    if lines:
        title = lines[0]

    authors = "Not Available"

    if len(lines) > 1:
        authors = lines[1]

    journal = "Unknown"

    if len(lines) > 2:
        journal = lines[2]

    year = "Unknown"

    year_match = re.search(
        r"(20\d{2})",
        text
    )

    if year_match:
        year = year_match.group(1)

    abstract = "Abstract not detected."

    abstract_match = re.search(
        r"ABSTRACT(.*?)(KEYWORDS|INTRODUCTION)",
        text,
        re.DOTALL | re.IGNORECASE,
    )

    if abstract_match:
        abstract = abstract_match.group(1).strip()

    keywords = []

    keyword_match = re.search(
        r"Keywords\s*:?\s*(.*)",
        text,
        re.IGNORECASE,
    )

    if keyword_match:

        keywords = [
            k.strip()
            for k in keyword_match.group(1).split(",")
            if k.strip()
        ]

    pdf.close()

    return {

        "title": title,

        "authors": authors,

        "journal": journal,

        "year": year,

        "abstract": abstract,

        "keywords": keywords,

        "pages": pages,

        "word_count": words,

        "reading_time": reading_time,

        "text": text

    }

