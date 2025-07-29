from jinja2 import Environment, FileSystemLoader


def generate_endpoints(model_name, methods, path):
    """
    Renders FastAPI endpoint functions using a Jinja2 template.

    Args:
        model_name (str): The name of the Pydantic model to use as input.
        methods (list[str]): List of HTTP methods (e.g., ["POST", "GET"]).
        path (str): The route path to register the endpoint under (e.g., "/predict").

    Returns:
        str: Concatenated string of rendered endpoint function definitions.
    """

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("endpoint.j2")
    return "\n\n".join([template.render(
        method=method.lower(),
        path=path,
        function_name=f"{method.lower()}_{model_name.lower()}",
        param_name="data" if method.upper() in ["POST", "PUT"] else "",
        model_name=model_name
    ) for method in methods])
