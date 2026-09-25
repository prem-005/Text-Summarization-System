def evaluate_summary(original, summary):
    original_words = original.split()
    summary_words = summary.split()

    compression = 0
    if original_words:
        compression = round((1 - len(summary_words) / len(original_words)) * 100, 2)

    try:
        from rouge_score import rouge_scorer
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        scores = scorer.score(original, summary)
        return {
            "compression": compression,
            "rouge1": round(scores["rouge1"].fmeasure, 4),
            "rouge2": round(scores["rouge2"].fmeasure, 4),
            "rougeL": round(scores["rougeL"].fmeasure, 4),
        }
    except Exception:
        return {
            "compression": compression,
            "rouge1": None,
            "rouge2": None,
            "rougeL": None,
        }
