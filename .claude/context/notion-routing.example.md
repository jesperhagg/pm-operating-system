# Notion Database Routing Table

_Copy this file to `.claude/context/notion-routing.md` in your consumer repo and fill in your IDs._

---

Workspace: {your-workspace-name}
Last verified: {YYYY-MM-DD}

## Databases

| Logical Name    | Notion Database ID               | Purpose                                       |
|-----------------|----------------------------------|-----------------------------------------------|
| Decisions       | REPLACE_WITH_32_CHAR_HEX_ID      | Product commitments — scope, pricing, kill    |
| Signals         | REPLACE_WITH_32_CHAR_HEX_ID      | Time-stamped observations from world          |
| Knowledge Base  | REPLACE_WITH_32_CHAR_HEX_ID      | Durable synthesized knowledge                 |
| Task Management | REPLACE_WITH_32_CHAR_HEX_ID      | Active backlog and work items                 |

## How to find a database ID

1. Open the database in Notion as a full page (not inline)
2. Click **Share** → **Copy link**
3. The URL looks like:
   `https://notion.so/workspace/Title-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. The ID is the 32-character hex string at the end (strip any hyphens if present)

## Security note

This file contains database IDs, not API tokens. IDs alone do not grant Notion
access — the token is the credential, and it lives in `.mcp.json` (gitignored).

This file is safe to commit. If your org requires stricter enumeration hygiene,
add `.claude/context/notion-routing.md` to your `.gitignore`.
