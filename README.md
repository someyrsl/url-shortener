# URL Shortener

A simple URL shortening service built with FastAPI and PostgreSQL. It turns a long link into a short code, redirects visitors to the original URL, and counts clicks.

## Features

- Create a short link from any `http`/`https` URL
- Redirect by short code (`302`)
- Click counter and stats per link
- Random 6-character codes with collision check
- Input validation with Pydantic

## Tech stack

- Python 3.11+
- FastAPI, Uvicorn
- PostgreSQL 16 (Docker)
- SQLAlchemy, psycopg2
- python-dotenv

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/someyrsl/url-shortener.git
cd url-shortener
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
docker run -d --name urlshortener-db \
  -e POSTGRES_USER=app \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=urlshortener \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

### 3. Create the table

```bash
docker exec -it urlshortener-db psql -U app -d urlshortener
```

```sql
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Configure environment

Copy `.env.example` to `.env` and adjust if needed:

```bash
cp .env.example .env
```

```
DATABASE_URL=postgresql+psycopg2://app:password@localhost:5432/urlshortener
```

Make sure the password matches the one used in step 2.

### 5. Run

```bash
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/links` | Create a short link |
| GET | `/{code}` | Redirect to the original URL |
| GET | `/links/{code}/stats` | Original URL and click count |

### Examples

Create a link:

```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path"}'
```

```json
{
  "original_url": "https://example.com/very/long/path",
  "code": "aB3xK9",
  "short_url": "http://localhost:8000/aB3xK9"
}
```

Get stats:

```bash
curl http://localhost:8000/links/aB3xK9/stats
```

```json
{
  "original_url": "https://example.com/very/long/path",
  "clicks": 3
}
```

Unknown codes return `404`.

## Project structure

```
.
├── main.py          # FastAPI app and endpoints
├── database.py      # Engine, session, Base
├── models.py        # SQLAlchemy models
├── requirements.txt
├── .env.example
└── README.md
```

## Roadmap

- [ ] Custom aliases
- [ ] Link expiration (`410 Gone`)
- [ ] Redis cache for popular links
- [ ] Rate limiting
- [ ] Tests (pytest)
- [ ] Docker Compose setup
