# Utilities – Config Loader

This module provides generic utility functions for loading configuration data from the project-level `Data/` directory. It enables all other modules (LLM logic, color matching, expression categorization, etc.) to dynamically load vocabulary files or mappings such as:

- `known_modifiers.json`
- `expression_triggers.json`
- `expression_context_rules.json`

## Why centralize loading?

To avoid repetition and improve maintainability. Instead of defining one loader function per config file, the project uses a single, generic `load_json_from_data_dir()` function with a flexible interface:

```python
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir

known_modifiers = set(load_json_from_data_dir("known_modifiers.json"))
expression_triggers = load_json_from_data_dir("expression_triggers.json")
