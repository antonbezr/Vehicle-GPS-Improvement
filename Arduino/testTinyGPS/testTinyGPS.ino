#include <AltSoftSerial.h>
#include "TinyGPS++.h"

AltSoftSerial gpsPort;
TinyGPSPlus gps;

void setup(void) {
  Serial.begin(115200);
  gpsPort.begin(9600);
  delay(1000);
}

void loop(void) { 
  while (gpsPort.available()) {
    gps.encode(gpsPort.read());
  }

  if (gps.location.isUpdated()) {
    Serial.print(gps.location.lat(), 6);
    Serial.print(", ");
    Serial.print(gps.location.lat(), 6);
    Serial.println();
  }
}
