

## Function: extract_compound_phrases

- **Purpose**:  
  Detects color phrases made from a modifier + tone, using 3 strategies:
  1. adjacent tokens (e.g. `"soft pink"`)
  2. dashed or malformed tokens (e.g. `"dusty-rose"`)
  3. glued tokens (e.g. `"mutedrose"`)

- **Functions It Calls**:
  - `extract_from_adjacent`
  - `extract_from_split`
  - `extract_from_glued`

- **Called By**:
  - `extract_all_descriptive_color_phrases`

- **Importance in Project**:  
  This is the **central entry point** for compound phrase recognition.  
  Without it, the system can't detect multi-word or merged color expressions.

- **Example**:
  ```python
  tokens = nlp("I want something dustyrose or soft pink")
  extract_compound_phrases(tokens, known_tones, known_modifiers, webcolor_names, debug=True)
  # → {'dusty rose', 'soft pink'}
  ```

---

## Function: extract_from_adjacent

- **Purpose**:  
  Detects compound color phrases made of an adjacent modifier + tone pair, like:
  - `"soft pink"`
  - `"muted beige"`

  This is the **fastest and most reliable** extraction method since it uses direct token adjacency (e.g., `ADJ + NOUN`) from spaCy's parsing.

- **Functions It Calls**:
  - `resolve_modifier_token` – resolves and validates modifiers and tones (with suffix stripping and fuzzy logic off)
  - `should_suppress_compound` – filters invalid modifier-tone combos (e.g., `"light night"`)

- **Called By**:
  - `extract_compound_phrases`

- **Importance in Project**:  
  It’s the **primary low-level strategy** for phrase detection. This method sets the baseline for color phrase extraction, catching the majority of well-formed input (like `"deep red"` or `"warm nude"`).

- **Example**:
  ```python
  tokens = nlp("I'd love something soft pink or muted beige")
  extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, all_webcolor_names, debug=True)
  # → adds: 'soft pink', 'muted beige' to compounds
  ```

---

## Function: split_tokens_to_parts

- **Purpose**:  
  Splits two token strings (`t1`, `t2`) into their internal sub-components using vocabulary-based deconstruction.  
  Used to recover compound candidates when tokens are malformed, glued, or partially merged.

- **Functions It Calls**:
  - `split_glued_tokens` – splits a glued word like `"dustyrose"` into valid components like `["dusty", "rose"]`
  - `singularize` – normalizes pluralized tones (e.g., `"pinks"` → `"pink"`)

- **Called By**:
  - `extract_from_split`

- **Importance in Project**:  
  Enables recovery of descriptive phrases when token boundaries are malformed. For instance, `"dustyrose tones"` would not be caught by direct adjacency and needs token-level splitting.

- **Example**:
  ```python
  t1 = "dustyrose"
  t2 = "tones"
  split_tokens_to_parts(t1, t2, known_color_tokens, debug=True)
  # → (["dusty", "rose"], ["tones"])
  ```

---
---

## Function: attempt_mod_tone_pair

- **Purpose**:  
  Validates a candidate modifier + tone pair and adds it to the output compound lists if it passes all checks.  
  Used during deconstruction logic (e.g., glued or malformed input like `"dustyrose"` → `"dusty" + "rose"`).

- **Functions It Calls**:
  - `resolve_modifier_token` – ensures the tone candidate is a valid known tone
  - `should_suppress_compound` – blocks combinations like `"light night"` or redundant suffix forms

- **Called By**:
  - `extract_from_split`

- **Importance in Project**:  
  This function is a **safety gate** for compound suggestions. It prevents invalid or illogical extractions during token splitting, ensuring only clean modifier-tone pairs are included.

- **Example**:
  ```python
  attempt_mod_tone_pair(
      mod_candidate="dusty",
      mod="dusty",
      tone_candidate="rose",
      compounds=compounds,
      raw_compounds=raw_compounds,
      known_modifiers=known_modifiers,
      known_tones=known_tones,
      all_webcolor_names=all_webcolor_names,
      debug=True
  )
  # → adds "dusty rose" if both components are valid
  ```

---

## Function: extract_from_split

- **Purpose**:  
  Attempts to recover compound color phrases by splitting mis-tokenized or malformed adjacent tokens.  
  This is useful for fixing broken input like `"dustyrose tones"` or `"taupeybeige shade"`.

- **Functions It Calls**:
  - `split_tokens_to_parts` – tries to break `t1` and `t2` into sub-tokens
  - `resolve_modifier_token` – resolves candidate modifier segments
  - `attempt_mod_tone_pair` – validates and adds each compound pair

- **Called By**:
  - `extract_compound_phrases`

- **Importance in Project**:  
  This is the **recovery mechanism** for malformed color phrases. It extends robustness by salvaging meaning from user typos, fused tokens, or stylistic joins.

- **Example**:
  ```python
  tokens = nlp("looking for taupeybeige tones")
  extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug=True)
  # → adds: "taupey beige"
  ```

---
---

## Function: extract_all_descriptive_color_phrases

- **Purpose**:  
  Full pipeline to extract all descriptive color phrases from raw input text.  
  It combines compound detection, standalone modifiers/tones, lone noun tones, and suffix-based fallbacks into a single unified list.

- **Functions It Calls**:
  - `extract_compound_phrases`
  - `extract_standalone_phrases`
  - `extract_lone_tones`
  - `extract_suffix_fallbacks`

- **Called By**:
  - `extract_phrases_from_segment`

- **Importance in Project**:  
  This function acts as the **master controller** of all rule-based extraction logic. It ensures complete and robust phrase extraction from any user sentence.

