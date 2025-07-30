import typer
import os
from generator.model_generator import generate_model
from generator.route_generator import generate_router
from generator.endpoint_generator import generate_endpoint_header, generate_endpoint_function
from generator.test_generator import generate_test_header, generate_test_function
from utils.json_parser import parse_json_file

app = typer.Typer()


@app.command()
def generate(
    json_path: str = typer.Option(..., "--json", help="Path to the input JSON file"),
    methods: str = typer.Option(..., "--methods", help="Comma-separated HTTP methods or 'all'"),
    output: str = typer.Option("generated", "--output", help="Output directory")
):
    """
    Generates a complete FastAPI endpoint scaffold from a sample JSON input.

    This command:
    - Parses the input JSON file and infers types (including nested structures)
    - Generates Pydantic models in `schemas/`
    - Creates route functions in `routes/`
    - Creates test cases in `tests/`
    - Creates a central `api_router.py` to register the router

    Args:
        json_path (str): Path to the input JSON file used to infer model structure.
        methods (str): Comma-separated HTTP methods to generate (e.g., "POST,GET") or "all".
        output (str): Directory where the generated code will be saved. Defaults to "generated".

    Example:
        fastapi-gen --json sample.json --methods all --output my_api
    """
    fields, nested_models = parse_json_file(json_path)

    if methods.lower() == "all":
        method_list = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    else:
        method_list = [m.strip().upper() for m in methods.split(",")]

    # Paths
    schemas_path = os.path.join(output, "schemas")
    routes_path = os.path.join(output, "routes")
    tests_path = os.path.join(output, "tests")
    os.makedirs(schemas_path, exist_ok=True)
    os.makedirs(routes_path, exist_ok=True)
    os.makedirs(tests_path, exist_ok=True)

    # File names
    model_filename = os.path.join(schemas_path, "input_model.py")
    route_file_path = os.path.join(routes_path, "input_route.py")
    test_file_path = os.path.join(tests_path, "test_input_route.py")
    api_router_filename = os.path.join(output, "api_router.py")

    # Generate Pydantic model
    model_code = generate_model("InputModel", fields, nested_models)
    with open(model_filename, "w") as f:
        f.write(model_code)

    # Generate route header
    with open(route_file_path, "w") as f:
        f.write(generate_endpoint_header("InputModel"))
        f.write("\n\n")

    # Generate route functions
    for method in method_list:
        func_code = generate_endpoint_function("InputModel", method, "/example")
        with open(route_file_path, "a") as f:
            f.write(func_code)
            f.write("\n\n")

    # Generate API router
    router_code = generate_router("input_route", "Input")
    with open(api_router_filename, "w") as f:
        f.write(router_code)

    # Generate tests
    example_data = {
        field: '"example"' if "str" in ftype else 0 if "int" in ftype else True
        for field, ftype in fields.items()
    }

    with open(test_file_path, "w") as f:
        f.write(generate_test_header())
        f.write("\n\n")

    for method in method_list:
        test_func = generate_test_function("InputModel", method, "/example", example_data)
        with open(test_file_path, "a") as f:
            f.write(test_func)
            f.write("\n\n")


if __name__ == "__main__":
    app()
