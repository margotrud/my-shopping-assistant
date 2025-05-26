#Chatbot/scripts/helpers.py

def split_glued_tokens(token: str, known_tokens: set[str]) -> list[str]:
    """
    Attempt to split a glued token into a sequence of known tone tokens.
    For example, "greige" → ["grey", "beige"] if both are in known_tones.

    Args:
        token (str): The glued token (e.g. "greige", "rosewood")
        known_tokens (set[str]): Set of known base tone tokens (e.g. {"grey", "beige"})

    Returns:
        list[str]: Sequence of known tokens if split found, else []
    """
    token = token.lower()
    n = len(token)
    results = []

    def backtrack(start, path):
        if start == n:
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            piece = token[start:end]
            if piece in known_tokens:
                path.append(piece)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    # Return first valid split (greedy match)
    return results[0] if results else []
