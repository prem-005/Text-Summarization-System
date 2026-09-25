import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize

class TextSummarizer:
    def _sentences(self, text):
        text = re.sub(r"\s+", " ", text).strip()
        try:
            return sent_tokenize(text)
        except LookupError:
            return re.split(r"(?<=[.!?])\s+", text)

    def extractive_summary(self, text, ratio=30):
        sentences = self._sentences(text)
        if len(sentences) <= 2:
            return text.strip()

        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(sentences)
        scores = np.asarray(matrix.sum(axis=1)).ravel()

        count = max(1, round(len(sentences) * ratio / 100))
        count = min(count, len(sentences))
        selected = np.argsort(scores)[-count:]
        selected = sorted(selected)

        return " ".join(sentences[i] for i in selected)

    def abstractive_summary(self, text):
        # Lazy import: the application can still run in extractive mode
        # without installing/loading the Transformer model.
        from transformers import pipeline

        if len(text) > 12000:
            text = text[:12000]

        pipe = pipeline("summarization", model="facebook/bart-large-cnn")
        chunks = self._chunk_text(text, 3500)
        summaries = []

        for chunk in chunks:
            result = pipe(
                chunk,
                max_length=180,
                min_length=40,
                do_sample=False
            )
            summaries.append(result[0]["summary_text"])

        return " ".join(summaries)

    def _chunk_text(self, text, max_chars):
        sentences = self._sentences(text)
        chunks, current = [], ""

        for sentence in sentences:
            if len(current) + len(sentence) + 1 > max_chars and current:
                chunks.append(current)
                current = sentence
            else:
                current += (" " if current else "") + sentence

        if current:
            chunks.append(current)

        return chunks
