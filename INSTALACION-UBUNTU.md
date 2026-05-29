# Cuenta regresiva — Instalación en Ubuntu y arranque automático

Guía paso a paso para ejecutar `cuenta_regresiva.py` en Ubuntu (pantalla completa, fuente Puma, Arduino opcional) y que inicie sola al encender la PC.

## Instalación automática (recomendada)

Después de configurar la **Deploy Key** (sección siguiente), en la PC Ubuntu:

```bash
git clone git@github.com:mletto/cuenta_regresiva.git
cd cuenta_regresiva
chmod +x install-ubuntu.sh iniciar.sh run.sh
./install-ubuntu.sh
```

Activa **inicio de sesión automático** en Configuración → Usuarios y reinicia.

---

## Clave SSH en Ubuntu (Deploy Key — recomendado)

La PC del evento necesita poder clonar el repo **privado** por SSH. Lo más seguro es una **Deploy Key**: clave solo para este repositorio, solo lectura.

### Paso 1 — Generar clave en la PC Ubuntu

```bash
ssh-keygen -t ed25519 -C "ubuntu-cuenta-regresiva" -f ~/.ssh/id_ed25519_github
```

Pulsa **Enter** en la passphrase (vacía) si es un kiosco dedicado al evento.

### Paso 2 — Copiar la clave pública

```bash
cat ~/.ssh/id_ed25519_github.pub
```

Copia **toda** la línea (empieza con `ssh-ed25519`).

### Paso 3 — Agregar la Deploy Key en GitHub

1. Abrí el repo: **[https://github.com/mletto/cuenta_regresiva](https://github.com/mletto/cuenta_regresiva)**
2. **Settings** → **Deploy keys** → **Add deploy key**
3. **Title:** `Ubuntu evento` (o el nombre que quieras)
4. **Key:** pegá la clave pública del paso 2
5. **Allow write access:** desmarcado (solo lectura)
6. **Add key**

### Paso 4 — Configurar SSH en Ubuntu

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/config
```

Pegá esto:

```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
```

Guardá: `Ctrl+O`, Enter, `Ctrl+X`.

```bash
chmod 600 ~/.ssh/config ~/.ssh/id_ed25519_github
```

### Paso 5 — Probar conexión

```bash
ssh -T git@github.com
```

Respuesta esperada (similar):

```text
Hi mletto/cuenta_regresiva! You've successfully authenticated...
```

Si dice `Permission denied` o `Repository not found` al clonar, revisá que la Deploy Key esté en el repo correcto y que `~/.ssh/config` apunte a `id_ed25519_github`.

### Paso 6 — Clonar e instalar

```bash
cd ~
git clone git@github.com:mletto/cuenta_regresiva.git
cd cuenta_regresiva
chmod +x install-ubuntu.sh iniciar.sh run.sh
./install-ubuntu.sh
```

> **Sin internet en el evento:** cloná una vez con internet, o copiá la carpeta del proyecto por USB (sin la carpeta `venv`).

---

## Requisitos

- Ubuntu 22.04 o 24.04 (Desktop, con entorno gráfico)
- Conexión a internet (solo para la instalación)
- Carpeta del proyecto **con** la subcarpeta `fonts/` (incluye el archivo `.ttf`)
- Opcional: Arduino conectado por USB para iniciar con el botón físico

---

## 1. Copiar el proyecto en la PC Ubuntu

**Opción recomendada:** clonar con Git (ver [Clave SSH en Ubuntu](#clave-ssh-en-ubuntu-deploy-key--recomendado)).

**Opción alternativa (USB):** no copies la carpeta `venv` desde Mac (no sirve en Linux). Sí copia todo lo demás:

```
Cuenta Regresiva/
├── cuenta_regresiva.py
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

Regla udev opcional (puerto estable; también está en `udev/99-arduino.rules` del repo):

```bash
sudo cp udev/99-arduino.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Cargar el sketch de Arduino

El código del botón está en el repo:

```
arduino/cuenta_regresiva/cuenta_regresiva.ino
```

1. Instalá **Arduino IDE** en Ubuntu (o cargá el sketch desde otra PC).
2. Abrí la carpeta `arduino/cuenta_regresiva/`.
3. **Herramientas → Placa** → tu modelo (ej. Arduino Uno).
4. **Herramientas → Puerto** → `/dev/ttyACM0` o `/dev/ttyUSB0`.
5. **Subir**.
6. **Monitor Serie** a **9600 baud**: al pulsar el botón debe imprimir `START`.

**Cableado:** pin **2** y **GND** al botón (una pata a cada uno). `INPUT_PULLUP` en el código.

---

## 5. Probar el script manualmente

```bash
cd /home/TU_USUARIO/cuenta-regresiva
source venv/bin/activate
python cuenta_regresiva.py
```


| Tecla / acción          | Efecto                                    |
| ----------------------- | ----------------------------------------- |
| **Espacio** o **Enter** | Inicia / reinicia la cuenta (sin Arduino) |
| **ESC** (1ª vez)        | Sale de pantalla completa                 |
| **ESC** (2ª vez)        | Cierra la aplicación                      |
| **Botón Arduino**       | Envía `START` por serial para iniciar     |


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
exec python cuenta_regresiva.py
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

