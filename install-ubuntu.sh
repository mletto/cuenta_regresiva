#!/usr/bin/env bash
# Instalación en Ubuntu: dependencias, venv y arranque automático al login.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_AUTOSTART="${1:-yes}"

echo "==> Instalando paquetes del sistema (requiere sudo)..."
sudo apt update
sudo apt install -y \
  python3 \
  python3-venv \
  python3-pip \
  libsdl2-dev \
  libsdl2-image-dev \
  libsdl2-mixer-dev \
  libsdl2-ttf-dev \
  fonts-dejavu-core \
  x11-xserver-utils

echo "==> Creando entorno virtual..."
python3 -m venv "$PROJECT_DIR/venv"
"$PROJECT_DIR/venv/bin/pip" install --upgrade pip
"$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

chmod +x "$PROJECT_DIR/iniciar.sh" "$PROJECT_DIR/run.sh"

if [[ ! -f "$PROJECT_DIR/fonts/FF DIN for Puma W01 Cond Bold.ttf" ]]; then
  echo "AVISO: Falta fonts/FF DIN for Puma W01 Cond Bold.ttf" >&2
fi

if [[ "$INSTALL_AUTOSTART" == "yes" ]]; then
  echo "==> Configurando arranque automático al iniciar sesión..."
  mkdir -p "$HOME/.config/autostart"
  sed "s|@PROJECT_DIR@|$PROJECT_DIR|g" \
    "$PROJECT_DIR/autostart/cuenta-regresiva.desktop" \
    > "$HOME/.config/autostart/cuenta-regresiva.desktop"
  echo "Autostart instalado en ~/.config/autostart/cuenta-regresiva.desktop"
fi

echo "==> Agregando usuario al grupo dialout (Arduino)..."
sudo usermod -aG dialout "$USER" || true

if [[ -f "$PROJECT_DIR/udev/99-arduino.rules" ]]; then
  echo "==> Instalando regla udev para Arduino..."
  sudo cp "$PROJECT_DIR/udev/99-arduino.rules" /etc/udev/rules.d/
  sudo udevadm control --reload-rules
  sudo udevadm trigger
fi

echo ""
echo "Instalación lista."
echo "  Probar ahora:  $PROJECT_DIR/run.sh"
echo "  Kiosco:        $PROJECT_DIR/iniciar.sh"
echo ""
echo "Siguiente paso recomendado: activar inicio de sesión automático"
echo "en Configuración → Usuarios, luego reiniciar."
echo ""
echo "Para desactivar autostart: rm ~/.config/autostart/cuenta-regresiva.desktop"
