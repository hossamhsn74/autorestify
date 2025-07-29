from jinja2 import Environment, FileSystemLoader


def generate_model(model_name, fields, nested_models=None):
    """
    Generates a Pydantic model (and nested sub-models if needed) using a Jinja2 template.

    Args:
        model_name (str): The name of the root Pydantic model.
        fields (dict): Dictionary of field names and their inferred types.
        nested_models (dict, optional): Dictionary of nested model names and their fields.

    Returns:
        str: Rendered Python code for the main and nested Pydantic models.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("model.j2")
    return template.render(
        model_name=model_name,
        fields=fields,
        nested_models=nested_models or {}
    )
