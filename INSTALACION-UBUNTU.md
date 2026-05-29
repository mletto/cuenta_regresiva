# Cuenta regresiva — Instalación en Ubuntu y arranque automático

Guía paso a paso para ejecutar `cuenta.py` en Ubuntu (pantalla completa, fuente Puma, Arduino opcional) y que inicie sola al encender la PC.

## Instalación automática (recomendada)

Si clonaste el repo desde GitHub (SSH):

```bash
git clone git@github.com:TU_USUARIO/cuenta-regresiva-puma-hyrox.git
cd cuenta-regresiva-puma-hyrox
chmod +x install-ubuntu.sh iniciar.sh run.sh
./install-ubuntu.sh
```

> En la PC Ubuntu necesitás tu clave SSH en `~/.ssh/` o usar un deploy key del repo.

Activa **inicio de sesión automático** en Configuración → Usuarios y reinicia.

---

## Requisitos

- Ubuntu 22.04 o 24.04 (Desktop, con entorno gráfico)
- Conexión a internet (solo para la instalación)
- Carpeta del proyecto **con** la subcarpeta `fonts/` (incluye el archivo `.ttf`)
- Opcional: Arduino conectado por USB para iniciar con el botón físico

---

## 1. Copiar el proyecto en la PC Ubuntu

No copies la carpeta `venv` desde Mac (no sirve en Linux). Sí copia todo lo demás:

```
Cuenta Regresiva/
├── cuenta.py
├── requirements.txt
├── run.sh
├── fonts/
│   └── FF DIN for Puma W01 Cond Bold.ttf
└── INSTALACION-UBUNTU.md
```

Ejemplo de ubicación recomendada:

```bash
/home/TU_USUARIO/cuenta-regresiva
```

Sustituye `TU_USUARIO` por tu usuario real en los pasos siguientes.

---

## 2. Instalar dependencias del sistema

Abre una terminal y ejecuta:

```bash
sudo apt update
sudo apt install -y \
  python3 \
  python3-venv \
  python3-pip \
  libsdl2-dev \
  libsdl2-image-dev \
  libsdl2-mixer-dev \
  libsdl2-ttf-dev \
  fonts-dejavu-core
```

> Estas librerías SDL2 son necesarias para que Pygame funcione en Linux.

---

## 3. Crear el entorno virtual e instalar Python

```bash
cd /home/TU_USUARIO/cuenta-regresiva

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Comprueba que la fuente existe:

```bash
ls -la fonts/
# Debe aparecer: FF DIN for Puma W01 Cond Bold.ttf
```

---

## 4. Permisos para Arduino (opcional)

Si usas Arduino por USB, agrega tu usuario al grupo `dialout`:

```bash
sudo usermod -aG dialout $USER
```

Cierra sesión y vuelve a entrar (o reinicia) para que el cambio aplique.

Regla udev opcional (puerto estable):

```bash
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="2341", MODE="0666", GROUP="dialout"' | sudo tee /etc/udev/rules.d/99-arduino.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

## 5. Probar el script manualmente

```bash
cd /home/TU_USUARIO/cuenta-regresiva
source venv/bin/activate
python cuenta.py
```

| Tecla / acción | Efecto |
|----------------|--------|
| **Espacio** o **Enter** | Inicia / reinicia la cuenta (sin Arduino) |
| **ESC** (1ª vez) | Sale de pantalla completa |
| **ESC** (2ª vez) | Cierra la aplicación |
| **Botón Arduino** | Envía `START` por serial para iniciar |

Si ves `Fuente Puma no encontrada; usando Arial` en la terminal, revisa que `fonts/FF DIN for Puma W01 Cond Bold.ttf` exista.

Para salir si la pantalla quedó bloqueada: `Alt + F4` o `Ctrl + Alt + T` y `killall python3`.

---

## 6. Script de arranque (recomendado)

Crea un script que evite el salvapantallas y lance la app:

```bash
nano /home/TU_USUARIO/cuenta-regresiva/iniciar.sh
```

Pega este contenido (ajusta la ruta si cambiaste de carpeta):

```bash
#!/bin/bash
cd /home/TU_USUARIO/cuenta-regresiva

# Evitar que la pantalla se apague en modo kiosco
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

source venv/bin/activate
exec python cuenta.py
```

Dale permisos de ejecución:

```bash
chmod +x /home/TU_USUARIO/cuenta-regresiva/iniciar.sh
```

