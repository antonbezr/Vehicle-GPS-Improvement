#include <Adafruit_BNO055.h>
#include <EEPROM.h>

#define RAD_DEG(v) ((v)*((float)(180.0/M_PI)))
#define DEG_RAD(v) ((v)*((float)(M_PI/180.0)))

template<typename T>
struct v3d
{
  T x, y, z;
  v3d() {}
  v3d(T v) : x(v), y(v),z(v) {}
  v3d(T _x, T _y, T _z) : x(_x), y(_y),z(_z) {}
  
  v3d operator + (const v3d& v) const { return v3d(x + v.x, y + v.y, z + v.z); }
  v3d operator - (const v3d& v) const { return v3d(x - v.x, y - v.y, z - v.z); }
  v3d operator * (float v)      const { return v3d(x * v, y * v, z * v); }
  
  v3d& operator -= (const v3d& v) { x -= v.x; y -= v.y, z -= v.z; return *this; }
  bool eq(const v3d& v, T eps) const { return (abs(x - v.x) < eps); }
  float magnitude() const { return (float(pow(float(pow(x, 2) + pow(y, 2) + pow(z, 2)), 0.5)));}
};

template<typename T>
struct box3d
{
  v3d<T> a, b;
  box3d() { init(); }
  
  void init() {
    a = v3d<T>(10000);
    b = v3d<T>(-10000);
  }

  void inflate(const v3d<T>& p) {
    if (a.x > p.x) a.x = p.x;
    if (b.x < p.x) b.x = p.x;
    if (a.y > p.y) a.y = p.y;
    if (b.y < p.y) b.y = p.y;
    if (a.z > p.z) a.z = p.z;
    if (b.z < p.z) b.z = p.z;
  }
};


Adafruit_BNO055 bno = Adafruit_BNO055(55);

typedef v3d<float> vec3d;
static v3d<float>  mag(0);
static v3d<float>  magOff(0);

static long doneCalibration = 0;

static float yaw = 0;
static float pitch = 0;
static float roll  = 0;
static float heading = 0;
static float headingOff = 0;
static float headingAvg = 0;
static float count = 0;

void setup(void) {
  Serial.begin(115200);
  bno.begin();
  bno.setExtCrystalUse(true);

  delay(1000);
  
  calibrate();
  initMag();
}

void loop() {
  updateHeading();
  uint8_t system, gyroC, accelC, magC = 0;
  bno.getCalibration(&system, &gyroC, &accelC, &magC);

  float fixedHeading = fmod((heading + 180), 360);

  if (millis() > doneCalibration + 60000) {
    headingAvg = (count * headingAvg + fixedHeading) / (count + 1);
    count += 1;
  }
    
  Serial.print(fixedHeading);
  Serial.print(", ");
  Serial.print(magC, DEC);
  Serial.print(", ");
  Serial.print(mag.magnitude());
  Serial.print(", ");
  Serial.print(headingAvg);
  Serial.println();
  delay(50);
}

void calibrate() {
  float pitchSum = 0;
  for (int i = 0; i < 10; i++) {
    readBno();
    pitchSum += pitch;
    delay(10);
  }
  pitchSum *= 0.10;
  if (pitchSum < DEG_RAD(50)) return;

  Serial.println("Begin Calibration");
  box3d<float> magMinMax;
  magMinMax.init();
  float timeStart = millis();
  float timeFlat = millis();
  int count = 0;
  vec3d vPRH0 = vec3d(pitch, roll, heading);
 
  while ((millis() - timeStart) < 300000) {
    readBno();
    magMinMax.inflate(mag);
    vec3d vPRH = vec3d(pitch, roll, heading);
    
    if (abs(pitch) > DEG_RAD(15) || !vPRH.eq(vPRH0, DEG_RAD(15))) {
      Serial.print("+");
      count += 1;
      timeFlat = millis();
      vPRH0 = vPRH;
    } else if ((millis() - timeFlat) > 5000) {
      Serial.println();
      break;
    } else {
      Serial.print("-");
      count += 1;
    }
    
    if (count >= 20) {
      Serial.println();
      count = 0;
    }
    delay(50);
  }
  
  magOff = (magMinMax.a + magMinMax.b) * 0.5;
  EEPROM.put(0, magOff);
  doneCalibration = millis();
  delay(1000);
}

void readBno() {
  imu::Vector<3> v;
  
  v = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  yaw = DEG_RAD(v.x());
  pitch = DEG_RAD(v.y());
  roll = -DEG_RAD(v.z());
  heading = yaw;
  
  v = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
  mag.x =  v.x();
  mag.y =  v.z();
  mag.z = -v.y();
  mag -= magOff;
}

void initMag() {
  EEPROM.get(0, magOff);
  for (int i = 0; i < 10; i++) {
    readBno();
    delay(10);
  }
  
  headingOff = get_heading() - RAD_DEG(yaw);
  while (headingOff > 180) headingOff -= 360;
  while (headingOff <= -180) headingOff += 360;
}

float get_heading() {
  float magx2 = mag.x * cos(pitch) - mag.y * sin(pitch) * cos(roll) + mag.z * sin(pitch) * sin(roll);
  float magz2 = mag.y * sin(roll) + mag.z * cos(roll);
  float heading2 = -RAD_DEG(atan2(magz2, magx2));
  return heading2 >= 0 ? heading2 : heading2 + 360;
}

void updateHeading() {
  readBno();
  float magHeading = get_heading();
  float newHeadingOff = magHeading - RAD_DEG(yaw);
  
  float diffHeading = newHeadingOff - headingOff;
  if (diffHeading > 180) diffHeading -= 360;
  else if (diffHeading <= -180) diffHeading += 360;
  
  diffHeading *= cos(pitch) * 0.02;
  headingOff += diffHeading;
  
  heading = RAD_DEG(yaw) + headingOff;
  if (heading > 360) heading -= 360;
  else if (heading < 0) heading += 360;
}
