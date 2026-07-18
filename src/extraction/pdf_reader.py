import fitz
import re


def extract_pdf(file):

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

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