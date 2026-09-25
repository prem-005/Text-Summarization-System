from flask import Flask, render_template, request, send_file, flash
from werkzeug.utils import secure_filename
from models.summarizer import TextSummarizer
from utils.extract_text import extract_text_from_file
from utils.evaluation import evaluate_summary
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "text-summarization-project-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
SUMMARY_DIR = os.path.join(BASE_DIR, "summaries")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
summarizer = TextSummarizer()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    original_text = ""
    method = "extractive"
    ratio = 30

    if request.method == "POST":
        original_text = request.form.get("text", "").strip()
        method = request.form.get("method", "extractive")
        try:
            ratio = max(10, min(80, int(request.form.get("ratio", 30))))
        except ValueError:
            ratio = 30

        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            if not allowed_file(uploaded.filename):
                flash("Supported files: TXT, PDF, DOCX")
                return render_template("index.html", result=None)
            filename = secure_filename(uploaded.filename)
            path = os.path.join(UPLOAD_DIR, filename)
            uploaded.save(path)
            try:
                original_text = extract_text_from_file(path)
            except Exception as exc:
                flash(f"Could not read the file: {exc}")
                return render_template("index.html", result=None)

        if not original_text:
            flash("Enter text or upload a document.")
            return render_template("index.html", result=None)

        try:
            if method == "abstractive":
                summary = summarizer.abstractive_summary(original_text)
                used_method = "Abstractive (BART)"
            else:
                summary = summarizer.extractive_summary(original_text, ratio)
                used_method = "Extractive (TF-IDF)"
        except Exception as exc:
            flash(f"Summarization failed: {exc}")
            return render_template("index.html", result=None)

        metrics = evaluate_summary(original_text, summary)
        result = {
            "summary": summary,
            "method": used_method,
            "metrics": metrics,
            "original_words": len(original_text.split()),
            "summary_words": len(summary.split())
        }

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(SUMMARY_DIR, f"summary_{stamp}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary)

        result["download"] = os.path.basename(out_path)

    return render_template("index.html", result=result, original_text=original_text,
                           method=method, ratio=ratio)

@app.route("/download/<filename>")
def download(filename):
    safe = secure_filename(filename)
    path = os.path.join(SUMMARY_DIR, safe)
    if not os.path.isfile(path):
        flash("Summary file not found.")
        return render_template("index.html")
    return send_file(path, as_attachment=True, download_name=safe)

if __name__ == "__main__":
    app.run(debug=True)
