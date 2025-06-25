---

## Function: normalize_token

- **Purpose**:  
  Standardizes a token by stripping whitespace and converting to lowercase.

- **Functions It Calls**:
  - None

- **Called By**:
  - `fuzzy_token_match`
  - `is_exact_match`

- **Importance in Project**:  
  Ensures consistent comparison across token matchers.

- **Example**:
  ```python
  normalize_token("  Peachy  ")
  # → "peachy"
  ```

---

## Function: fuzzy_token_match

- **Purpose**:  
  Computes a blended fuzzy score between two tokens using multiple strategies:
  - literal equality
  - Word-level similarity (`fuzz.partial_ratio`, `fuzz.ratio`)
  - Bonus for common prefixes

- **Functions It Calls**:
  - `normalize_token`

- **Called By**:
  - `_fuzzy_match_modifier`
  - `is_strong_fuzzy_match`

- **Example**:
  ```python
  fuzzy_token_match("peachy", "peach")
  # → ~90
  ```

---

## Function: match_expression_aliases

- **Purpose**:  
  Determines if the input string fuzzily matches any known alias in a list, using both partial and token-sort ratios.

- **Functions It Calls**:
  - `fuzz.partial_ratio`
  - `fuzz.token_sort_ratio`

- **Called By**:
  - Expression matching logic (`extract_alias_matches`)

- **Example**:
  ```python
  match_expression_aliases("work appropriate", ["work safe", "professional"])
  # → True
  ```

---

## Function: should_accept_multiword_alias

- **Purpose**:  
  Evaluates if a multi-word alias should be accepted based on a fuzzy match against user input.

- **Functions It Calls**:
  - `fuzz.partial_ratio`

- **Called By**:
  - Fuzzy alias acceptance logic

- **Example**:
  ```python
  should_accept_multiword_alias("work appropriate", "something more work appropriate")
  # → True
  ```

---

## Function: is_exact_match

- **Purpose**:  
  Checks if two tokens are equal after normalization.

- **Functions It Calls**:
  - `normalize_token`

- **Called By**:
  - Exact match filters

- **Example**:
  ```python
  is_exact_match(" Blush ", "blush")
  # → True
  ```

---

## Function: is_strong_fuzzy_match

- **Purpose**:  
  Combines fuzzy scoring with conflict detection to determine if two tokens are a strong match.

- **Functions It Calls**:
  - `fuzzy_token_match`
  - `is_negation_conflict`

- **Called By**:
  - Alias match safety logic

- **Example**:
  ```python
  is_strong_fuzzy_match("natural", "natrual")
  # → True
  ```

---

## Function: is_embedded_alias_conflict

- **Purpose**:  
  Returns True if one alias is a **substring** of another longer one, potentially leading to semantic conflict.

- **Functions It Calls**:
  - None

- **Called By**:
  - Alias filtering / conflict suppression

- **Example**:
  ```python
  is_embedded_alias_conflict("glamorous", "glam")
  # → True
  ```

---

## Function: is_modifier_compound_conflict

- **Purpose**:  
  Detects if an expression (e.g., `"natural"`) is **dual-used** both as a modifier and a style expression.

- **Functions It Calls**:
  - None

- **Called By**:
  - Expression parsing safety logic

- **Example**:
  ```python
  is_modifier_compound_conflict("natural", known_modifiers)
  # → True
  ```

---

## Function: remove_subsumed_matches

- **Purpose**:  
  Removes short alias matches that are **subsumed** by longer, more descriptive ones.  
  Useful when `"glam"` and `"soft glam"` both matched, but only the latter should be retained.

- **Functions It Calls**:
  - `re.search`

- **Called By**:
  - Alias filter pipelines

- **Example**:
  ```python
  remove_subsumed_matches(["soft glam", "glam"])
  # → ["soft glam"]
  ```

---

## Function: is_negation_conflict

- **Purpose**:  
  Flags conflict where one phrase is the **negation** of the other (e.g., `"no makeup"` vs `"makeup"`).

- **Functions It Calls**:
  - None

- **Called By**:
  - Fuzzy conflict blocker

- **Example**:
  ```python
  is_negation_conflict("no glam", "glam")
  # → True
  ```

---
---

## Function: get_tokens_and_counts

- **Purpose**:  
  Tokenizes a raw input string by whitespace and returns a frequency dictionary of lowercase tokens.  
  This is a **lightweight alternative to full NLP parsing**, used when speed and simplicity are preferred.

- **Functions It Calls**:
  - None

- **Called By**:
  - Standalone token analysis
  - Frequency-aware filters
  - `extract_standalone_phrases`, `extract_lone_tones` (via token count tracking)

- **Importance in Project**:  
  This function enables **frequency-based filtering and logic**, such as preferring non-compound usages of repeated tokens like `"pink pink"`.

- **Example**:
  ```python
  get_tokens_and_counts("Soft pink and peachy tones pink")
  # → {"soft": 1, "pink": 2, "and": 1, "peachy": 1, "tones": 1}
  ```

---
