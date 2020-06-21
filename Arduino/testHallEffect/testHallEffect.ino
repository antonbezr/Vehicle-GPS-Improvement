#define PIN_HALL  2

volatile byte rotations = 0;

void setup() {
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(PIN_HALL), hall, FALLING);
}

void loop() {
  Serial.println(rotations);
  delay(100);
}

void hall() {
  rotations++;
}
