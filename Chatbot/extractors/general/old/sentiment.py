#Chatbot/extractors/general/sentiment.py
"""
Sentiment Detection & Clause Splitting
--------------------------------------
Handles:
- Zero-shot classification via LLM
- Negation-aware sentiment fallback
- Clause splitting (e.g. "I like pink but not red")
"""

import re
import spacy
from typing import List, Dict, Tuple
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

# ─────────────────────────────────────────────
# Zero-shot sentiment classifier setup
# ─────────────────────────────────────────────
_SENTIMENT_MODEL_NAME = "facebook/bart-large-mnli"
_CANDIDATE_LABELS = ["I like this", "I dislike this", "I'm unsure or neutral"]
_LABEL_MAP = {
    "I like this": "positive",
    "I dislike this": "negative",
    "I'm unsure or neutral": "neutral"
}
_sentiment_pipeline = pipeline("zero-shot-classification", model=_SENTIMENT_MODEL_NAME)

# ─────────────────────────────────────────────
# Main Entry: Classify all segments
# ─────────────────────────────────────────────
def classify_segments_by_sentiment_no_neutral(has_splitter: bool, segments: List[str]) -> Dict[str, List[str]]:
    """
    Runs classification on each segment. If neutral is returned,
    it uses negation to infer whether it leans positive or negative.
    """
    classification = {"positive": [], "negative": []}

    for seg in segments:
        try:
            sentiment = detect_sentiment(seg)
            mapped = map_sentiment(sentiment, seg)
            classification[mapped].append(seg)
        except Exception as e:
            print(f"[❌ SENTIMENT ERROR] → {e}")

    return classification


def detect_sentiment(text: str) -> str:
    """
    Classifies input as positive, negative, or neutral.
    Uses zero-shot pipeline.
    """
    try:
        result = _sentiment_pipeline(text, _CANDIDATE_LABELS)
        label = result["labels"][0]
        return _LABEL_MAP.get(label, "neutral")
    except Exception as e:
        print(f"[❌ Sentiment pipeline failed] → {e}")
        return "neutral"


def map_sentiment(predicted: str, text: str) -> str:
    """
    Applies fallback logic for neutral labels using negation detection.
    """
    if predicted == "neutral":
        if is_negated(text) or is_softly_negated(text):
            print(f"[🧠 FALLBACK NEGATION DETECTED] '{text}' → forcing 'negative'")
            return "negative"
        return "positive"
    return predicted

# ─────────────────────────────────────────────
# Clause Segmentation
# ─────────────────────────────────────────────
def contains_sentiment_splitter_with_segments(text: str) -> Tuple[bool, List[str]]:
    """
    Detects whether the sentence contains a clause-level sentiment split
    and returns segmented parts. Uses dependency parsing and punctuation fallback.
    """
    doc = nlp(text)

    if should_skip_split_due_to_or_negation(doc):
        return False, [text.strip()]

    index = find_splitter_index(doc)
    if index is not None:
        return True, split_text_on_index(doc, index)

    return fallback_split_on_punctuation(text)


def should_skip_split_due_to_or_negation(doc) -> bool:
    has_neg = any(tok.dep_ == "neg" for tok in doc)
    has_or = any(tok.text.lower() == "or" for tok in doc)
    has_punct = any(tok.text in {".", ",", ";"} for tok in doc)
    return has_neg and has_or and not has_punct


def find_splitter_index(doc) -> int | None:
    for i, tok in enumerate(doc):
        if tok.dep_ == "cc" and tok.text.lower() in {"and", "or"}:
            if is_tone_conjunction(doc, i):
                continue
        if tok.dep_ in {"cc", "mark", "discourse"}:
            return i
        if tok.dep_ == "advmod":
            if i == 0:
                return i
            prev = doc[i - 1]
            next_ = doc[i + 1] if i + 1 < len(doc) else None
            if prev.is_punct and tok.is_alpha and (not next_ or next_.dep_ not in {"amod", "acomp", "dobj", "advmod"}):
                return i
    return None


def is_tone_conjunction(doc, index: int) -> bool:
    prev = doc[index - 1] if index > 0 else None
    next_ = doc[index + 1] if index + 1 < len(doc) else None
    return prev and next_ and prev.pos_ in {"ADJ", "NOUN"} and next_.pos_ in {"ADJ", "NOUN"}


def split_text_on_index(doc, i: int) -> List[str]:
    if i == 0 or i == len(doc) - 1:
        remaining = " ".join(tok.text for tok in doc[i + 1:]).strip()
        return [seg.strip() for seg in re.split(r"[;,]", remaining) if seg.strip()]
    return [doc[:i].text.strip(), doc[i + 1:].text.strip()]


def fallback_split_on_punctuation(text: str) -> Tuple[bool, List[str]]:
    segments = [s.strip() for s in re.split(r"[.;,]", text) if s.strip()]
    return (True, segments) if len(segments) >= 2 else (False, [text.strip()])

# ─────────────────────────────────────────────
# Negation Detection
# ─────────────────────────────────────────────
def is_negated(text: str) -> bool:
    """
    Detects hard negation patterns (e.g., 'not pink', 'no red').
    """
    doc = nlp(text)
    if any(tok.dep_ == "neg" for tok in doc):
        return True

    for i in range(len(doc) - 1):
        t1, t2 = doc[i], doc[i + 1]
        if (
            t1.text.lower() == "no"
            and t1.dep_ in {"det", "neg"}
            and t2.pos_ in {"ADJ", "NOUN"}
            and t2.dep_ in {"amod", "compound", "conj", "ROOT"}
        ):
            return True
    return False


def is_softly_negated(text: str) -> bool:
    """
    Detects soft patterns like 'not too shiny' or 'nothing too bold'.
    """
    doc = nlp(text.lower())
    for i in range(len(doc) - 2):
        t1, t2, t3 = doc[i], doc[i + 1], doc[i + 2]
        if t1.text in {"nothing", "not", "no"} and t2.text == "too" and t3.pos_ == "ADJ":
            return True
    return False
