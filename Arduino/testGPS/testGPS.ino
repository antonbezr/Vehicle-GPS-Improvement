#include <AltSoftSerial.h>
AltSoftSerial gpsPort;

void setup() {
  Serial.begin(115200);
  gpsPort.begin(9600);
  delay(1000);
}

void loop() {
  while (gpsPort.available()) {
    char c = gpsPort.read();
    Serial.print(c);
  }
}
