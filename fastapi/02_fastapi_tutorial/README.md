# FastAPI Tutorial 02 — Production Codebase Structure

This tutorial teaches how to structure a **real-world FastAPI project** with MongoDB.  
We use the same architecture used in production backends — layered, modular, and testable.

---

## What You Will Learn

- How to organise a FastAPI project into clean, scalable layers
- How to connect FastAPI to MongoDB using **Motor** (async) and **ODMantic** (ODM)
- How to write a **logger** that writes to `logs/debug.log`
- How to use **JWT** for authentication without third-party auth services
- How to send **async emails** via Gmail SMTP using `aiosmtplib`
- How to separate **router → controller → CRUD** responsibilities
- How to manage app **startup / shutdown** with FastAPI's `lifespan`

---

## Folder Structure

```
02_fastapi_tutorial/
│
├── main.py                          ← Entry point: runs uvicorn
├── requirements.txt                 ← All dependencies
├── .env.example                     ← Environment variable template
│
├── commons/                         ← Shared utilities (used everywhere)
│   ├── __init__.py
│   ├── logger.py                    ← Logger factory → writes to logs/debug.log
│   └── auth.py                      ← JWT sign/decode, bcrypt password helpers
│
├── core/                            ← Application core
│   ├── __init__.py                  ← Exposes logger via `from core import logger`
│   │
│   ├── apis/                        ← HTTP layer (routers + schemas)
│   │   ├── api.py                   ← FastAPI app factory, middleware, lifespan
│   │   ├── routes/
│   │   │   └── user_router.py       ← Route definitions (thin — just call controller)
│   │   └── schemas/
│   │       ├── requests/
│   │       │   └── user_request.py  ← Pydantic request schemas (validate input)
│   │       └── responses/
│   │           └── user_responses.py← Pydantic response schemas (shape output)
│   │
│   ├── controllers/                 ← Business logic layer
│   │   └── user_controller.py       ← All user business rules live here
│   │
│   ├── cruds/                       ← Database access layer (no business logic here)
│   │   ├── base.py                  ← Generic CRUD: get, get_all, create, update, delete
│   │   └── user_crud.py             ← User-specific queries (get_by_email, etc.)
│   │
│   ├── database/                    ← MongoDB connection management
│   │   ├── base_class.py            ← `Base = odmantic.Model` (all models inherit this)
│   │   └── database.py              ← Singleton client, connect/disconnect, get_engine()
│   │
│   ├── models/                      ← ODMantic document models (MongoDB schema)
│   │   └── user_model.py            ← User document with enums, fields, timestamps
│   │
│   └── utils/                       ← Feature utilities
│       └── email/
│           ├── email_helper.py      ← Async send_email() via Gmail SMTP
│           └── email_template_generator.py ← HTML + plain-text email builders
│
└── logs/                            ← Auto-created; .gitignore this folder
    └── debug.log                    ← Written by logger.py
```

---

## Layered Architecture (The Most Important Concept)

```
HTTP Request
     │
     ▼
┌─────────────────────────────────────────────────┐
│  ROUTER  (user_router.py)                       │
│  - Declares HTTP method + path                  │
│  - Validates request body via Pydantic schema   │
│  - Calls Controller                             │
│  - Returns result (serialised by response_model)│
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  CONTROLLER  (user_controller.py)               │
│  - Contains ALL business logic                  │
│  - Validates uniqueness, hashes passwords, etc. │
│  - Calls CRUD for DB operations                 │
│  - Calls utilities (email sending, etc.)        │
│  - Raises HTTPException on errors               │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  CRUD  (user_crud.py → base.py)                 │
│  - Only talks to the database                   │
│  - No business logic — just queries             │
│  - CRUDBase provides generic operations         │
│  - CRUDUser adds user-specific queries          │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  MODEL  (user_model.py)                         │
│  - Defines the MongoDB document structure       │
│  - ODMantic maps it to a "users" collection     │
└─────────────────────────────────────────────────┘
```

**Why layers?**

- Each layer has **one responsibility** — easy to understand, change, and test
- Business rules live in ONE place (controller), not scattered across routes
- You can swap MongoDB for PostgreSQL by only changing the CRUD layer

