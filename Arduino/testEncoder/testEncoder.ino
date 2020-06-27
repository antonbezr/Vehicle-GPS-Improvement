static int pinA = 2;
static int pinB = 3;
volatile byte aFlag = 0;
volatile byte bFlag = 0;
volatile byte encoderPos = 0;
volatile byte oldEncPos = 0;
volatile byte reading = 0;

void setup() {
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);
  attachInterrupt(0, interruptA, RISING);
  attachInterrupt(1, interruptB, RISING);
  Serial.begin(115200);
}

void loop() {
  if(oldEncPos != encoderPos) {
    Serial.println(encoderPos);
    oldEncPos = encoderPos;
  }
}

void interruptA() {
  reading = PIND & 0xC;
  if(reading == B00001100 && aFlag) {
    encoderPos--;
    bFlag = 0;
    aFlag = 0;
  }
  else if (reading == B00000100) bFlag = 1;
}

void interruptB() {
  reading = PIND & 0xC;
  if (reading == B00001100 && bFlag) {
    encoderPos++;
    bFlag = 0;
    aFlag = 0;
  }
  else if (reading == B00001000) aFlag = 1;
}
