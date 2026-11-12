# URL Shortener

A simple URL shortening service built with FastAPI and PostgreSQL. It turns a long link into a short code, redirects visitors to the original URL, and counts clicks.

## Features

- Create a short link from any `http`/`https` URL
- Redirect by short code (`302`)
- Click counter and stats per link
- Random 6-character codes with collision check
- Input validation with Pydantic
- Automated tests (pytest)
- One-command startup with Docker Compose

## Tech stack

- Python 3.12
- FastAPI, Uvicorn
- PostgreSQL 16
- SQLAlchemy, psycopg2
- pytest, httpx
- Docker, Docker Compose

## Quick start (Docker Compose)

Requires Docker Desktop (or Docker Engine) to be running.

```bash
git clone https://github.com/someyrsl/url-shortener.git
cd url-shortener
cp .env.example .env
docker compose up --build
```

The API is available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

The database table is created automatically from `init.sql` on the first start. Data is stored in the `pgdata` Docker volume and survives restarts.

Useful commands:

```bash
docker compose up -d      # run in the background
docker compose logs api   # API logs
docker compose down       # stop containers (data is kept)
docker compose down -v    # stop and delete the database volume
```

## Local development (without Docker for the API)

Run only PostgreSQL in Docker and the API on your machine.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d db
uvicorn main:app --reload
```

For this mode `DATABASE_URL` in `.env` must point to `localhost`, and the `db` service must expose port `5432` (add a `ports` section to it in `docker-compose.yml`).

## Configuration

Environment variables (see `.env.example`):

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `DATABASE_URL` | SQLAlchemy connection string (used when running the API locally) |

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

Unknown codes return `404`, invalid URLs return `422`.

## Tests

```bash
pytest -v
```

Tests run against an in-memory SQLite database, so PostgreSQL is not required.

## Project structure

```
.
├── main.py              # FastAPI app and endpoints
├── database.py          # Engine, session, Base
├── models.py            # SQLAlchemy models
├── conftest.py          # pytest fixtures
├── test_links.py        # API tests
├── init.sql             # Table creation for a fresh database
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Roadmap

- [x] Basic API: create, redirect, stats
- [x] PostgreSQL via SQLAlchemy
- [x] Tests (pytest)
- [x] Docker Compose setup
- [ ] Custom aliases
- [ ] Link expiration (`410 Gone`)
- [ ] Database migrations (Alembic)
- [ ] Rate limiting