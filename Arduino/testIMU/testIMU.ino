#include <Adafruit_BNO055.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup(void) {
  Serial.begin(115200);
  bno.begin();
  bno.setExtCrystalUse(true);
  delay(1000);
}

void loop(void) {
  sensors_event_t event; 
  bno.getEvent(&event);
  
  Serial.print(event.orientation.x, 4);
  Serial.print(", ");
  Serial.print(event.orientation.y, 4);
  Serial.print(", ");
  Serial.print(event.orientation.z, 4);
  Serial.println();
  
  delay(100);
}
