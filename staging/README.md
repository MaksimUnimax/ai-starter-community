# Staging environment — OpenScript / AI Starter Community

## Purpose

This is the isolated local staging/test environment for design experiments,
Kilo workflow runs, and safe app testing without touching production.

## Safety rules

- Staging is LOCALHOST-ONLY (127.0.0.1:8090).
- Staging uses its OWN SQLite database (staging/data/ai_starter_community.sqlite3).
- Staging does NOT access production state/, runtime/, .env, or secrets.
- Staging does NOT use production SMTP credentials.
- Staging data is gitignored and can be deleted at any time.
- Staging is for design/Kilo experiments only — no production use.

## How to start

```bash
cd /opt/ai-starter-community
bash staging/start.sh
```

This starts uvicorn on http://127.0.0.1:8090.

## How to stop

Press Ctrl+C in the terminal where start.sh is running.

## Rollback

Delete staging runtime and data files (gitignored):

```bash
rm -rf staging/data/*
rm -rf staging/runtime/*
```

The staging scripts and README remain committed in git for the next use.
Any source changes made during design work must be committed separately.

## Execution policy

- **Strict rules (never violated):**
  - Do NOT daemonize staging.
  - Do NOT connect staging to systemd or nginx.
  - Do NOT expose staging publicly (127.0.0.1 only).
  - Do NOT use production .env, secrets, state/, runtime/, or logs/.
  - Do NOT use production SMTP credentials (email_mode=outbox).
  - Staging data is gitignored and ephemeral.

- **Bounded root execution allowed:**
  Bounded short-lived root execution is allowed only for local health proof
  if ALL of these are true:
  - APP_HOST=127.0.0.1
  - APP_PORT=8090
  - DATABASE_PATH points to staging/data/ai_starter_community.sqlite3
  - EMAIL_MODE=outbox
  - SESSION_COOKIE_NAME is staging-specific
  - Process runs in foreground only (no daemon)
  - Process is stopped after /healthz and /readyz checks
  - No production files are touched

- No production data is ever written to staging paths.
- No public ports are exposed.
- Agent Lab repos are NOT touched by staging operations.
