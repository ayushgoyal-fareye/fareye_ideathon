from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from api.data_router import router as data_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(data_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, use specific domains
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"status": "success", "message": "FastAPI is running!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"greeting": f"Hello, {name}!"}

