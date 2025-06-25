---

## Function: build_color_prompt

- **Purpose**:  
  Constructs a consistent prompt instructing the LLM to return only an RGB tuple for a given color phrase.

- **Functions It Calls**:
  - None

- **Called By**:
  - `build_llm_request_payload`

- **Importance in Project**:  
  This prompt standardizes all RGB requests sent to the LLM, ensuring minimal variation and structured outputs that are easy to parse.

- **Example**:
  ```python
  build_color_prompt("rosy nude")
  # → "What is the RGB color code for the descriptive phrase: 'rosy nude'? ..."
  ```

---

## Function: build_llm_request_payload

- **Purpose**:  
  Assembles the request payload for the LLM API, including the prompt, model, temperature, and max tokens.

- **Functions It Calls**:
  - `build_color_prompt`

- **Called By**:
  - `query_llm_for_rgb`

- **Importance in Project**:  
  Keeps the API payload logic modular and centralized, making it easier to adjust model parameters globally.

- **Example**:
  ```python
  build_llm_request_payload("warm beige")
  # → { "model": ..., "messages": [{"role": "user", "content": "..."}], ... }
  ```

---

## Function: build_llm_headers

- **Purpose**:  
  Constructs the authorization and content-type headers required for OpenRouter LLM requests.

- **Functions It Calls**:
  - None

- **Called By**:
  - `query_llm_for_rgb`

- **Importance in Project**:  
  Abstracts header generation for security and reuse, particularly helpful when rotating API keys or modifying request formats.

- **Example**:
  ```python
  build_llm_headers("sk-abc123")
  # → {"Authorization": "Bearer sk-abc123", "Content-Type": "application/json"}
  ```

---

## Function: _parse_rgb_tuple

- **Purpose**:  
  Parses the LLM's text response to extract a valid RGB tuple in the format `(R, G, B)`.

- **Functions It Calls**:
  - `re.search`

- **Called By**:
  - `query_llm_for_rgb`

- **Importance in Project**:  
  Ensures that noisy or verbose LLM responses are safely reduced to clean, structured RGB data.

- **Example**:
  ```python
  _parse_rgb_tuple("Sure! The RGB is (243, 207, 183)", debug=True)
  # → (243, 207, 183)
  ```

---

## Function: query_llm_for_rgb

- **Purpose**:  
  Sends the full request to the LLM to resolve a color phrase into an RGB value, with retry logic, caching, and debug tracing.

- **Functions It Calls**:
  - `build_llm_request_payload`
  - `build_llm_headers`
  - `_parse_rgb_tuple`
  - `cache.get_rgb()` and `cache.store_rgb()` (if provided)

- **Called By**:
  - `get_rgb_from_descriptive_color_llm_first`
  - `resolve_rgb_with_llm`

- **Importance in Project**:  
  This is the **core external I/O function** connecting descriptive color phrases to LLM-powered RGB predictions. It includes retry safety and optional caching for performance.

- **Example**:
  ```python
  query_llm_for_rgb("rosy nude", llm_client=openrouter, cache=color_cache, debug=True)
  # → (231, 180, 188)
  ```

---
---

## Function: resolve_rgb_with_llm

- **Purpose**:  
  Entry point to resolve a descriptive color phrase into an RGB value using a hybrid strategy.  
  Starts with an LLM lookup, then falls back to simplified matches or fuzzy color matching.

- **Functions It Calls**:
  - `get_rgb_from_descriptive_color_llm_first`

- **Called By**:
  - `process_color_phrase`

- **Importance in Project**:  
  This function ensures consistent and intelligent RGB resolution. It abstracts the fallback chain and serves as the main callable for any module needing a color-to-RGB lookup.

- **Example**:
  ```python
  resolve_rgb_with_llm("rosy nude", all_webcolor_names, llm_client, cache=color_cache)
  # → (231, 180, 188)
  ```

---

## Function: get_rgb_from_descriptive_color_llm_first

- **Purpose**:  
  Performs the full RGB resolution sequence in order:
  1. Direct query to LLM
  2. Simplification + matching in XKCD or CSS4 color sets
  3. Fuzzy RGB fallback against known colors

- **Functions It Calls**:
  - `query_llm_for_rgb`
  - `simplify_color_description_with_llm`
  - `_try_simplified_match`
  - `fuzzy_match_rgb_from_known_colors`

- **Called By**:
  - `resolve_rgb_with_llm`

