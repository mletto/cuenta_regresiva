#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if [[ ! -x "$PROJECT_DIR/venv/bin/python" ]]; then
  echo "No existe venv. Ejecutá: ./install-ubuntu.sh" >&2
  exit 1
fi

if command -v xset >/dev/null 2>&1; then
  xset s off 2>/dev/null || true
  xset -dpms 2>/dev/null || true
  xset s noblank 2>/dev/null || true
fi

source "$PROJECT_DIR/venv/bin/activate"
exec python "$PROJECT_DIR/cuenta_regresiva.py"
