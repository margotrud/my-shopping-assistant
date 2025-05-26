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

    # 🚫 Early block: if negation + "or" + no punctuation, avoid segmenting
    has_negation = any(tok.dep_ == "neg" for tok in doc)
    has_or = any(tok.text.lower() == "or" for tok in doc)
    has_punct = any(tok.text in {".", ",", ";"} for tok in doc)
    if has_negation and has_or and not has_punct:
        return False, [text.strip()]

    splitter_index = None

    for i, token in enumerate(doc):
        # Case 1: "and"/"or" between two adjectives or nouns → skip as splitter
        if token.dep_ == "cc" and token.text.lower() in {"and", "or"}:
            prev = doc[i - 1] if i > 0 else None
            next_ = doc[i + 1] if i + 1 < len(doc) else None

            if prev and next_:
                if prev.pos_ in {"ADJ", "NOUN"} and next_.pos_ in {"ADJ", "NOUN"}:
                    continue  # "and"/"or" connecting two tones/modifiers — do not split

        # Case 2: clause-level conjunctions or markers
        if token.dep_ in {"cc", "mark", "discourse"}:
            splitter_index = i
            break

        # Case 3: discourse adverb (e.g. "however", "but", etc.)
        if token.dep_ == "advmod":
            next_token = doc[i + 1] if i + 1 < len(doc) else None
            if next_token and next_token.dep_ in {"amod", "acomp", "dobj", "advmod"}:
                continue
            prev_token = doc[i - 1] if i > 0 else None
            prev_punct = prev_token.is_punct if prev_token else False
            if i == 0 or (prev_token and prev_punct and token.is_alpha):
                splitter_index = i
                break

    if splitter_index is not None:
        # Case A: Start or end of sentence
        if splitter_index == 0 or splitter_index == len(doc) - 1:
            remaining_tokens = list(doc[splitter_index + 1:])
            cleaned_tokens = []
            skip = True
            for tok in remaining_tokens:
                if skip and tok.dep_ in {"mark", "advmod", "discourse"} and tok.pos_ in {"SCONJ", "ADV"}:
                    continue
                skip = False
                cleaned_tokens.append(tok)
            remaining_text = " ".join(tok.text for tok in cleaned_tokens).strip()
            segments = [seg.strip() for seg in re.split(r"[;,]", remaining_text)]
            if len(segments) == 1 and segments[0] == "":
                return True, [doc[:splitter_index].text.strip()]
            if len(segments) == 2 and segments[1] == "":
                return True, [doc[:splitter_index].text.strip()]
            return True, [seg for seg in segments if seg.strip()]

        # Case B: Split at detected conjunction
        first_segment = doc[:splitter_index].text.strip()
        second_segment = doc[splitter_index + 1:].text.strip()
        return True, [first_segment, second_segment]

    # Fallback: punctuation-based segmentation
    if any(punct in text for punct in [".", ";", ","]):
        segments = [seg.strip() for seg in re.split(r"[.;,]", text) if seg.strip()]
        if len(segments) >= 2:
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
        if predicted == "neutral":
            if is_negated(text) or is_softly_negated(text):
                print(f"[🧠 FALLBACK NEGATION DETECTED] '{text}' → forcing 'negative'")
                return "negative"
            else:
                return "positive"
        return predicted

    for seg in segments:
        try:
            sentiment = detect_sentiment(seg)
            mapped = map_sentiment(sentiment, seg)
            classification[mapped].append(seg)
        except Exception as e:
            print(f"[❌ SENTIMENT ERROR] → {e}")

    return classification



def is_negated(text: str) -> bool:
    doc = nlp(text)

    # direct negation (not, never, etc.)
    if any(tok.dep_ == "neg" for tok in doc):
        return True

    # check for cases like "no brown", "no coral"
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
    doc = nlp(text.lower())

    for i in range(len(doc) - 2):
        t1, t2, t3 = doc[i], doc[i + 1], doc[i + 2]

        # expanded check for soft negation structures like 'nothing too metallic'
        if (
            t1.text.lower() in {"nothing", "not", "no"} and
            t2.text.lower() == "too" and
            t3.pos_ == "ADJ"
        ):
            return True

    return False
