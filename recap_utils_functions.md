---

## Function: get_all_trigger_tokens

- **Purpose**:  
  Loads all **modifier and alias tokens** for each expression tag from `expression_definition.json`.  
  This includes multi-word triggers like `"soft glam"` and single-word ones like `"romantic"` or `"edgy"`.

- **Functions It Calls**:
  - `load_json_from_data_dir("expression_definition.json")`

- **Called By**:
  - Expression parsing modules
  - `extract_standalone_phrases`, `match_expression_aliases`, or token filter utilities

- **Importance in Project**:  
  This function defines the **recognition vocabulary** for aesthetic expressions. It powers alias detection, tone injection, and fuzzy tag interpretation.

- **Example**:
  ```python
  get_all_trigger_tokens()
  # → {
  #     "romantic": ["soft", "flirty", "date", "lovely"],
  #     "elegant": ["refined", "formal", "timeless"]
  #   }
  ```

---

## Function: get_glued_token_vocabulary

- **Purpose**:  
  Builds a vocabulary set of all known tone, modifier, and web-safe color tokens.  
  This is used to detect and split fused tokens (e.g., `"dustyrose"` → `"dusty" + "rose"`).

- **Functions It Calls**:
  - `load_known_modifiers`

- **Called By**:
  - `split_glued_tokens`
  - `extract_from_split`
  - `extract_from_glued`

- **Importance in Project**:  
  This function defines the **token matching boundaries** for compound recovery logic. It ensures glued or malformed color descriptions are still extractable.

- **Example**:
  ```python
  get_glued_token_vocabulary()
  # → {'dusty', 'rose', 'peachy', 'lavender', ...}
  ```

---
---

## Function: is_known_tone

- **Purpose**:  
  Checks whether a word exists in the tone vocabulary.

- **Functions It Calls**:
  - None

- **Called By**:
  - Any logic that filters or validates tone candidates

- **Importance in Project**:  
  Acts as a fast lookup gate for color tone validation.

- **Example**:
  ```python
  is_known_tone("beige")
  # → True
  ```

---

## Function: match_direct_modifier

- **Purpose**:  
  Performs a direct match for a word in the modifier set.

- **Functions It Calls**:
  - None

- **Called By**:
  - `resolve_modifier_token`

- **Importance in Project**:  
  Fast and reliable way to accept standard modifiers without fallback logic.

- **Example**:
  ```python
  match_direct_modifier("dusty", known_modifiers)
  # → "dusty"
  ```

---

## Function: match_suffix_fallback

- **Purpose**:  
  Attempts to resolve words like `"rosy"` or `"mochish"` to known modifier bases like `"rose"` or `"mocha"`.

- **Functions It Calls**:
  - None

- **Called By**:
  - `resolve_modifier_token`

- **Importance in Project**:  
  Enables recovery of derived modifier forms using `"y"` and `"ish"` suffixes. Improves robustness for user-written input.

- **Example**:
  ```python
  match_suffix_fallback("rosy", known_modifiers)
  # → "rose"
  ```

---

## Function: fuzzy_match_modifier_safe

- **Purpose**:  
  Securely attempts fuzzy matching between a word and known modifiers using a similarity threshold.

- **Functions It Calls**:
  - `_fuzzy_match_modifier`

- **Called By**:
  - `resolve_modifier_token`

- **Importance in Project**:  
  Tolerates typos or off-by-one variants like `"mochy"` → `"mocha"`.

- **Example**:
  ```python
  fuzzy_match_modifier_safe("mochy", known_modifiers)
  # → "mocha"
  ```

---

## Function: _fuzzy_match_modifier

- **Purpose**:  
  Internal helper that calculates similarity scores between a raw word and all known modifiers using `fuzzy_token_match`.

- **Functions It Calls**:
  - `fuzzy_token_match`

- **Called By**:
  - `fuzzy_match_modifier_safe`

