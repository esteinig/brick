"""
bricks/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI main application
│   ├── dependencies.py     # Dependencies, like database connections
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas for request and response
│   ├── crud.py             # CRUD operations (Create, Read, Update, Delete)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/      # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── endpoint1.py
│   │   │   └── endpoint2.py
│   │   └── deps.py         # Dependency injections for endpoints
│   └── core/
│       ├── config.py       # Configuration settings
│       └── celery_app.py   # Celery application setup
"""