from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class LinkCreate(BaseModel):
    url: HttpUrl

class LinkResponse(BaseModel):
    original_url: HttpUrl
    code: str
    short_url: str

links_db = {}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/links", response_model=LinkResponse)
def create_link(data: LinkCreate):
    code = "test123"
    links_db[code] = str(data.url)
    return {"original_url": data.url, "code": "test123", "short_url": f"http://localhost:8000/{code}"}