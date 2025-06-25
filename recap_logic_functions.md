---

## Function: build_tone_modifier_mappings

- **Purpose**:  
  Analyzes a list of descriptive phrases to extract modifier-tone relationships.  
  Supports suffix tolerance for modifier variants like `"rosy"` → `"rose"`, `"glowy"` → `"glow"`.

- **Functions It Calls**:
  - `normalize_modifier` (internal helper function)

- **Called By**:
  - `format_tone_modifier_mappings`
  - `build_color_sentiment_summary`

- **Importance in Project**:  
  This is the **core function for tag enrichment**, used in filtering, visual grouping, or tone clustering based on user input.  
  Without it, the assistant can't reason about what tone each modifier influences.

- **Example**:
  ```python
  build_tone_modifier_mappings(
      ["soft pink", "dusty rose"],
      known_tones,
      known_modifiers
  )
  # → (
  #     {"pink", "rose"},
  #     {"soft", "dusty"},
  #     {"soft": {"pink"}, "dusty": {"rose"}},
  #     {"pink": {"soft"}, "rose": {"dusty"}}
  # )
  ```

---

## Function: format_tone_modifier_mappings

- **Purpose**:  
  Converts the raw tone-modifier data from `build_tone_modifier_mappings` into a clean, sorted, and display-friendly dictionary.

- **Functions It Calls**:
  - `build_tone_modifier_mappings`

- **Called By**:
  - `build_color_sentiment_summary`
  - Any UI, API, or visualization layer that needs to display color groupings

- **Importance in Project**:  
  This is a **presentation adapter** that prepares tone/modifier relations for human-facing consumption, including dashboards, logs, or front-end payloads.

- **Example**:
  ```python
  format_tone_modifier_mappings(
      ["soft pink", "dusty rose"],
      known_tones,
      known_modifiers
  )
  # → {
  #     "modifiers": {"soft": ["pink"], "dusty": ["rose"]},
  #     "tones": {"pink": ["soft"], "rose": ["dusty"]}
  #   }
  ```

---
---

## Function: process_color_phrase

- **Purpose**:  
  Executes a complete resolution pipeline for a single descriptive phrase:
  1. Attempts rule-based or suffix simplification
  2. Falls back to LLM simplification (if needed)
  3. Resolves RGB using `resolve_rgb_with_llm`

- **Functions It Calls**:
  - `simplify_phrase_if_needed`
  - `simplify_color_description_with_llm`
  - `resolve_rgb_with_llm`

- **Called By**:
  - `process_segment_colors`

- **Importance in Project**:  
  This is the **core phrase-level pipeline** used for turning vague natural input into usable RGB triples. It abstracts all simplification and lookup logic for individual inputs like `"dusty rose"` or `"rosy nude"`.

- **Example**:
  ```python
  process_color_phrase("rosy nude", known_modifiers, all_webcolor_names, llm_client, cache, debug=True)
  # → ("rosy nude", (231, 180, 188))
  ```

---

## Function: process_segment_colors

- **Purpose**:  
  Runs `process_color_phrase()` on a list of color phrases (typically extracted from a sentence), returning two lists:
  - simplified phrases
  - corresponding RGB values

- **Functions It Calls**:
  - `process_color_phrase`

- **Called By**:
  - `aggregate_color_phrase_results`

- **Importance in Project**:  
  This is the **segment-level batch processor**, transforming extracted color chunks into structured RGB data for UI, recommendation, or sentiment analysis.

- **Example**:
  ```python
  process_segment_colors(
      ["soft pink", "muted coral"],
      known_modifiers,
      all_webcolor_names,
      llm_client,
      cache,
      debug=True
  )
  # → (["soft pink", "muted coral"], [(255,192,203), (240,128,128)])
  ```

---

## Function: resolve_fallback_tokens

- **Purpose**:  
  Attempts to recover missed descriptive tokens that were not caught by the main compound phrase extractor.  
  Uses token-level checks and modifier resolution as a last resort.

- **Functions It Calls**:
  - `resolve_modifier_token`

- **Called By**:
  - `extract_all_descriptive_color_phrases` (via fallback recovery logic)

- **Importance in Project**:  
  This function boosts **recall** in fuzzy or informal input where some tokens are missed due to formatting, token splitting, or poor phrasing. It rescues overlooked tones like `"coral"` or suffixy modifiers like `"mochish"`.

- **Example**:
  ```python
  tokens = nlp("maybe something mocha")
  resolve_fallback_tokens(tokens, known_modifiers, known_tones, debug=True)
  # → {"mocha"}
  ```

---
---

## Function: is_blocked_modifier_tone_pair

- **Purpose**:  
  Determines whether a given modifier-tone combination should be **suppressed** based on a predefined blocklist.  
  Prevents invalid or stylistically incoherent phrases like `"light night"` or `"romantic dramatic"` from being extracted.

- **Functions It Calls**:
  - None

- **Called By**:
  - `extract_from_adjacent`
  - `attempt_mod_tone_pair`

