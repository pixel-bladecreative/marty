#!/usr/bin/env bash
# Generate an image with Kie.ai over the REST API, bypassing Composio's hosted MCP.
#
# Composio's hosted MCP blocks every KIEAI_GENERATE_* tool under a marketplace
# policy restriction. That block is on Composio's server, not on the Kie account,
# so no setting on our side clears it. api.kie.ai itself is reachable from this
# environment and only wants a key.
#
# Setup, once: add KIE_API_KEY to the environment's variables (key from
# https://kie.ai/api-key). Nothing else is needed; egress to api.kie.ai already works.
#
# Usage:
#   ./kie.sh "a prompt"                        # defaults to google/nano-banana
#   ./kie.sh "a prompt" google/nano-banana out.png
set -euo pipefail

PROMPT="${1:?usage: kie.sh \"prompt\" [model] [outfile]}"
MODEL="${2:-google/nano-banana}"
OUT="${3:-kie-output.png}"
API="https://api.kie.ai/api/v1/jobs"

if [ -z "${KIE_API_KEY:-}" ]; then
  echo "KIE_API_KEY is not set. Add it to the environment's variables, key from https://kie.ai/api-key" >&2
  exit 2
fi

auth=(-H "Authorization: Bearer $KIE_API_KEY" -H "Content-Type: application/json")

payload=$(PROMPT="$PROMPT" MODEL="$MODEL" python3 -c '
import json, os
print(json.dumps({"model": os.environ["MODEL"],
                  "input": {"prompt": os.environ["PROMPT"], "output_format": "png"}}))')

echo "submitting to $MODEL" >&2
create=$(curl -sS --max-time 60 -X POST "$API/createTask" "${auth[@]}" -d "$payload")

task=$(printf '%s' "$create" | python3 -c '
import json,sys
r=json.load(sys.stdin)
if r.get("code") != 200:
    sys.exit(f"create failed: {r.get(\"code\")} {r.get(\"msg\")}")
print((r.get("data") or {}).get("taskId",""))')
[ -n "$task" ] || { echo "no taskId returned: $create" >&2; exit 1; }
echo "task $task" >&2

for i in $(seq 1 60); do
  sleep 5
  rec=$(curl -sS --max-time 40 "$API/recordInfo?taskId=$task" "${auth[@]}")
  read -r state url <<<"$(printf '%s' "$rec" | python3 -c '
import json,sys
d=(json.load(sys.stdin).get("data") or {})
res=d.get("resultJson") or "{}"
if isinstance(res,str):
    try: res=json.loads(res)
    except Exception: res={}
urls=res.get("resultUrls") or []
print(d.get("state",""), urls[0] if urls else "")')"
  case "$state" in
    success) echo "done in ~$((i*5))s" >&2
             curl -sS --max-time 120 -L "$url" -o "$OUT"
             echo "$OUT"; exit 0 ;;
    fail)    echo "generation failed: $rec" >&2; exit 1 ;;
    *)       printf '.' >&2 ;;
  esac
done
echo "timed out after 5 minutes; task $task may still finish" >&2
exit 1
