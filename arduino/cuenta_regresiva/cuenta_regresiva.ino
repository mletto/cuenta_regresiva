// Cuenta regresiva Puma Hyrox — botón de inicio
// Conecta el botón entre pin 2 y GND (INPUT_PULLUP).
// Al presionar envía "START" por Serial a 9600 baud.

const int buttonPin = 2;

bool lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 50;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  bool reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (lastButtonState == HIGH && reading == LOW) {
      Serial.println("START");
    }
  }

  lastButtonState = reading;
}
