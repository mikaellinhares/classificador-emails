import os
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from utils.file_loader import extract_text
from utils.process_text import process_text

from ai_providers.base import AIClient
from ai_providers.deepseek_provider import DeepSeekAIClient


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "txt"}

PROVIDER_MAP = {
    "deepseek": DeepSeekAIClient,
}


def get_ai_client() -> AIClient:
    provider_name = os.environ.get("AI_PROVIDER", "").lower()
    ClientCls = PROVIDER_MAP.get(provider_name)
    if ClientCls is None:
        raise ValueError(f"Provider não suportado: {provider_name}")
    return ClientCls()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")


# * Rotas
@app.get("/")
def upload_form():
    return render_template("upload.html")


@app.post("/classify-and-suggest")
def classify_and_suggest():
    text = request.form.get("text")
    file = request.files.get("file")

    if not text and not file:
        flash("Nenhum arquivo ou texto recebido.", "error")
        return redirect(url_for("upload_form"))

    if file and not allowed_file(file.filename):
        flash("Formato não suportado. Envie .pdf ou .txt.", "error")
        return redirect(url_for("upload_form"))

    file_text = ""
    if file:
        filename = secure_filename(file.filename)
        file_path = UPLOAD_DIR / filename
        file.save(file_path)
        file_text = extract_text(file_path).strip()
        os.remove(file_path)

    email_text = text + "\n" + file_text
    
    processed_email_text = process_text(email_text)

    client = get_ai_client()

    classifications = {
        "produtivo": "Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).",
        "improdutivo": "Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos)."
    }

    company_context = {
        "areaAtuacaoEmpresa": "Instituição Financeira",
    }

    result = client.classify_and_reply(
        email_text=processed_email_text,
        classifications=classifications,
        company_context=company_context,
    )

    return render_template(
        "result.html",
        email_preview=email_text[:3000],
        classification=result.get("classification", "desconhecido"),
        reply_suggestion=result.get("reply_suggestion", "(sem sugestão)")
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
