#include <AltSoftSerial.h>
#include <TinyGPS++.h>
#include <Adafruit_BNO055.h>
#include <SparkFunMPL3115A2.h>

#define PIN_HALL  2

AltSoftSerial gpsPort;
TinyGPSPlus gps;
Adafruit_BNO055 bno = Adafruit_BNO055(55);
MPL3115A2 altimeter;

volatile byte wheelCount = 0;
static byte prevWheelCount = 0;

static float yaw = 0;
static float roll = 0;

static float altimeterRead = 0;
static float altimeterOld = 0;
static int altimeterUpdated = 0;
static long prevBaroReadTime = 0;

void setup(void) {
  attachInterrupt(digitalPinToInterrupt(PIN_HALL), hallInterrupt, FALLING);
  
  Serial.begin(115200);
  gpsPort.begin(9600);
  bno.begin();
  bno.setExtCrystalUse(true);
  altimeter.begin();
  altimeter.setModeAltimeter();
  altimeter.setOversampleRate(7);
  altimeter.enableEventFlags();
  
  delay(1000);
}

void loop(void) { 
  while (gpsPort.available()) {
    gps.encode(gpsPort.read());
  }
  
  if (gps.location.isUpdated()) {
    printAll();
  } else if (wheelCount != prevWheelCount) {
    prevWheelCount = wheelCount;
    printAll();
  }

  updateIMU();
  updateHeight();
}

void hallInterrupt() {
  wheelCount++;
}

void updateIMU() {
  sensors_event_t event; 
  bno.getEvent(&event);
  
  yaw = event.orientation.x;
  roll = -event.orientation.z;  
}

void updateHeight() {
  if (millis() - prevBaroReadTime > 400) {
    altimeterRead = altimeter.readAltitude();
    altimeterUpdated = 1;
    printAll();
    prevBaroReadTime = millis();
  }
  altimeterUpdated = 0;
}

void printAll() {
  Serial.print(gps.location.isUpdated());
  Serial.print(", ");
  Serial.print(gps.location.lat(), 6);
  Serial.print(", ");
  Serial.print(gps.location.lng(), 6);
  Serial.print(", ");
  Serial.print(gps.course.deg());
  Serial.print(", ");
  Serial.print(gps.satellites.value());
  Serial.print(", ");
  Serial.print(yaw);
  Serial.print(", ");
  Serial.print(roll);
  Serial.print(", ");
  Serial.print(wheelCount);
  Serial.print(", ");
  Serial.print(altimeterUpdated);
  Serial.print(", ");
  Serial.print(altimeterRead);
  Serial.print(", ");
  Serial.print(millis());
  Serial.println();
}
