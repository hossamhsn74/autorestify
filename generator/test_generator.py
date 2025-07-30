from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


def generate_test_header():
    """
    Renders the test file header using a Jinja2 template.

    This typically includes:
    - Import statements for FastAPI's TestClient
    - Initialization of the test client with the FastAPI app

    Returns:
        str: The rendered test header code block.
    """
    template = env.get_template("test_header.j2")
    return template.render()


def generate_test_function(model_name, method, path, example_data):
    """
    Renders a test function for a given HTTP method and route using a Jinja2 template.

    Args:
        model_name (str): Name of the input Pydantic model (used for naming).
        method (str): HTTP method to test (e.g., "POST").
        path (str): API route path (e.g., "/example").
        example_data (dict): Dictionary of example field values to use in the test body.

    Returns:
        str: The rendered test function block.
    """
    template = env.get_template("test_func.j2")
    return template.render(
        model_name=model_name,
        method=method,
        path=path,
        example_data=example_data
    )
