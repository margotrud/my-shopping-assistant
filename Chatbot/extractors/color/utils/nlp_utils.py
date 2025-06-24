# Chatbot/extractors/color/utils/nlp_utils.py

"""
nlp_utils.py
============

Natural language helpers for token-level relationship checks.

Currently supports:
- WordNet-based antonym detection
"""

from nltk.corpus import wordnet


def are_antonyms(word1: str, word2: str) -> bool:
    """
    Determines whether two words are antonyms based on WordNet definitions.

    This function checks all synsets (word senses) of the first word,
    and inspects each lemma (canonical form) for listed antonyms.
    If the second word appears as an antonym of any lemma, it returns True.

    ⚠️ Note:
        - This function strictly uses the antonym relationships defined in NLTK's WordNet.
        - It does NOT infer antonyms using logic, embeddings, or semantic similarity.
        - Common-sense or intuitive opposites like ("create", "destroy") may return False
          if WordNet lacks an explicit antonym relation.

    Args:
        word1 (str): The first word to compare.
        word2 (str): The second word to check as a possible antonym of the first.

    Returns:
        bool: True if word2 is a WordNet-defined antonym of word1; False otherwise.
    """
    for syn in wordnet.synsets(word1):
        for lemma in syn.lemmas():
            if word2 in [ant.name() for ant in lemma.antonyms()]:
                return True
    return False
