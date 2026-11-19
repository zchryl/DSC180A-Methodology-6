#!/usr/bin/env bash
set -uo pipefail

payload=$(cat)
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

if [ -x ".venv/Scripts/python.exe" ]; then
  PY=".venv/Scripts/python.exe"
elif [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
else
  PY="python"
fi

path=$(printf '%s' "$payload" | "$PY" -c \
  'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')

norm_path="${path//\\//}"
case "$norm_path" in
  *src/*.py) ;;
  *) exit 0 ;;
esac

if ! out=$("$PY" -m pytest tests/test_leakage.py -q 2>&1); then
  echo "Leakage tests failed after editing $path:" >&2
  echo "$out" | tail -20 >&2
  exit 2
fi
exit 0