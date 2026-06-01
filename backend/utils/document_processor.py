import io


def extract_text(content: bytes, filename: str) -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            pass

    if name.endswith(".json"):
        import json
        try:
            data = json.loads(content)
            return json.dumps(data, indent=2)
        except Exception:
            pass

    return content.decode("utf-8", errors="ignore")
