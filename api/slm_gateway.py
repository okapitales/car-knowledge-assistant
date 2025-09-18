import re
import spacy
from transformers import pipeline as hf_pipeline

# ---- Load spaCy (English small model) ----
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# ---- Small classifier (DistilBERT) ----
classifier = hf_pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def slm_gateway(user_input: str) -> dict:
    text = re.sub(r"[^a-zA-Z0-9\s?.!]", "", user_input)
    text = re.sub(r"\s+", " ", text).strip()

    # Check relevance
    result = classifier(text, candidate_labels=["car query", "irrelevant", "other"])
    top_label = result["labels"][0]

    if top_label == "irrelevant":
        return {"action": "block", "cleaned": text, "reason": "Irrelevant query"}

    # spaCy simplify
    doc = nlp(text)
    simplified = " ".join([token.lemma_ for token in doc if not token.is_stop])

    return {"action": "pass", "cleaned": simplified, "reason": "Clean + simplified"}