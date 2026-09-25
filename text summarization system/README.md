# SmartSummarizer — Text Summarization System

A final-year-project-ready Flask application for text summarization.

## Features
- Extractive summarization using TF-IDF
- Abstractive summarization using BART (`facebook/bart-large-cnn`)
- TXT, PDF and DOCX upload
- Summary percentage control
- ROUGE-1, ROUGE-2 and ROUGE-L evaluation
- Compression ratio
- Download generated summary
- Responsive professional UI

## 1. Create virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Download NLTK tokenizer

Run once:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

## 4. Run

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

## Abstractive mode

The first BART request downloads the model from Hugging Face and may require several GB of disk space and a good internet connection. Extractive TF-IDF mode is lightweight and works without loading BART.

## Project architecture

User -> Flask UI -> File/Text Extraction -> Preprocessing -> Summarization Model -> Evaluation -> Result/Download

## Suggested academic title

"An Intelligent Web-Based Text Summarization System Using Extractive and Abstractive Natural Language Processing"

## Future enhancements
- User login and database history
- Multi-language summarization
- Keyword extraction
- Text-to-speech
- YouTube/article URL summarization
- Transformer fine-tuning on CNN/DailyMail or custom dataset
