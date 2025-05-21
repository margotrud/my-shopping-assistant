### Modifier Vocabulary

The `Data/known_modifiers.json` file contains a curated list of modifier adjectives commonly used in makeup (e.g., "soft", "warm", "muted"). This vocabulary enables the assistant to extract and understand nuanced user preferences from natural language input.

This list was curated from real product data (e.g., Sephora, MAC), tone naming standards (e.g., Pantone SkinTone), and real-world usage in color descriptions. It is used across LLM prompting, fuzzy parsing, and testing.



## Design Decisions & Edge Cases

### ❗ Exception: Rejecting "muted lipstick" and similar color phrases

Although `"lipstick"` is technically included in the XKCD color vocabulary, it is overwhelmingly used as a product category (e.g., "matte lipstick") rather than a color descriptor.

In this project, we made a deliberate exception to **hardcode the rejection of `"lipstick"` as a tone** to avoid false-positive extractions like `"muted lipstick"` or `"pink lipstick"` being interpreted as actual color tones.

This exception:
- Keeps extraction results clean and relevant
- Prevents lipstick-based product types from polluting color suggestions
- Was the only hardcoded color-based exclusion in the system
