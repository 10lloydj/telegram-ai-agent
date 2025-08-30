CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS tg_messages (
  chat_id      BIGINT NOT NULL,
  message_id   BIGINT NOT NULL,
  sender_id    BIGINT,
  topic_id     BIGINT,
  topic_title  TEXT,
  posted_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  text         TEXT,
  link         TEXT,
  is_job_post  BOOLEAN,
  is_relevant  BOOLEAN,
  confidence   REAL,
  verdict      JSONB,
  PRIMARY KEY (chat_id, message_id)
);

CREATE INDEX IF NOT EXISTS idx_tg_messages_trgm ON tg_messages USING gin (text gin_trgm_ops);

CREATE TABLE IF NOT EXISTS alerts (
  id           BIGSERIAL PRIMARY KEY,
  chat_id      BIGINT NOT NULL,
  message_id   BIGINT NOT NULL,
  alerted_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  delivered_to TEXT NOT NULL,
  method       TEXT NOT NULL,
  confidence   REAL,
  reasons      JSONB,
  UNIQUE (chat_id, message_id)
);

CREATE TABLE IF NOT EXISTS chat_topics (
  chat_id      BIGINT NOT NULL,
  topic_id     BIGINT NOT NULL,
  title        TEXT,
  PRIMARY KEY (chat_id, topic_id)
);


