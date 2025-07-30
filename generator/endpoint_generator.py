from jinja2 import Environment, FileSystemLoader


def generate_endpoint_header(model_name):
    """
    Renders the import and router initialization block for a FastAPI route file.

    This includes:
    - Importing the FastAPI `APIRouter`
    - Importing the generated Pydantic model
    - Instantiating the `router` object

    Args:
        model_name (str): The name of the Pydantic model used in route functions.

    Returns:
        str: The rendered header block for a FastAPI route file.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("endpoint_header.j2")
    return template.render(model_name=model_name)


def generate_endpoint_function(model_name, method, path):
    """
    Renders a single FastAPI route function using a Jinja2 template.

    Args:
        model_name (str): Name of the Pydantic model used as the request body (if applicable).
        method (str): HTTP method for the endpoint (e.g., "POST", "GET").
        path (str): The API route path (e.g., "/example").

    Returns:
        str: The rendered route function block with proper annotations and TODO comment.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("endpoint_func.j2")
    return template.render(
        method=method.lower(),
        path=path,
        function_name=f"{method.lower()}_{model_name.lower()}",
        param_name="data" if method.upper() in ["POST", "PUT"] else "",
        model_name=model_name
    )
