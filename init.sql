CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);