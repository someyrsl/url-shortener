from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import secrets, string

app = FastAPI()

class LinkCreate(BaseModel):
    url: HttpUrl

class LinkResponse(BaseModel):
    original_url: HttpUrl
    code: str
    short_url: str

class LinkStats(BaseModel):
    original_url: HttpUrl
    clicks: int

links_db = {}
alphabet = string.ascii_letters + string.digits

def generate_code(length: int = 6) -> str:
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if code not in links_db:
            return code

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/links", response_model=LinkResponse)
def create_link(data: LinkCreate):
    code = generate_code()
    links_db[code] = {"url": str(data.url), "clicks": 0}
    return {"original_url": data.url, "code": code, "short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str):
    found = links_db.get(code)
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    found["clicks"] += 1
    return RedirectResponse(url=found["url"],status_code=302)

@app.get("/links/{code}/stats",response_model=LinkStats)
def get_stats(code: str):
    found = links_db.get(code)
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"original_url": found["url"], "clicks": found["clicks"]}