- **Example**:
  ```python
  extract_all_descriptive_color_phrases(
      "I love dusty rose blush and peachy tones",
      known_tones,
      known_modifiers,
      all_webcolor_names,
      debug=True
  )
  # → ['dusty rose', 'peachy', 'rose']
  ```

---

## Function: extract_phrases_from_segment

- **Purpose**:  
  Convenience wrapper that applies global vocabularies and calls the full color extraction pipeline on a single text segment.

- **Functions It Calls**:
  - `load_known_modifiers`
  - `extract_all_descriptive_color_phrases`

- **Called By**:
  - `process_segment_colors`
  - `aggregate_color_phrase_results`

- **Importance in Project**:  
  This is a **lightweight adapter** function that ensures consistent vocabulary injection and simplifies downstream usage in segmentation pipelines.

- **Example**:
  ```python
  extract_phrases_from_segment("maybe something like warm beige", debug=True)
  # → ['warm beige']
  ```

---

## Function: aggregate_color_phrase_results

- **Purpose**:  
  Aggregates simplified color phrase outputs from multiple user segments.  
  It extracts descriptive color terms, resolves RGB values, and produces a unified summary.

- **Functions It Calls**:
  - `extract_phrases_from_segment`
  - `process_segment_colors` (assumed external function doing LLM+RGB work)

- **Called By**:
  - `build_color_sentiment_summary` (and potentially LLM or recommendation engines)

- **Importance in Project**:  
  This is the **integration point** for multi-turn or multi-segment processing. It allows fragmented input to be merged into a single structured output for recommendation, UI display, or visualization.

- **Example**:
  ```python
  aggregate_color_phrase_results(
      segments=["soft pink glow", "maybe muted beige"],
      known_modifiers=known_modifiers,
      all_webcolor_names=all_webcolor_names,
      llm_client=llm_api,
      debug=True
  )
  # → (
  #     {'soft pink', 'muted beige'},
  #     ['soft pink', 'muted beige'],
  #     {'soft pink': (255, 192, 203), 'muted beige': (222, 203, 192)}
  #   )
  ```

---

---

## Function: extract_standalone_phrases

- **Purpose**:  
  Identifies standalone tone or modifier tokens that are not part of any compound.  
  It combines:
  1. modifiers explicitly injected from expressions
  2. tokens resolved independently as valid modifiers or tones

- **Functions It Calls**:
  - `_inject_expression_modifiers`
  - `_extract_filtered_tokens`
  - `_finalize_standalone_phrases`

- **Called By**:
  - `extract_all_descriptive_color_phrases`

- **Importance in Project**:  
  This is the **second pass** in color extraction, allowing the system to recover meaningful descriptive terms that were not part of phrases like `"soft pink"` but still convey user intent (e.g., `"peachy"`, `"natural"`).

- **Example**:
  ```python
  tokens = nlp("a warm beige or peachy tone")
  extract_standalone_phrases(tokens, known_modifiers, known_tones, debug=True)
  # → {'warm', 'peachy'}
  ```

---

## Function: _inject_expression_modifiers

- **Purpose**:  
  Adds modifier words found in the token stream if they are valid and not blocked by cosmetic noun contexts.

- **Functions It Calls**:
  - None (internal loop)

- **Called By**:
  - `extract_standalone_phrases`

- **Importance in Project**:  
  Ensures that even out-of-phrase modifiers like `"romantic"` or `"gentle"` get extracted, **especially when user input is short or stylistic**.

- **Example**:
  ```python
  _inject_expression_modifiers(nlp("romantic and soft"), known_modifiers, debug=True)
  # → {'romantic', 'soft'}
  ```

---

## Function: _extract_filtered_tokens

- **Purpose**:  
  Filters the token list to return only valid resolved standalone tones or modifiers, excluding any cosmetic product nouns.

- **Functions It Calls**:
  - `resolve_modifier_token`

- **Called By**:
  - `extract_standalone_phrases`

- **Importance in Project**:  
  Applies resolution logic to surface descriptive color terms that weren’t part of compound phrases (e.g., `"peachy"`, `"nude"`), but are still meaningful on their own.

- **Example**:
  ```python
  _extract_filtered_tokens(nlp("love peachy makeup"), known_modifiers, known_tones, debug=True)
  # → {'peachy'}
  ```

---

## Function: _finalize_standalone_phrases

- **Purpose**:  
  Merges injected modifiers and resolved filtered tokens into a final deduplicated set.

- **Functions It Calls**:
  - None

- **Called By**:
  - `extract_standalone_phrases`

- **Importance in Project**:  
  This is a **combining step** to unify both signal paths (expression-based and standalone resolution), creating the final usable output.

- **Example**:
  ```python
  _finalize_standalone_phrases({"romantic"}, {"peachy"}, debug=True)
  # → {'romantic', 'peachy'}
  ```

---

## Function: extract_lone_tones

- **Purpose**:  
  Captures color tone tokens that appear by themselves and are not part of any known compound.  
  Focuses on isolated tone nouns like `"pink"` or `"beige"` when they stand alone in a sentence.

- **Functions It Calls**:
  - None

- **Called By**:
  - `extract_all_descriptive_color_phrases`

- **Importance in Project**:  
  This is the **fallback safety net** for short or ambiguous input like `"maybe beige"`, where no compound exists but color intent is still clear.

- **Example**:
  ```python
  tokens = nlp("not sure, maybe beige")
  extract_lone_tones(tokens, known_tones, debug=True)
  # → {'beige'}
  ```

---
