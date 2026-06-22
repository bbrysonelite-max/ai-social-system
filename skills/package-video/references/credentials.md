# Credentials map

**Golden rule:** reference every key BY NAME only. Never print, echo, paste, log,
or quote a key VALUE — not in chat, output, commits, or PRs. Reading a key into a
variable to use it is fine; surfacing the value is not. Verify keys by HTTP status
code only (`-o /dev/null -w '%{http_code}'`).

`~/Desktop/GitSync/` is Brent's standard secret store. Files there: `kloop.env`,
`BRENT_CREDENTIALS.md`, `Cal.com.txt`, `gmail_app_password_tigerclaw`,
`Synthtic Tenant.txt`.

## HeyGen API key — USE kloop.env

- **Live keys:** `~/Desktop/GitSync/kloop.env`, on the lines that read
  `1.  HEYGEN_API_KEY=…` and `2.  HEYGEN_API_KEY=…`.
- **Gotcha:** the `1.` / `2.` numbered-list prefix means a plain `source kloop.env`
  does **not** pick these up (they're not clean shell assignments). Extract with sed:

  ```bash
  KEY=$(grep -m1 'HEYGEN_API_KEY=' ~/Desktop/GitSync/kloop.env \
        | sed -E 's/.*HEYGEN_API_KEY=//' | tr -d '[:space:]"')
  ```

- Both kloop.env keys were verified live (HTTP 200 on
  `GET https://api.heygen.com/v2/user/remaining_quota`) on 2026-06-22.
- **STALE — do not use:** the keys in `~/Desktop/GitSync/BRENT_CREDENTIALS.md`
  (`HEY_GEN_API_KEY=` and the "API Key (v2)" line) both return **401**. They are an
  old key; ignore them.
- **Auth the CLI** (`~/.local/bin/heygen`): `printf '%s' "$KEY" | heygen auth login`
  (saves to `~/.heygen/credentials`). Then `heygen video list --human`,
  `heygen video get <id>` → `.data.video_url`.
- **Quick live check** (status only, value masked):

  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' -H "X-Api-Key: $KEY" \
    https://api.heygen.com/v2/user/remaining_quota
  ```

## Blotato API key

- `~/.claude.json` at path `.mcpServers.blotato.headers["blotato-api-key"]`
  (also surfaced in GitSync). Used by `blotato-post`/`cadence`, not by this skill
  directly — listed here for completeness.

## If a key is missing or returns 401

Say so plainly and ask Brent for the current key (he can `! heygen auth login` in
the prompt, or drop a fresh value into `kloop.env`). Do not guess, and do not fall
back to a vertical clip or a fabricated transcript just to keep moving.
