# Cuenta regresiva — Puma Hyrox

Pantalla de cuenta regresiva en **pantalla completa** (`00:45` → `00:00`), tipografía Puma, inicio por **Arduino** o teclado.

## Requisitos

- Python 3.10+
- Pantalla con entorno gráfico (Linux o macOS)
- Opcional: Arduino que envíe `START` por serial a 9600 baud

## Estructura del proyecto

```
.
├── cuenta.py              # Aplicación principal
├── fonts/                 # Fuente FF DIN for Puma (incluida)
├── requirements.txt
├── run.sh                 # Ejecutar en Mac o Linux (crea venv local)
├── iniciar.sh             # Ejecutar en Ubuntu (modo kiosco)
├── install-ubuntu.sh      # Instalación completa en Ubuntu + autostart
├── install-systemd.sh     # Servicio systemd (opcional)
├── autostart/             # Plantilla de inicio al login
├── systemd/               # Plantilla de servicio
├── udev/                  # Regla para puerto Arduino
└── INSTALACION-UBUNTU.md  # Guía detallada paso a paso
```

## Uso rápido (Mac o Linux)

```bash
git clone git@github.com:mletto/cuenta_regresiva.git
cd cuenta_regresiva
chmod +x run.sh
./run.sh
```

| Tecla | Acción |
|-------|--------|
| Espacio / Enter | Iniciar o reiniciar cuenta |
| ESC | Salir de fullscreen / cerrar app |

## Ubuntu — instalación en una PC de evento

1. Configurá una **Deploy Key** en la PC Ubuntu (solo una vez). Guía: [INSTALACION-UBUNTU.md → Clave SSH](INSTALACION-UBUNTU.md#clave-ssh-en-ubuntu-deploy-key--recomendado)
2. Luego:

```bash
git clone git@github.com:mletto/cuenta_regresiva.git
cd cuenta_regresiva
chmod +x install-ubuntu.sh iniciar.sh run.sh
./install-ubuntu.sh
```

Eso instala dependencias, crea `venv`, configura **arranque automático al login** y permisos de Arduino.

Luego activá **inicio de sesión automático** en Configuración → Usuarios y reiniciá.

Guía completa: [INSTALACION-UBUNTU.md](INSTALACION-UBUNTU.md)

### Sin autostart (solo instalar dependencias)

```bash
./install-ubuntu.sh no
```

### Servicio systemd (opcional)

```bash
./install-systemd.sh
```

## Configuración

En `cuenta.py`:

```python
COUNTDOWN_START = 45   # segundos (se muestra como MM:SS)
SERIAL_BAUDRATE = 9600
```

## Arduino

El sketch debe enviar la línea `START` por Serial cuando se presiona el botón.

Tras instalar en Ubuntu, cerrá sesión una vez para aplicar el grupo `dialout`.

## Fuente

La fuente **FF DIN for Puma** está en `fonts/`. Es material con licencia de Puma; usá un **repositorio privado** en GitHub si no tenés permiso de distribución pública.

## Subir a GitHub (SSH)

1. Creá un repo vacío en GitHub (sin README, sin `.gitignore`).
2. En tu Mac, desde la carpeta del proyecto:

```bash
git remote add origin git@github.com:mletto/cuenta_regresiva.git
git push -u origin main
```

Si el repo ya tiene commit local (como este proyecto):

```bash
git remote -v                    # ver si ya hay remote
git remote set-url origin git@github.com:mletto/cuenta_regresiva.git
git push -u origin main
```

### SSH (solo la primera vez)

```bash
# Generar clave si no tenés una
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# Copiar clave pública al portapapeles (macOS)
pbcopy < ~/.ssh/id_ed25519.pub
```

En GitHub: **Settings → SSH and GPG keys → New SSH key** → pegar y guardar.

Probar conexión:

```bash
ssh -T git@github.com
```

> Reemplazá `TU_USUARIO` y el nombre del repo por los tuyos.

## Licencia

Código del evento — uso interno. La fuente en `fonts/` no se redistribuye sin autorización de Puma.
