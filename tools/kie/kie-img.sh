#!/usr/bin/env bash
# Generate or edit an image on Kie.ai with reference image inputs.
#
# Companion to kie.sh (plain text-to-image). This one uploads local reference
# files through Kie's base64 file-upload API (files live ~3 days, ample for a
# working session) and passes them to the model. The input key differs by
# model family: gpt-image-2-* wants `input_urls`, everything else observed
# (nano-banana-edit, seedream i2i) wants `image_urls`.
#
# Usage:
#   ./kie-img.sh "prompt" MODEL OUT.png REF1 [REF2 ...]
#   REFs may be local paths (auto-uploaded) or https URLs (passed through).
#   ASPECT_RATIO=16:9 ./kie-img.sh ...   # optional, model-dependent
#
# Verified models (docs.kie.ai/market):
#   google/nano-banana            text-to-image
#   google/nano-banana-edit       image edit, multi-reference
#   gpt-image-2-text-to-image     text-to-image (tutorial's sheet tool)
#   gpt-image-2-image-to-image    image edit, multi-reference
#   bytedance/seedance-2-5        video: prompt, first/last frame,
#                                 reference_image_urls, reference_video_urls
set -euo pipefail

PROMPT="${1:?usage: kie-img.sh \"prompt\" model out.png ref1 [ref2...]}"
MODEL="${2:?model required}"
OUT="${3:?output file required}"
shift 3

if [ -z "${KIE_API_KEY:-}" ]; then
  echo "KIE_API_KEY is not set" >&2; exit 2
fi

PROMPT="$PROMPT" MODEL="$MODEL" OUT="$OUT" ASPECT_RATIO="${ASPECT_RATIO:-}" \
python3 - "$@" <<'EOF'
import base64, json, mimetypes, os, sys, time, urllib.request

API = "https://api.kie.ai"
KEY = os.environ["KIE_API_KEY"]

def call(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def upload(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    data = base64.b64encode(open(path, "rb").read()).decode()
    r = call("/api/file-base64-upload", {
        "base64Data": f"data:{mime};base64,{data}",
        "uploadPath": "marty/refs",
        "fileName": os.path.basename(path)})
    d = r.get("data") or {}
    url = d.get("downloadUrl") or d.get("fileUrl") or d.get("url")
    if not url:
        sys.exit(f"upload failed for {path}: {r}")
    print(f"uploaded {path} -> {url}", file=sys.stderr)
    return url

refs = [a if a.startswith("http") else upload(a) for a in sys.argv[1:]]

model = os.environ["MODEL"]
inp = {"prompt": os.environ["PROMPT"], "output_format": "png"}
if refs:
    inp["input_urls" if model.startswith("gpt-image-2") else "image_urls"] = refs
if os.environ.get("ASPECT_RATIO"):
    inp["aspect_ratio"] = os.environ["ASPECT_RATIO"]
if model.startswith("gpt-image-2"):
    inp.pop("output_format", None)

r = call("/api/v1/jobs/createTask", {"model": model, "input": inp})
if r.get("code") != 200:
    sys.exit(f"create failed: {r}")
task = r["data"]["taskId"]
print(f"task {task}", file=sys.stderr)

for i in range(120):
    time.sleep(5)
    req = urllib.request.Request(f"{API}/api/v1/jobs/recordInfo?taskId={task}",
        headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        d = (json.load(resp).get("data") or {})
    state = d.get("state", "")
    if state == "success":
        res = d.get("resultJson") or "{}"
        if isinstance(res, str): res = json.loads(res)
        url = (res.get("resultUrls") or [None])[0]
        if not url: sys.exit(f"no result url: {d}")
        urllib.request.urlretrieve(url, os.environ["OUT"])
        print(f"done in ~{(i+1)*5}s", file=sys.stderr)
        print(os.environ["OUT"])
        break
    if state == "fail":
        sys.exit(f"generation failed: {json.dumps(d)[:800]}")
    print(".", end="", file=sys.stderr, flush=True)
else:
    sys.exit(f"timed out; task {task} may still finish")
EOF
