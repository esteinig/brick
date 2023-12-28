from fastapi import FastAPI
from .endpoints import upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(upload.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for allowing any domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)