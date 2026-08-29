#!/usr/bin/env bash
# Seedance video generation on Kie.ai, split into submit and poll phases
# because a generation can outlast a single command timeout.
#
#   ./kie-vid.sh submit PROMPT_FILE OUT.mp4 REF1 [REF2 ...]
#       Uploads local refs, creates the task, writes OUT.mp4.task with the
#       task id, prints the id. Env: MODEL (default bytedance/seedance-2-5),
#       RESOLUTION (default 720p), DURATION (default 12), GENERATE_AUDIO
#       (default false).
#   ./kie-vid.sh poll OUT.mp4 [MAX_SECONDS]
#       Polls the task in OUT.mp4.task until success/fail or MAX_SECONDS
#       (default 540), downloading to OUT.mp4 on success. Exit 3 = still
#       running (call poll again).
set -euo pipefail
MODE="${1:?usage: kie-vid.sh submit|poll ...}"; shift

python3 - "$MODE" "$@" <<'EOF'
import base64, json, mimetypes, os, sys, time, urllib.request

API = "https://api.kie.ai"
UPLOAD_API = "https://kieai.redpandaai.co"
KEY = os.environ["KIE_API_KEY"]
UA = "curl/8.5.0"

def call(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                 "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def upload(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    data = base64.b64encode(open(path, "rb").read()).decode()
    r = call(UPLOAD_API + "/api/file-base64-upload", {
        "base64Data": f"data:{mime};base64,{data}",
        "uploadPath": "marty/film", "fileName": os.path.basename(path)})
    url = (r.get("data") or {}).get("downloadUrl")
    if not url: sys.exit(f"upload failed for {path}: {r}")
    print(f"uploaded {os.path.basename(path)}", file=sys.stderr)
    return url

mode = sys.argv[1]
if mode == "submit":
    prompt_file, out = sys.argv[2], sys.argv[3]
    refs = [a if a.startswith("http") else upload(a) for a in sys.argv[4:]]
    inp = {"prompt": open(prompt_file).read(),
           "resolution": os.environ.get("RESOLUTION", "720p"),
           "duration": int(os.environ.get("DURATION", "12")),
           "aspect_ratio": "16:9",
           "generate_audio": os.environ.get("GENERATE_AUDIO", "false") == "true"}
    if refs: inp["reference_image_urls"] = refs
    r = call(API + "/api/v1/jobs/createTask",
             {"model": os.environ.get("MODEL", "bytedance/seedance-2-5"), "input": inp})
    if r.get("code") != 200: sys.exit(f"create failed: {r}")
    task = r["data"]["taskId"]
    open(out + ".task", "w").write(task)
    print(task)
elif mode == "poll":
    out = sys.argv[2]
    max_s = int(sys.argv[3]) if len(sys.argv) > 3 else 540
    task = open(out + ".task").read().strip()
    start = time.time()
    while time.time() - start < max_s:
        req = urllib.request.Request(f"{API}/api/v1/jobs/recordInfo?taskId={task}",
            headers={"Authorization": f"Bearer {KEY}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            d = (json.load(resp).get("data") or {})
        state = d.get("state", "")
        if state == "success":
            res = d.get("resultJson") or "{}"
            if isinstance(res, str): res = json.loads(res)
            url = (res.get("resultUrls") or [None])[0]
            if not url: sys.exit(f"no result url: {d}")
            dl = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(dl, timeout=600) as r, open(out, "wb") as f:
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk: break
                    f.write(chunk)
            print(f"{out} credits={d.get('creditsConsumed','?')}")
            sys.exit(0)
        if state == "fail":
            sys.exit(f"generation failed: code={d.get('failCode')} msg={d.get('failMsg')}")
        time.sleep(10)
    print(f"still running: {task}", file=sys.stderr)
    sys.exit(3)
else:
    sys.exit(f"unknown mode {mode}")
EOF
