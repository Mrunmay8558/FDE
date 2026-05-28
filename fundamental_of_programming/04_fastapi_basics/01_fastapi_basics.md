# FastAPI Basics

This lesson introduces the basic ideas needed before building APIs with FastAPI.

## 1. What Is FastAPI?

FastAPI is a modern Python web framework used to build APIs.

It helps us create backend applications quickly with:

- simple route creation
- automatic data validation
- automatic API documentation
- good performance
- support for async code

FastAPI is mainly used for:

- backend APIs
- microservices
- internal tools
- AI and ML service backends
- CRUD applications

Simple idea:

- client sends request
- FastAPI receives request
- FastAPI runs Python function
- FastAPI sends response back

## 2. Why FastAPI Is Popular

FastAPI became popular because it is beginner-friendly and also powerful enough for real production systems.

Main reasons:

- syntax is clean and easy to read
- built-in validation reduces bugs
- automatic Swagger documentation is generated
- supports async and await
- works well with Python type hints
- very fast compared to many other Python frameworks

## 3. What Is Starlette?

FastAPI is built on top of Starlette.

Starlette is a lightweight ASGI framework for building web applications and async services in Python.

### What Is ASGI?

ASGI stands for Asynchronous Server Gateway Interface.

It is a standard way for a Python web server and a Python web application to communicate with each other.

Simple idea:

- Uvicorn is the server
- FastAPI or Starlette is the application
- ASGI is the standard that helps them work together

ASGI is important because it supports:

- async and await
- multiple requests at the same time
- WebSockets
- long-running connections

You can think of it like this:

`Client -> Uvicorn -> ASGI -> FastAPI or Starlette`

You can think of it like this:

- Starlette provides the web foundation
- FastAPI adds easier API features on top of it

Starlette handles things like:

- routing
- requests and responses
- middleware
- background tasks
- WebSocket support

So when people use FastAPI, they are also indirectly using Starlette underneath.

## 4. What Is Pydantic?

Pydantic is a Python library used for data validation and data parsing.

FastAPI uses Pydantic heavily.

When a client sends JSON data to a FastAPI endpoint, Pydantic checks whether the data is correct.

For example, if we expect:

- `name` as string
- `price` as float
- `in_stock` as boolean

Pydantic validates the request body and raises an error if the data is wrong.

This is useful because:

- it reduces manual checking
- it gives cleaner code
- it catches bad input early
- it works well with type hints

Example:

```python
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
```

If the incoming data does not match this structure, FastAPI returns a validation error automatically.

## 5. What Is `requirements.txt`?

`requirements.txt` is a file that lists the Python packages needed by a project.

Example:

```txt
fastapi
uvicorn
pydantic
```

Why we use it:

- to share dependencies with other developers
- to install the same packages in another machine
- to keep project setup consistent
- to make deployment easier

Install packages from it:

```bash
pip install -r requirements.txt
```

Create it from installed packages:

```bash
pip freeze > requirements.txt
```

## 6. What Is `venv`?

`venv` means virtual environment.

A virtual environment is an isolated Python environment for one project.

It helps keep project dependencies separate.

Without `venv`, packages installed for one project may affect another project.

Why we use `venv`:

- different projects may need different package versions
- it avoids package conflicts
- it keeps the global Python installation clean
- it makes project setup safer and more organized

## 7. Example Of `venv`

Create a virtual environment:

```bash
python3 -m venv venv
```

Here:

- the first `venv` is the Python module name
- the second `venv` is the folder name we are creating

So this command means:

"Use Python's built-in virtual environment tool and create a new environment inside a folder named `venv`."

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

After activation, install packages inside that environment:

```bash
pip install fastapi uvicorn
```

Deactivate when finished:

```bash
deactivate
```

## 8. First FastAPI Example

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}
```

### What This Code Means

- `FastAPI()` creates the application
- `@app.get("/")` creates a GET route for the home path
- `read_root()` is the function that runs when that route is called
- the returned Python dictionary is automatically converted into JSON

## 9. Running The FastAPI App

If the file name is `main.py`, run:

```bash
uvicorn main:app --reload
```

Meaning:

- `main` is the Python file name
- `app` is the FastAPI object
- `--reload` restarts the server automatically when code changes

After running, open:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

The `/docs` page shows automatic API documentation generated by FastAPI.

## 10. FastAPI, Starlette, And Pydantic Together

These three are connected:

- FastAPI is the main API framework we write code in
- Starlette provides the web and ASGI foundation underneath
- Pydantic validates and parses incoming and outgoing data

Simple view:

`FastAPI -> uses Starlette for web features -> uses Pydantic for validation`

## 11. Basic Project Setup Example

Example project structure:

```text
my_fastapi_project/
|-- venv/
|-- main.py
|-- requirements.txt
```

## 12. Quick Setup Steps

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
pip freeze > requirements.txt
uvicorn main:app --reload
```

## 13. Summary

- FastAPI is a Python framework for building APIs
- Starlette is the web framework underneath FastAPI
- Pydantic is used for validation and type-based data parsing
- `requirements.txt` stores project dependencies
- `venv` creates an isolated environment for the project
- `uvicorn` runs the FastAPI application server

These basics are important before learning:

- path parameters
- query parameters
- request body
- response models
- async route handlers
- CRUD operations
