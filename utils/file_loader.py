from pathlib import Path
from typing import Union
from PyPDF2 import PdfReader

PathLike = Union[str, Path]


def extract_text(path: PathLike) -> str:
    """Realiza a leitura de um arquivo .txt ou .pdf e retorna seu conteúdo."""

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    ext = p.suffix.lower()
    if ext == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")

    if ext == ".pdf":
        reader = PdfReader(str(p))
        parts = []
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(parts)

    raise ValueError(f"Extensão não suportada: {ext}")
