from fastapi import FastAPI

from .endpoints import files
from .endpoints import sessions
from .endpoints import tasks
from .endpoints import rings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(files.router)
app.include_router(sessions.router)
app.include_router(tasks.router)
app.include_router(rings.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for allowing any domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)