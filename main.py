from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
import secrets, string
from database import get_db
from models import Link

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

alphabet = string.ascii_letters + string.digits

def generate_code(db: Session, length: int = 6) -> str:
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        existing = db.query(Link).filter(Link.code == code).first()
        if not existing:
            return code

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/links", response_model=LinkResponse)
def create_link(data: LinkCreate, db: Session = Depends(get_db)):
    code = generate_code(db)
    link = Link(code=code, original_url=str(data.url))
    db.add(link)
    db.commit()
    return {"original_url": data.url, "code": code, "short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    found = db.query(Link).filter(Link.code == code).first()
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    found.clicks += 1
    db.commit()
    return RedirectResponse(url=found.original_url,status_code=302)

@app.get("/links/{code}/stats",response_model=LinkStats)
def get_stats(code: str, db: Session = Depends(get_db)):
    found = db.query(Link).filter(Link.code == code).first()
    if not found:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"original_url": found.original_url, "clicks": found.clicks}