- **Importance in Project**:  
  Provides transparent scoring logic with debug output to trace fuzzy fallback decisions.

- **Example**:
  ```python
  _fuzzy_match_modifier("mochy", known_modifiers, debug=True)
  # → ("mocha", 85.7)
  ```

---

## Function: resolve_modifier_token

- **Purpose**:  
  Full resolution pipeline for mapping a token to a valid modifier.  
  Combines:
  1. Direct match
  2. Suffix fallback
  3. Tone exclusion guard
  4. Optional fuzzy match

- **Functions It Calls**:
  - `match_direct_modifier`
  - `match_suffix_fallback`
  - `fuzzy_match_modifier_safe`

- **Called By**:
  - `extract_from_adjacent`
  - `extract_from_split`
  - `extract_from_glued`
  - `extract_standalone_phrases`

- **Importance in Project**:  
  This is the **central modifier resolution function**. It enables precise and flexible recovery of modifiers even in noisy or informal user input.

- **Example**:
  ```python
  resolve_modifier_token("mochish", known_modifiers, known_tones, debug=True)
  # → "mocha"
  ```

---

## Function: is_y_suffix_from_tone

- **Purpose**:  
  Checks if a word ending in `"y"` is derived from a known tone.  
  Used to suppress over-extension (e.g., `"rosy"` → `"rose"`).

- **Functions It Calls**:
  - None

- **Called By**:
  - Derivative suppression logic in phrase extractors

- **Importance in Project**:  
  Prevents redundant or invalid extraction of tone derivatives that don’t add new value.

- **Example**:
  ```python
  is_y_suffix_from_tone("rosy", known_tones)
  # → True
  ```

---

## Function: should_suppress_compound

- **Purpose**:  
  Determines if a compound modifier-tone pair should be **rejected** due to redundancy or self-similarity.

- **Functions It Calls**:
  - None

- **Called By**:
  - `attempt_mod_tone_pair`
  - `extract_from_adjacent`

- **Importance in Project**:  
  Filters bad compounds like `"pink pink"` or `"peach peachy"` from entering the final phrase list.

- **Example**:
  ```python
  should_suppress_compound("pink", "pink")
  # → True

  should_suppress_compound("dusty", "rose")
  # → False
  ```

---
---

## Function: are_antonyms

- **Purpose**:  
  Determines whether two words are explicit antonyms according to WordNet's lexical database.  
  It inspects all word senses (synsets) for the first word and checks whether the second word is listed as an antonym for any of its lemmas.

- **Functions It Calls**:
  - `wordnet.synsets(...)` from NLTK

- **Called By**:
  - `extract_alias_matches` (during fuzzy conflict resolution)

- **Importance in Project**:  
  This function adds **semantic safety** to fuzzy matching. It prevents false positives when a user's input contradicts an alias — such as blocking `"natural"` from matching `"glamorous"` if they are antonyms.

- **Example**:
  ```python
  are_antonyms("light", "dark")
  # → True

  are_antonyms("peachy", "rosy")
  # → False
  ```

- **Caveats**:  
  - Based purely on **WordNet’s lexical graph** (not embeddings or transformer-based logic)
  - May miss intuitive opposites if no formal antonym is listed

---
---

## Function: rgb_distance

- **Purpose**:  
  Calculates the **Euclidean distance** between two RGB color values in 3D space.

- **Functions It Calls**:
  - None

- **Called By**:
  - `is_within_rgb_margin`
  - `choose_representative_rgb`

- **Importance in Project**:  
  Forms the mathematical basis for comparing color similarity — a foundational part of tone clustering and nearest match detection.

- **Example**:
  ```python
  rgb_distance((255, 192, 203), (240, 128, 128))
  # → 77.9
  ```

---

## Function: is_within_rgb_margin

- **Purpose**:  
  Determines whether two RGB colors are perceptually close within a defined threshold.