Prueba:

```bash
/home/TU_USUARIO/cuenta-regresiva/iniciar.sh
```

---

## 7. Arranque automático al iniciar sesión (método sencillo)

Este método lanza la app cuando el usuario **inicia sesión** en el escritorio (lo más habitual en eventos).

### 7.1 Crear entrada de autostart

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/cuenta-regresiva.desktop
```

Contenido (cambia `TU_USUARIO`):

```ini
[Desktop Entry]
Type=Application
Name=Cuenta Regresiva Puma Hyrox
Comment=Cuenta regresiva en pantalla completa
Exec=/home/TU_USUARIO/cuenta-regresiva/iniciar.sh
Terminal=false
X-GNOME-Autostart-enabled=true
```

### 7.2 Inicio de sesión automático (kiosco)

Para que no pida contraseña al encender:

1. **Configuración** → **Usuarios** → tu usuario → **Inicio de sesión automático**: activado  
   (en algunas versiones: **Configuración** → **Pantalla de bloqueo** → desactivar bloqueo al suspender, si molesta)

En Ubuntu con **LightDM** también puedes editar:

```bash
sudo nano /etc/lightdm/lightdm.conf
```

Busca la sección `[Seat:*]` y agrega o descomenta:

```ini
autologin-user=TU_USUARIO
autologin-user-timeout=0
```

Reinicia:

```bash
sudo reboot
```

Al volver, debería iniciar sesión solo y abrir la cuenta regresiva en pantalla completa.

### 7.3 Desactivar el autostart

```bash
rm ~/.config/autostart/cuenta-regresiva.desktop
```

---

## 8. Arranque con systemd (método avanzado)

Útil si quieres reinicio automático si el programa se cierra. Requiere sesión gráfica ya iniciada.

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/cuenta-regresiva.service
```

Contenido (ajusta usuario y rutas):

```ini
[Unit]
Description=Cuenta regresiva Puma Hyrox
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
WorkingDirectory=/home/TU_USUARIO/cuenta-regresiva
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/TU_USUARIO/.Xauthority
ExecStart=/home/TU_USUARIO/cuenta-regresiva/iniciar.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=graphical-session.target
```

Activa el servicio:

```bash
systemctl --user daemon-reload
systemctl --user enable cuenta-regresiva.service
systemctl --user start cuenta-regresiva.service
```

Comandos útiles:

```bash
systemctl --user status cuenta-regresiva.service   # ver estado
systemctl --user restart cuenta-regresiva.service  # reiniciar
systemctl --user stop cuenta-regresiva.service     # detener
journalctl --user -u cuenta-regresiva.service -f   # ver logs
```

> Si usas **Wayland** y falla `DISPLAY=:0`, inicia sesión con **Ubuntu on Xorg** en la pantalla de login (engranaje → *Ubuntu on Xorg*).

---

## 9. Resolución de problemas

### Pygame no abre / error SDL

```bash
sudo apt install --reinstall libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0
```

### Pantalla negra al arrancar automático

- Espera 10–15 s tras el login (el escritorio puede tardar).
- Añade retraso en el `.desktop`:

```ini
Exec=sh -c 'sleep 5 && /home/TU_USUARIO/cuenta-regresiva/iniciar.sh'
```

### Arduino no detectado

```bash
groups          # debe listar dialout
ls /dev/ttyUSB* /dev/ttyACM*   # ver puerto
```

### Fuente incorrecta

Verifica el archivo:

```bash
file fonts/FF\ DIN\ for\ Puma\ W01\ Cond\ Bold.ttf
```

Debe decir `TrueType Font data`.

### Desinstalar arranque automático

```bash
rm -f ~/.config/autostart/cuenta-regresiva.desktop
systemctl --user disable --now cuenta-regresiva.service 2>/dev/null
```

---

## 10. Resumen rápido

```bash
# Instalación (una vez)
cd /home/TU_USUARIO/cuenta-regresiva
sudo apt install -y python3 python3-venv libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
chmod +x iniciar.sh
# Crear ~/.config/autostart/cuenta-regresiva.desktop
# Activar inicio de sesión automático en Configuración
sudo reboot
```

---

## Controles en el evento

- **Inicio sin Arduino:** barra espaciadora o Enter  
- **Inicio con Arduino:** botón que envía `START` por serial (9600 baud)  
- **Salir del modo kiosco:** ESC dos veces (o matar el proceso desde otra terminal)
