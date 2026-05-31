#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# OpenScript / AI Starter Community — Staging startup script
#
# This script starts the application in isolated staging mode.
# It uses env.staging.example for defaults with explict local-only overrides.
#
# Safety:
#   - Binds to 127.0.0.1 only (localhost)
#   - Uses port 8090 (non-default, avoids production collision)
#   - Uses isolated SQLite database under staging/data/
#   - Never reads production .env
#   - Fails if port 8090 is already in use
# =============================================================================

STAGING_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$STAGING_DIR/.." && pwd)"

export APP_ENV="${APP_ENV:-staging}"
export APP_HOST="${APP_HOST:-127.0.0.1}"
export APP_PORT="${APP_PORT:-8090}"
export BASE_URL="${BASE_URL:-http://127.0.0.1:8090}"
export DATABASE_PATH="${DATABASE_PATH:-$STAGING_DIR/data/ai_starter_community.sqlite3}"
export SESSION_COOKIE_NAME="${SESSION_COOKIE_NAME:-ai_starter_community_staging_session}"
export SESSION_COOKIE_SECURE="${SESSION_COOKIE_SECURE:-false}"
export EMAIL_MODE="${EMAIL_MODE:-outbox}"
export EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS="${EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS:-24}"
export PASSWORD_RESET_TOKEN_EXPIRY_MINUTES="${PASSWORD_RESET_TOKEN_EXPIRY_MINUTES:-30}"

# Source optional env.staging.example for non-sensitive overrides
ENV_EXAMPLE="$STAGING_DIR/env.staging.example"
if [ -f "$ENV_EXAMPLE" ]; then
  set -a
  source "$ENV_EXAMPLE"
  set +a
fi

# Ensure staging data directory exists
mkdir -p "$STAGING_DIR/data"

# Verify port 8090 is free
if command -v ss &>/dev/null; then
  if ss -tln "sport = :$APP_PORT" 2>/dev/null | grep -q ":$APP_PORT"; then
    echo "ERROR: Port $APP_PORT is already in use. Is staging already running?" >&2
    exit 1
  fi
elif command -v lsof &>/dev/null; then
  if lsof -iTCP:"$APP_PORT" -sTCP:LISTEN 2>/dev/null | grep -q .; then
    echo "ERROR: Port $APP_PORT is already in use. Is staging already running?" >&2
    exit 1
  fi
fi

# Use project virtual environment if it exists
VENV_PYTHON="$APP_ROOT/source/.venv/bin/python"
PYTHON_BIN="${PYTHON:-}"
if [ -z "$PYTHON_BIN" ] && [ -x "$VENV_PYTHON" ]; then
  PYTHON_BIN="$VENV_PYTHON"
elif [ -z "$PYTHON_BIN" ]; then
  PYTHON_BIN="python"
fi

cd "$APP_ROOT/source"

echo "=========================================="
echo " OpenScript / AI Starter Community"
echo " Staging environment"
echo "------------------------------------------"
echo " APP_ENV:       $APP_ENV"
echo " Bind:          $APP_HOST:$APP_PORT"
echo " Base URL:      $BASE_URL"
echo " Database:      $DATABASE_PATH"
echo " Session:       $SESSION_COOKIE_NAME"
echo " Email mode:    $EMAIL_MODE"
echo " Python:        $PYTHON_BIN"
echo "------------------------------------------"
echo " Press Ctrl+C to stop."
echo "=========================================="

exec "$PYTHON_BIN" -m uvicorn app.main:app \
  --host "$APP_HOST" \
  --port "$APP_PORT" \
  --log-level info
