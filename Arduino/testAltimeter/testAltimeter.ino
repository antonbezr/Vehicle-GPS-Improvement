#include <Wire.h>
#include <SparkFunMPL3115A2.h>

MPL3115A2 altimeter;

static float altimeterRead = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  altimeter.begin();
  altimeter.setModeAltimeter();
  altimeter.setOversampleRate(7);
  altimeter.enableEventFlags();
  delay(1000);
}

void loop() {
  altimeterRead = altimeter.readAltitude();
  Serial.println(altimeterRead);
  delay(50);
}
