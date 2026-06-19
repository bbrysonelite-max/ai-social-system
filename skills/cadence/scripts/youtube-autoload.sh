#!/usr/bin/env bash
# youtube-autoload.sh — publish a video to YouTube via Blotato, PRIVATE-first for review.
#
# Brent's rule: he never uploads manually again. This pushes a video straight to
# the channel as PRIVATE (only he can see it) so his only job is a morning "make
# it public". Use --schedule to stage it as Scheduled (private until the date,
# then auto-public).
#
# Usage:
#   youtube-autoload.sh --video <PUBLIC_URL> --title "<title>" --desc-file <path> \
#       [--privacy private|public|unlisted] [--schedule <ISO8601-UTC>]
#
#   --video       PUBLIC URL of the video. Blotato's /v2/media fetches it; there is
#                 NO REST upload for raw local files (confirmed against Blotato docs).
#                 Daily HeyGen renders already have public URLs — pass those.
#                 For a local-only file, host it first (or use the in-session MCP
#                 presigned uploader) and pass the resulting URL.
#   --title       YouTube video title (required).
#   --desc-file   Path to a text file holding the description (preferred), OR use --desc.
#   --desc        Inline description string.
#   --privacy     Default: private. (Brent reviews, then flips public.)
#   --schedule    Optional ISO-8601 UTC; stages as Scheduled (private until then).
#
# Reads the Blotato key from ~/.claude.json. NEVER prints the key.
set -euo pipefail

API="https://backend.blotato.com/v2"
ACCOUNT_ID="27755"   # YouTube @BrentBrysonaios. Re-verify via GET /users/me/accounts if reconnected.
PRIVACY="private"; SCHEDULE=""; VIDEO=""; TITLE=""; DESCFILE=""; DESC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --video) VIDEO="$2"; shift 2;;
    --title) TITLE="$2"; shift 2;;
    --desc-file) DESCFILE="$2"; shift 2;;
    --desc) DESC="$2"; shift 2;;
    --privacy) PRIVACY="$2"; shift 2;;
    --schedule) SCHEDULE="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$VIDEO" ] || { echo "ERROR: --video <PUBLIC_URL> required" >&2; exit 2; }
[ -n "$TITLE" ] || { echo "ERROR: --title required" >&2; exit 2; }
[ -n "$DESCFILE" ] && DESC="$(cat "$DESCFILE")"

case "$VIDEO" in
  http://*|https://*) : ;;
  *) echo "ERROR: --video must be a PUBLIC URL. Blotato has no REST upload for local files." >&2
     echo "       Host the file first (or use the in-session MCP presigned uploader), then pass its URL." >&2
     exit 3;;
esac

KEY=$(python3 -c "import json;print(json.load(open('$HOME/.claude.json'))['mcpServers']['blotato']['headers']['blotato-api-key'])")

echo "1/3  Hosting video on Blotato (POST /media)…"
MEDIA_URL=$(curl -s -X POST -H "blotato-api-key: $KEY" -H "Content-Type: application/json" \
  -d "{\"url\":\"$VIDEO\"}" "$API/media" | python3 -c "import sys,json;print(json.load(sys.stdin)['url'])")
echo "     hosted ✓"

echo "2/3  Creating YouTube post (privacy=$PRIVACY${SCHEDULE:+, scheduled=$SCHEDULE})…"
PAYLOAD=$(python3 - "$ACCOUNT_ID" "$MEDIA_URL" "$TITLE" "$DESC" "$PRIVACY" "$SCHEDULE" <<'PY'
import json,sys
acct,media,title,desc,priv,sched=sys.argv[1:7]
body={"post":{"accountId":acct,
  "content":{"text":desc,"mediaUrls":[media],"platform":"youtube"},
  "target":{"targetType":"youtube","title":title,"privacyStatus":priv,"shouldNotifySubscribers":False}}}
if sched: body["scheduledTime"]=sched
print(json.dumps(body))
PY
)
PID=$(curl -s -X POST -H "blotato-api-key: $KEY" -H "Content-Type: application/json" \
  -d "$PAYLOAD" "$API/posts" | python3 -c "import sys,json;print(json.load(sys.stdin)['postSubmissionId'])")
echo "     submission ✓ ($PID)"

echo "3/3  Polling for result…"
for i in $(seq 1 30); do
  RESP=$(curl -s -H "blotato-api-key: $KEY" "$API/posts/$PID")
  ST=$(echo "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('status',''))")
  case "$ST" in
    published)
      URL=$(echo "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('publicUrl',''))")
      echo "✅ DONE — $PRIVACY on YouTube: $URL"
      echo "   Review it, then flip to Public when you're happy."
      exit 0;;
    scheduled)
      echo "🕒 SCHEDULED (private until $SCHEDULE, then auto-public). It's in the review queue."
      exit 0;;
    failed)
      echo "❌ FAILED: $(echo "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('errorMessage',''))")"
      exit 1;;
  esac
  sleep 10
done
echo "⏳ Still processing after 5 min — check later: GET $API/posts/$PID"
exit 0
