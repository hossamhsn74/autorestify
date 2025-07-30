# Autorestify

This CLI tool helps you **instantly scaffold FastAPI endpoints** from a sample JSON input. It's designed for developers, data scientists, and ML engineers who want to expose models or services quickly — without worrying about boilerplate code or standards.

---

## 🔧 Features

- Converts JSON into typed Pydantic models
- Auto-generates FastAPI route handlers
- Supports multiple HTTP methods (POST, GET, PUT, DELETE, PATCH, or all)
- Handles nested JSON and lists of objects
- Adds clear TODOs so you know *exactly* where to add logic
- Auto-generates test files using `fastapi.testclient` and example input
- Best-practice file structure:
  ```
  generated/
  ├── schemas/         # Pydantic models
  ├── routes/          # Endpoint functions
  ├── tests/           # Test cases for generated endpoints
  └── api_router.py    # Router registration
  ```

---

## 🚀 Quick Start

1. Save your input as a JSON file (e.g. `sample.json`)

2. Run the CLI:
```bash
fastapi-gen --json sample.json --methods POST,GET --output generated
```

3. Your scaffolded code is now in the `generated/` directory. Add your logic where you see `TODO` comments.

4. (Optional) Use the generated `api_router.py` in your main app:
```python
from fastapi import FastAPI
from generated.api_router import api_router

app = FastAPI()
app.include_router(api_router)
```

5. (Optional) Run the generated test file:
```bash
pytest generated/tests/
```

---

## ✅ Example

Input:
```json
{
  "feature1": 3.14,
  "feature2": "cat"
}
```

Output:
- `schemas/input_model.py`: defines `feature1: float`, `feature2: str`
- `routes/input_route.py`: creates a route like `@router.post("/example")`
- `tests/test_input_route.py`: includes test cases for each generated method

---

## 👨‍💻 For ML Engineers

Use this to expose your model via an API in seconds:
- Get your model's input as JSON
- Run this tool
- Drop in your inference logic

Done!

---

## 🧠 Coming Soon

- YAML schema input support
- Example response generation
- Interactive mode

---

MIT License © 2025