- **Functions It Calls**:
  - `rgb_distance`

- **Called By**:
  - `find_similar_color_names`

- **Importance in Project**:  
  This function supports **threshold-based color grouping** and filtering by proximity — a key requirement for identifying "visually similar" tones.

- **Example**:
  ```python
  is_within_rgb_margin((245, 222, 179), (240, 220, 180), margin=10.0)
  # → True
  ```

---

## Function: choose_representative_rgb

- **Purpose**:  
  From a group of RGB values, selects the **most central** color based on total pairwise distance.  
  Used to anchor a sentiment cluster with a single RGB tone.

- **Functions It Calls**:
  - `rgb_distance`

- **Called By**:
  - `build_color_sentiment_summary`

- **Importance in Project**:  
  Enables **sentiment-based color summarization**, choosing a best-fit RGB for a list of tones.

- **Example**:
  ```python
  choose_representative_rgb({
      "soft pink": (255, 192, 203),
      "muted rose": (240, 128, 128)
  })
  # → (255, 192, 203)
  ```

---

## Function: find_similar_color_names

- **Purpose**:  
  Finds all known color names whose RGB values fall within a distance threshold of a target RGB.

- **Functions It Calls**:
  - `is_within_rgb_margin`

- **Called By**:
  - `process_color_phrase`
  - `resolve_fallback_tokens`

- **Importance in Project**:  
  Enables the assistant to **map arbitrary RGB values** to known human-readable color names — improving clarity for UI, logs, or explanations.

- **Example**:
  ```python
  find_similar_color_names((245, 222, 179), known_rgb_map, threshold=50.0)
  # → ["wheat", "beige"]
  ```

---

## Function: fuzzy_match_rgb_from_known_colors

- **Purpose**:  
  Attempts to match a simplified color phrase to the **closest known color name** using fuzzy text similarity.

- **Functions It Calls**:
  - `difflib.get_close_matches`

- **Called By**:
  - `get_rgb_from_descriptive_color_llm_first`

- **Importance in Project**:  
  This is the **final fallback** for unknown or ambiguous phrases. It allows loose matching to known names, bridging LLM outputs with deterministic vocab.

- **Example**:
  ```python
  fuzzy_match_rgb_from_known_colors("peachy nude")
  # → "peach nude" or closest available match
  ```

---
---

## Function: split_glued_tokens

- **Purpose**:  
  Attempts to decompose a glued-together token like `"earthyrose"` into recognizable color modifiers and tones using recursive logic and fallback heuristics.

- **Functions It Calls**:
  - Internal: `recursive_split()`
  - `is_valid_token()` (defined in-place)

- **Called By**:
  - `extract_from_split`
  - `extract_from_glued`

- **Importance in Project**:  
  This is the **core degluing function**, enabling recovery of malformed or user-fused tokens like `"dustyrose"`, `"taupeybeige"`, or `"mochylavender"` by analyzing token parts against an augmented vocabulary of tones and modifiers.

- **How It Works**:
  1. **Recursively splits** the token into valid known pieces from an extended vocab
  2. If that fails, it performs a **greedy longest-match fallback** using substring matching

- **Example**:
  ```python
  split_glued_tokens("dustyrose", known_tokens, known_modifiers, debug=True)
  # → ['dusty', 'rose']
  ```

---

## Function: singularize

- **Purpose**:  
  Applies basic string rules to normalize plural cosmetic nouns into their singular form (e.g., `"blushes"` → `"blush"`).

- **Functions It Calls**:
  - None

- **Called By**:
  - `extract_standalone_phrases`
  - `extract_lone_tones`

- **Importance in Project**:  
  Ensures consistency in token comparison by avoiding mismatches due to plural forms — especially important in domains like cosmetics and fashion where plurals are common.

- **Example**:
  ```python
  singularize("lipsticks")
  # → "lipstick"

  singularize("glosses")
  # → "gloss"
  ```

---
