from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class LinkCreate(BaseModel):
    url: HttpUrl

class LinkResponse(BaseModel):
    original_url: HttpUrl
    code: str
    short_url: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/links", response_model=LinkResponse)
def create_link(data: LinkCreate):
    return {"original_url": data.url, "code": "test123", "short_url": "http://localhost:8000/test123"}