# AGENTS.md — OpenScript / AI Starter Community: Application Repo

This file is the standing repository contract for Codex runs in this repo.

## 1. Repository identity

- Repo: OpenScript / AI Starter Community — application code
- Local path: /opt/ai-starter-community
- Docs repo (separate): /opt/openscript-site-docs
- Production site: https://openscript.ru
- Default branch: main
- Current branch: design/product-story-03 (feature branch)

## 2. What this repo contains

This repo contains the application source code (source/) and supporting files.
It does NOT contain:
- project documentation (docs live in the docs repo)
- secrets or .env files
- production credentials

## 3. Before any app work

Prove the following before any change:
- git status --short (note all dirty/untracked state)
- git branch --show-current
- git rev-parse HEAD
- git remote -v

## 4. Codex contract

- Do not touch secrets, .env, auth files, tokens, or private credentials.
- Do not delete untracked backup/image/draft files unless the task explicitly requests it.
- No production/runtime/systemd/nginx/service changes unless the task explicitly allows.
- runtime/, state/, logs/, backups/, and tmp/ are NOT source of truth.
- Changes must be minimal, scoped to the task.
- Every change must be committed, pushed, and verified: local HEAD == origin branch HEAD.
- Do not touch /opt/openscript-agent-lab or /opt/openscript-agent-lab-docs unless the task explicitly allows.
