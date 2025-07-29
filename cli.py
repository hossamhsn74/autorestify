import typer
from generator.model_generator import generate_model
from generator.endpoint_generator import generate_endpoints
from generator.route_generator import generate_router
from utils.json_parser import parse_json_file
import os

app = typer.Typer()


@app.command()
def generate(
    json_path: str = typer.Option(..., "--json",
                                  help="Path to the input JSON file"),
    methods: str = typer.Option(..., "--methods",
                                help="Comma-separated HTTP methods"),
    output: str = typer.Option(
        "generated", "--output", help="Output directory")
):
    """
    Generates a complete FastAPI endpoint scaffold from a sample JSON input.

    This command:
    - Parses the input JSON file and infers types (including nested structures)
    - Generates Pydantic models in `schemas/`
    - Creates route functions in `routes/`
    - Creates a central `api_router.py` file to register the endpoint

    Args:
        json_path (str): Path to the input JSON file used to infer model structure.
        methods (str): Comma-separated HTTP methods to generate (e.g., "POST,GET").
        output (str): Directory where the generated code will be saved. Defaults to "generated".

    Example:
        fastapi-gen --json sample.json --methods POST,GET --output my_api
    """
    fields, nested_models = parse_json_file(json_path)

    # Paths
    schemas_path = os.path.join(output, "schemas")
    routes_path = os.path.join(output, "routes")
    os.makedirs(schemas_path, exist_ok=True)
    os.makedirs(routes_path, exist_ok=True)

    # File names
    model_filename = os.path.join(schemas_path, "input_model.py")
    route_filename = os.path.join(routes_path, "input_route.py")
    api_router_filename = os.path.join(output, "api_router.py")

    # Generate files
    model_code = generate_model("InputModel", fields, nested_models)
    with open(model_filename, "w") as f:
        f.write(model_code)

    endpoint_code = generate_endpoints(
        "InputModel", methods.split(","), "/example")
    with open(route_filename, "w") as f:
        f.write(endpoint_code)

    router_code = generate_router("input_route", "Input")
    with open(api_router_filename, "w") as f:
        f.write(router_code)


if __name__ == "__main__":
    app()
