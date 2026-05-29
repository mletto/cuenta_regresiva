#!/usr/bin/env bash
# Instala el servicio systemd de usuario (opcional, alternativa al autostart).
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/cuenta-regresiva.service"

mkdir -p "$SERVICE_DIR"
sed "s|@PROJECT_DIR@|$PROJECT_DIR|g" \
  "$PROJECT_DIR/systemd/cuenta-regresiva.service" \
  > "$SERVICE_FILE"

systemctl --user daemon-reload
systemctl --user enable cuenta-regresiva.service
systemctl --user start cuenta-regresiva.service

echo "Servicio instalado. Estado:"
systemctl --user status cuenta-regresiva.service --no-pager