- **Importance in Project**:  
  This is the **core color intelligence routine**. It intelligently balances LLM output with known vocabularies and resilient fallback strategies to ensure RGB coverage for even non-standard input.

- **Example**:
  ```python
  get_rgb_from_descriptive_color_llm_first("blushed taupe", all_webcolor_names, llm_client, debug=True)
  # → (205, 180, 190)
  ```

---

## Function: _try_simplified_match

- **Purpose**:  
  Attempts to match a simplified color phrase directly to official XKCD or CSS4 color dictionaries.  
  Converts hex color codes into RGB if a match is found.

- **Functions It Calls**:
  - `hex_to_rgb`

- **Called By**:
  - `get_rgb_from_descriptive_color_llm_first`

- **Importance in Project**:  
  This method serves as a **deterministic fallback** to the LLM. It boosts performance by skipping further fuzzy logic if a clean match is possible via simplification.

- **Example**:
  ```python
  _try_simplified_match("deep lavender", all_webcolor_names, debug=True)
  # → (150, 123, 182)
  ```

---
---

## Function: simplify_phrase_if_needed

- **Purpose**:  
  Attempts to simplify a descriptive color phrase by:
  1. Checking if it’s a valid tone
  2. Applying suffix-based fallback logic (e.g., `"peachy"` → `"light peach"`)
  3. Returning the raw phrase if no simplification is possible

- **Functions It Calls**:
  - `is_valid_tone`
  - `extract_suffix_fallbacks`

- **Called By**:
  - `get_rgb_from_descriptive_color_llm_first`

- **Importance in Project**:  
  This function ensures color phrases are interpreted safely and consistently before LLM calls, helping handle common user modifiers like `"rosy"`, `"bluish"`, or `"taupey"`.

- **Example**:
  ```python
  simplify_phrase_if_needed("peachy", known_modifiers, known_tones, debug=True)
  # → "light peach"
  ```

---

## Function: is_valid_tone

- **Purpose**:  
  Checks if a color phrase exactly matches a known tone.

- **Functions It Calls**:
  - None

- **Called By**:
  - `simplify_phrase_if_needed`

- **Importance in Project**:  
  This is a fast guard clause that prevents unnecessary LLM lookups or suffix parsing if the phrase is already valid.

- **Example**:
  ```python
  is_valid_tone("beige", known_tones)
  # → True
  ```

---

## Function: extract_suffix_fallbacks

- **Purpose**:  
  Attempts to reduce suffix-based color tokens into known modifier + tone pairs.  
  Works with suffixes like `"y"` or `"ish"` (e.g., `"dusty"`, `"bluish"`, `"mochish"`).

- **Functions It Calls**:
  - `resolve_modifier_token`

- **Called By**:
  - `simplify_phrase_if_needed`

- **Importance in Project**:  
  Helps interpret informal or stylistically modified color descriptions often used by real users, recovering valid interpretations from partial roots.

- **Example**:
  ```python
  extract_suffix_fallbacks("dusty", known_modifiers, known_tones, debug=True)
  # → "dust dusty"
  ```

---

## Function: build_prompt

- **Purpose**:  
  Generates a natural language prompt to ask the LLM to return a simplified tone (e.g., `"soft pink"`).

- **Functions It Calls**:
  - None

- **Called By**:
  - `simplify_color_description_with_llm`

- **Importance in Project**:  
  Controls the phrasing used in LLM interactions. Simpler, more targeted prompts result in higher accuracy from the model.

- **Example**:
  ```python
  build_prompt("rosy nude")
  # → "What is the simplified base color or tone implied by: 'rosy nude'?"
  ```

---

## Function: simplify_color_description_with_llm

- **Purpose**:  
  Sends a simplification request to the LLM to return a normalized tone or tone+modifier phrase.  
  Caches the result if a cache object is provided.

- **Functions It Calls**:
  - `build_prompt`
  - `cache.get_simplified()` and `cache.store_simplified()` if caching is active

- **Called By**:
  - `get_rgb_from_descriptive_color_llm_first`

- **Importance in Project**:  
  This is the **last-resort simplifier** when suffix fallback fails. It gives the model a chance to resolve vague or abstract phrases before matching against known tones.

- **Example**:
  ```python
  simplify_color_description_with_llm("soft autumn haze", llm_client, cache=cache, debug=True)
  # → "muted peach"
  ```

---
