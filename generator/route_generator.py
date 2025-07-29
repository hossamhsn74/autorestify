from jinja2 import Environment, FileSystemLoader


def generate_router(route_file: str, tag: str):
    """
    Generates a central API router registration file using a Jinja2 template.

    Args:
        route_file (str): Name of the route module to import and register.
        tag (str): Swagger tag used to group the endpoints under in the OpenAPI docs.

    Returns:
        str: Rendered Python code for the API router that includes the specified route module.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("router.j2")
    return template.render(route_file=route_file, tag=tag)
