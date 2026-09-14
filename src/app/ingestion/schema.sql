CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    filename TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_path TEXT,
    sha256 VARCHAR(64),
    status VARCHAR(32) NOT NULL DEFAULT 'indexed',
    indexed_at TIMESTAMPTZ
);

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS source_path TEXT;

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS sha256 VARCHAR(64);

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS status VARCHAR(32) NOT NULL DEFAULT 'indexed';

ALTER TABLE documents
ADD COLUMN IF NOT EXISTS indexed_at TIMESTAMPTZ;

CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_sha256
ON documents(sha256)
WHERE sha256 IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_filename
ON documents(filename);

CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    page_number INTEGER,
    section TEXT,
    metadata JSONB,
    embedding VECTOR(384)
);

CREATE INDEX IF NOT EXISTS chunks_document_id_idx
ON chunks(document_id);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    risk_level VARCHAR(32) NOT NULL DEFAULT 'unknown',
    inherent_risk_score NUMERIC,
    residual_risk_score NUMERIC,
    status VARCHAR(32) NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS risk_assessments_updated_at_idx
ON risk_assessments(updated_at DESC);
