from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
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

@app.get("/{code}")
def redirect(code: str):
    found = links_db.get(code)
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=found,status_code=302)
    