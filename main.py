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
    links_db[code] = str(data.url)
    return {"original_url": data.url, "code": code, "short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str):
    found = links_db.get(code)
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=found,status_code=302)
