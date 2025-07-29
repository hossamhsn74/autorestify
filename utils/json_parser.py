import json
import re
import sys
from typing import Any
from collections import defaultdict


def camel_to_snake(name):
    """
    Converts a camelCase or PascalCase string to snake_case.

    Args:
        name (str): The input string to convert.

    Returns:
        str: The snake_case version of the input string.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def infer_type(value):
    """
    Infers the corresponding Python type hint (as a string) for a given JSON value.

    Args:
        value (Any): The value to infer the type for.

    Returns:
        str: The inferred type (e.g., 'str', 'int', 'List[str]', 'SubModel').
    """
    if isinstance(value, str):
        return "str"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, list):
        if value:
            first_item = value[0]
            if isinstance(first_item, dict):
                return f"List[{infer_model_name(first_item)}]"
            else:
                return f"List[{infer_type(first_item)}]"
        else:
            return "List[Any]"
    elif isinstance(value, dict):
        return infer_model_name(value)
    else:
        return "Any"


def infer_model_name(obj):
    """
    Returns a placeholder name for a nested model.
    Can be extended to generate dynamic or contextual names.

    Args:
        obj (dict): The nested object to name.

    Returns:
        str: The name of the nested model (default is 'SubModel').
    """
    return "SubModel"


def check_duplicates(pairs):
    """
    Detects and raises an error if duplicate keys exist in the JSON.

    Args:
        pairs (list): List of (key, value) pairs from JSON parsing.

    Returns:
        dict: A dictionary of unique key-value pairs.

    Raises:
        ValueError: If any duplicate key is found.
    """
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Duplicate key found in JSON: '{key}'")
        seen[key] = value
    return seen


def parse_json_file(path):
    """
    Loads and validates a JSON file, ensuring it's a valid, non-empty dictionary
    with unique string keys. Also triggers type extraction.

    Args:
        path (str): Path to the JSON file.

    Returns:
        tuple: A tuple containing:
            - fields (dict): Top-level fields and their types.
            - nested_models (dict): Nested models and their fields.

    Raises:
        SystemExit: On invalid JSON syntax, duplicates, wrong structure, or key types.
    """
    try:
        with open(path, "r") as f:
            data = json.load(f, object_pairs_hook=check_duplicates)

        if not isinstance(data, dict):
            print("❌ JSON root must be an object/dict.")
            raise SystemExit(1)
        if not data:
            print("❌ JSON object is empty.")
            raise SystemExit(1)
        for key in data.keys():
            if not isinstance(key, str):
                print(f"❌ Invalid key (not a string): {key}")
                raise SystemExit(1)

        return extract_fields(data)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON syntax: {e}")
        raise SystemExit(1)
    except ValueError as ve:
        print(f"❌ Validation Error: {ve}")
        raise SystemExit(1)


def extract_fields(data):
    """
    Recursively extracts fields and their types from a JSON object,
    including nested models and lists of objects.

    Args:
        data (dict): Parsed JSON data.

    Returns:
        tuple: A tuple containing:
            - fields (dict): Field name to type mappings.
            - nested_models (dict): Nested model names mapped to their fields.
    """
    fields = {}
    nested_models = {}
    for key, value in data.items():
        field_name = camel_to_snake(key)
        value_type = infer_type(value)
        fields[field_name] = value_type
        if isinstance(value, dict):
            nested_models[infer_model_name(value)] = extract_fields(value)[0]
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            nested_models[infer_model_name(
                value[0])] = extract_fields(value[0])[0]
    return fields, nested_models