- **Importance in Project**:  
  This function enforces **semantic integrity** in color phrase extraction by excluding phrases that are logically or visually meaningless within the domain. It filters out rare but problematic matches.

- **Example**:
  ```python
  is_blocked_modifier_tone_pair("light", "night")
  # → True

  is_blocked_modifier_tone_pair("dusty", "rose")
  # → False
  ```

---
---

## Function: get_valid_tokens

- **Purpose**:  
  Scans the input text and extracts all full expression aliases found in the expression map.  
  Ensures longer aliases like `"soft glam"` are prioritized over their substrings like `"soft"`.

- **Functions It Calls**:
  - `re.search`

- **Called By**:
  - `match_expression_aliases` or related alias mappers

- **Importance in Project**:  
  Provides **clean alias filtering** by preventing partial or overlapping matches, a critical step before running fuzzy or modifier-based inference.

- **Example**:
  ```python
  get_valid_tokens("I want a soft glam look", expression_map)
  # → ['soft glam']
  ```

---

## Function: extract_alias_matches

- **Purpose**:  
  Uses literal and fuzzy matching logic to identify style/aesthetic expression tags (like `"romantic"`, `"elegant"`, etc.) from user input.

- **Functions It Calls**:
  - `singularize`
  - `are_antonyms`
  - `fuzz.ratio`

- **Called By**:
  - `map_expressions_to_tones`

- **Importance in Project**:  
  This is the **core matcher** that connects natural user phrasing to expression tags via multi-path matching. It supports typo tolerance, synonymy, and negation-aware filters.

- **Example**:
  ```python
  extract_alias_matches("I want a romantic soft look", expression_def)
  # → {'romantic'}
  ```

---

## Function: map_expressions_to_tones

- **Purpose**:  
  Maps detected expression tags to their related tone modifiers.  
  Applies:
  1. Literal and fuzzy alias extraction
  2. Context-based expression promotion
  3. Suppression rules for conflicting tags

- **Functions It Calls**:
  - `extract_alias_matches`
  - `apply_expression_context_rules`
  - `apply_expression_suppression_rules`

- **Called By**:
  - Any pipeline trying to infer tones from abstract aesthetic input

- **Importance in Project**:  
  This is the **expression → tone bridge**, helping map abstract intent (e.g., `"elegant"`) into actual descriptive modifiers (e.g., `"refined"`, `"rosy"`).

- **Example**:
  ```python
  map_expressions_to_tones("something timeless and elegant", expression_def, known_tones, debug=True)
  # → {'elegant': ['refined', 'polished']}
  ```

---

## Function: apply_expression_context_rules

- **Purpose**:  
  Promotes expressions that were not matched literally but are **contextually implied** based on required and clue token co-occurrence.

- **Functions It Calls**:
  - None

- **Called By**:
  - `map_expressions_to_tones`

- **Importance in Project**:  
  Captures implicit meaning by **boosting** expressions that are suggested by context (e.g., `"evening"` promoted when `"night"` and `"glam"` are both present).

- **Example**:
  ```python
  apply_expression_context_rules(
      tokens=["night", "glam"],
      matched_expressions=set(),
      context_map=context_rules
  )
  # → {"evening"}
  ```

---

## Function: apply_expression_suppression_rules

- **Purpose**:  
  Removes lower-priority expressions if a dominant, semantically conflicting one is also matched.  
  E.g., suppresses `"natural"` if `"glamorous"` is present.

- **Functions It Calls**:
  - None

- **Called By**:
  - `map_expressions_to_tones`

- **Importance in Project**:  
  Maintains **expression clarity** by avoiding contradictory tag pairs from appearing together in final results.

- **Example**:
  ```python
  apply_expression_suppression_rules({"natural", "glamorous", "romantic"})
  # → {"glamorous", "romantic"}
  ```

---
---

## Function: build_color_sentiment_summary

- **Purpose**:  
  Aggregates all matched color tones, simplified phrases, and RGB values tied to a specific **sentiment label** (e.g., `"romantic"`, `"edgy"`).  
  Computes a representative base RGB for that group and stores it for downstream use.

- **Functions It Calls**:
  - `aggregate_color_phrase_results`
  - `format_tone_modifier_mappings`
  - `choose_representative_rgb`

- **Called By**:
  - Any sentiment-aware recommendation pipeline

- **Importance in Project**:  
  This function is a **core summarizer** for sentiment-conditioned color analysis.  
  It supports personalized recommendations, aesthetic clustering, or emotion-to-color mapping by reducing multiple segments to a single RGB anchor.

- **Example**:
  ```python
  build_color_sentiment_summary(
      sentiment="romantic",
      segments=["soft pink tones", "maybe dusty rose"],
      known_tones=known_tones,
      known_modifiers=known_modifiers,
      rgb_map={},
      base_rgb_by_sentiment={}
  )
  # → {
  #     "matched_color_names": ["dusty rose", "soft pink"],
  #     "base_rgb": (230, 180, 190),
  #     "threshold": 60.0
  #   }
  ```

---
