import os
import sys
import time

import pygame
import serial
import serial.tools.list_ports

# Mejora teclado en pantalla completa en macOS
os.environ.setdefault("SDL_VIDEO_MAC_FULLSCREEN_SPACES", "1")

COUNTDOWN_START = 45
SERIAL_BAUDRATE = 9600

PUMA_FONT_NAMES = (
    "FF DIN for Puma W01 Cond Bold.ttf",
    "FFDINforPumaW01-CondBold.ttf",
)


def _puma_font_candidates():
    base = os.path.dirname(os.path.abspath(__file__))
    dirs = [
        os.path.join(base, "fonts"),
        os.path.expanduser("~/.local/share/fonts"),
        os.path.expanduser("~/.fonts"),
        "/usr/local/share/fonts",
        "/usr/share/fonts/truetype",
        "/usr/share/fonts",
        os.path.expanduser("~/Library/Fonts"),
        "/Library/Fonts",
    ]
    for directory in dirs:
        for name in PUMA_FONT_NAMES:
            yield os.path.join(directory, name)


def load_puma_font(size):
    for path in _puma_font_candidates():
        if os.path.isfile(path):
            return pygame.font.Font(path, size)
    if "ffdinforpumaw01cond" in pygame.font.get_fonts():
        return pygame.font.SysFont("ffdinforpumaw01cond", size)
    print("Fuente Puma no encontrada; usando Arial.", file=sys.stderr)
    return pygame.font.SysFont("Arial", size, bold=True)


def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if (
            "Arduino" in port.description
            or "usbmodem" in port.device
            or "usbserial" in port.device
            or port.device.startswith("/dev/ttyACM")
            or port.device.startswith("/dev/ttyUSB")
        ):
            return port.device
    return None


def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def main():
    global screen, WIDTH, HEIGHT

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Cuenta regresiva")
    WIDTH, HEIGHT = screen.get_size()

    font_timer = load_puma_font(650)
    font_small = load_puma_font(20)
    clock = pygame.time.Clock()

    arduino_port = find_arduino_port()
    ser = None

    if arduino_port:
        ser = serial.Serial(arduino_port, SERIAL_BAUDRATE, timeout=0.1)
        time.sleep(2)
        print(f"Arduino conectado en {arduino_port}")
    else:
        print("Arduino no detectado. Podés probar con la tecla ESPACIO.")

    counting = False
    remaining = COUNTDOWN_START
    last_tick = time.time()

    def draw_screen(value, status):
        screen.fill((0, 0, 0))
        timer_text = font_timer.render(format_time(value), True, (255, 255, 255))
        screen.blit(timer_text, timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if status:
            status_text = font_small.render(status, True, (180, 180, 180))
            screen.blit(status_text, status_text.get_rect(center=(WIDTH // 2, HEIGHT - 80)))
        pygame.display.flip()

    running = True

    try:
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN) and not counting:
                        counting = True
                        remaining = COUNTDOWN_START
                        last_tick = time.time()
                    elif event.key == pygame.K_ESCAPE:
                        if screen.get_flags() & pygame.FULLSCREEN:
                            screen = pygame.display.set_mode((1280, 720))
                            WIDTH, HEIGHT = screen.get_size()
                        else:
                            running = False

            if ser and ser.in_waiting > 0:
                message = ser.readline().decode(errors="ignore").strip()
                if message == "START" and not counting:
                    counting = True
                    remaining = COUNTDOWN_START
                    last_tick = time.time()

            if counting:
                now = time.time()
                if now - last_tick >= 1:
                    remaining -= 1
                    last_tick = now
                    if remaining <= 0:
                        remaining = 0
                        counting = False
                draw_screen(remaining, "")
            elif remaining == 0:
                draw_screen(0, "Finalizado - presionar el botón para reiniciar")
            else:
                draw_screen(COUNTDOWN_START, "Presionar el botón para iniciar")
    finally:
        pygame.quit()
        if ser:
            ser.close()


if __name__ == "__main__":
    main()
    sys.exit(0)