---

## Key Files Explained

### `commons/logger.py`

Every module in the project creates its own logger:

```python
from core import logger
logging = logger(__name__)
logging.info("User created")
```

All logs go to `logs/debug.log` with a timestamp, module name, and PID.

---

### `core/database/database.py`

Uses a **Singleton** pattern:

- One MongoDB connection pool is created on startup
- All requests share it — efficient and safe
- `get_database()` is a FastAPI dependency that injects the engine into routes

```python
@router.post("/v1/auth/register")
async def register(request: UserCreate, db: AIOEngine = Depends(get_database)):
    ...
```

---

### `core/cruds/base.py`

Generic CRUD using Python generics:

```python
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)
```

`CRUDBase` gives you `get`, `get_all`, `create`, `update`, `delete` for free.  
`CRUDUser` only adds what is user-specific (`get_by_email`, etc.).

---

### `core/apis/api.py`

The **lifespan** context manager replaces old `@app.on_event("startup")`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()   # runs on startup
    yield
    await close_mongo_connection()  # runs on shutdown
```

Add every new router with `app.include_router(...)`.

---

## Setup & Run

```bash
# 1. Clone / navigate to this folder
cd fastapi/02_fastapi_tutorial

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env: add MongoDB URI, JWT secret, Gmail credentials

# 5. Start MongoDB (if running locally)
# brew services start mongodb-community   ← macOS
# OR use MongoDB Atlas (cloud)

# 6. Run the server
python main.py
# OR
uvicorn core.apis.api:app --reload --port 8000
```

Open **http://localhost:8000/docs** for the interactive Swagger UI (only in LOCAL/DEVELOPMENT).

---

## API Endpoints

| Method | Path                | Description                             |
| ------ | ------------------- | --------------------------------------- |
| `POST` | `/v1/auth/register` | Register a new user                     |
| `POST` | `/v1/auth/login`    | Login with email + password             |
| `GET`  | `/v1/auth/me`       | Get current user profile (JWT required) |
| `GET`  | `/health`           | Liveness check                          |

### Register example

```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com"}'
```

### Login example

```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"<password from email>"}'
```

### Get profile (protected)

```bash
curl http://localhost:8000/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## Adding a New Feature

Follow this checklist every time you add a new resource (e.g., `Product`):

1. **Model** → `core/models/product_model.py` — ODMantic document fields
2. **Request schema** → `core/apis/schemas/requests/product_request.py`
3. **Response schema** → `core/apis/schemas/responses/product_responses.py`
4. **CRUD** → `core/cruds/product_crud.py` — extends `CRUDBase[Product, ...]`
5. **Controller** → `core/controllers/product_controller.py` — business logic
6. **Router** → `core/apis/routes/product_router.py` — route definitions
7. **Register router** → Add `app.include_router(product_router)` in `core/apis/api.py`

That's the complete cycle.

---

## Email System

Email is sent asynchronously using `aiosmtplib` (Gmail SMTP):

```
UserController.create_user()
    └──▶ email_template_generator.welcome_email_with_credentials()  → {subject, text, html}
    └──▶ email_helper.send_email(subject, to, text, html)           → sends via SMTP
```

To add a new email type:

1. Add a new function in `email_template_generator.py` returning `{subject, text, html}`
2. Call `send_email(...)` from the controller with those values

---

## Environment Variables Reference

| Variable             | Required        | Description                                           |
| -------------------- | --------------- | ----------------------------------------------------- |
| `MONGODB_URL`        | Yes             | Single MongoDB connection string used by the tutorial |
| `DATABASE_NAME`      | Yes             | MongoDB database name                                 |
| `secret`             | Yes             | JWT signing secret (keep this private)                |
| `algorithm`          | No              | JWT algorithm (default `HS256`)                       |
| `gmail_user`         | Yes (for email) | Gmail address                                         |
| `gmail_app_password` | Yes (for email) | Gmail App Password (not your login password)          |
| `company_name`       | No              | Used in email templates                               |
| `support_email`      | No              | Shown in email footer                                 |
| `logo_url`           | No              | Logo shown in email header                            |
