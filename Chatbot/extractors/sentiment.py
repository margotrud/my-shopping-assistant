# Chatbot/extractors/sentiment_detector.py
import re
from transformers import pipeline

# === Zero-shot configuration ===
_SENTIMENT_MODEL_NAME = "facebook/bart-large-mnli"
_CANDIDATE_LABELS = ["I like this", "I dislike this", "I'm unsure or neutral"]

_LABEL_MAP = {
    "I like this": "positive",
    "I dislike this": "negative",
    "I'm unsure or neutral": "neutral"
}

# === Initialize pipeline ===
_sentiment_pipeline = pipeline("zero-shot-classification", model=_SENTIMENT_MODEL_NAME)

def detect_sentiment(text: str) -> str:
    """
    Runs zero-shot sentiment classification on user input.

    Args:
        text (str): User message

    Returns:
        str: One of {"positive", "negative", "neutral"}
    """

    try:
        result = _sentiment_pipeline(text, _CANDIDATE_LABELS)
        top_label = result["labels"][0]
        mapped = _LABEL_MAP.get(top_label, "neutral")

        return mapped

    except Exception as e:
        print(f"[❌ ERROR] Sentiment pipeline failed: {e}")
        return "neutral"



############################## II. Sentiment splitter: Test checked and rewritten
import spacy

nlp = spacy.load("en_core_web_sm")

def contains_sentiment_splitter_with_segments(text: str):
    doc = nlp(text)
    splitter_index = None

    # Step 1: Detect sentiment splitter
    for i, token in enumerate(doc):
        if token.dep_ in {"cc", "mark", "discourse"}:
            splitter_index = i
            break

        if token.dep_ == "advmod":
            # Look ahead: if next token is a tone/modifier, treat as a compound, not a split
            next_token = doc[i + 1] if i + 1 < len(doc) else None
            if next_token and next_token.dep_ in {"amod", "acomp", "dobj", "advmod"}:
                continue

            prev_token = doc[i - 1] if i > 0 else None
            prev_punct = prev_token.is_punct if prev_token else False

            if i == 0 or (prev_token and prev_punct and token.is_alpha):
                splitter_index = i
                break

    # Step 2: Handle segmentation if splitter found
    if splitter_index is not None:

        # Case A: Splitter at beginning or end
        if splitter_index == 0 or splitter_index == len(doc) - 1:
            remaining_tokens = list(doc[splitter_index + 1:])

            # Skip low-value openers like 'though', 'even', etc.
            cleaned_tokens = []
            skip = True
            for tok in remaining_tokens:
                if skip and tok.dep_ in {"mark", "advmod", "discourse"} and tok.pos_ in {"SCONJ", "ADV"}:
                        continue
                skip = False
                cleaned_tokens.append(tok)

            remaining_text = " ".join(tok.text for tok in cleaned_tokens).strip()
            segments = [seg.strip() for seg in re.split(r"[;,]", remaining_text)]

            # ✅ Handle trailing splitter (e.g., "I like red but")
            if len(segments) == 1 and segments[0] == "":
                return True, [doc[:splitter_index].text.strip()]

            # Handle trailing empty: e.g. "I like red; but"
            if len(segments) == 2 and segments[1] == "":
                return True, [doc[:splitter_index].text.strip()]

            # Cleanup and return
            segments = [seg for seg in segments if seg.strip()]
            return True, segments

        # Case B: Splitter inside the sentence
        first_segment = doc[:splitter_index].text.strip()
        second_segment = doc[splitter_index + 1:].text.strip()
        return True, [first_segment, second_segment]

    # Step 3: Fallback — punctuation-based segmentation
    if any(punct in text for punct in [".", ";", ","]):
        segments = [seg.strip() for seg in re.split(r"[.;,]", text) if seg.strip()]
        if len(segments) >= 2:
            segments = [seg for seg in segments if seg.strip()]
            return True, segments

    return False, [text.strip()]

############################## III. Double sentiment detection

def classify_segments_by_sentiment_no_neutral(has_splitter: bool, segments: list[str]) -> dict[str, list[str]]:
    """
    Classify each independent segment into positive or negative categories using detect_sentiment().
    Neutral results are mapped using dynamic negation detection (spaCy-based).
    """
    classification = {
        "positive": [],
        "negative": []
    }

    def map_sentiment(predicted: str, text: str) -> str:
        # Dynamically detect negation if model returned "neutral"
        if predicted == "neutral" and is_negated(text):
            print(f"[🧠 NEGATION DETECTED] '{text}' → forcing 'negative'")
            return "negative"
        return predicted

    for seg in segments:
        sentiment = detect_sentiment(seg)
        mapped = map_sentiment(sentiment, seg)
        classification[mapped].append(seg)

    return classification

def is_negated(text: str) -> bool:
    doc = nlp(text)
    return any(tok.dep_ == "neg" for tok in doc)
