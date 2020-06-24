import serial
import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from datetime import datetime

def newTxtPath():
    now = datetime.now()
    dtString = now.strftime("%m-%d-%H-%M-%S")
    return "/home/pi/Documents/VehicleGPS/Data/" + dtString + ".txt"

ser = serial.Serial('/dev/ttyACM0',115200)
t0 = int(time.time() * 1000)
txtPath = newTxtPath()

i2c = busio.I2C(SCL, SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height - padding
x = 0

prevMillis = 0
currMillis = 0
oldGpsLat = 0
oldGpsLng = 0
gpsLat = 0
gpsLng = 0
gpsSat = 0
wheel = 0

while True:
    read_serial = ser.readline()
    
    if (int(time.time() * 1000) - t0 > 5000):
        rawData = read_serial[:(len(read_serial) - 2)]
        dataStr = rawData.decode()
        data = dataStr.split(',')
        
        if len(data) == 13:
            currMillis = int(float(data[12]))
            gpsLat = float(data[1])
            gpsLng = float(data[2])
            gpsSat = int(float(data[6]))
            wheel = int(float(data[9]))
            
        if (currMillis < prevMillis):
            txtPath = newTxtPath()
        prevMillis = currMillis
        
        print(dataStr)
        with open(txtPath, "a") as txtFile:
            txtFile.write(dataStr + "\n")
        
        if gpsLat != oldGpsLat or gpsLng != oldGpsLng:
            
            oldGpsLat = gpsLat
            oldGpsLng = gpsLng
            
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            draw.text((x, top), "GPS Lat: " + str(gpsLat) + "°", fill=255)
            draw.text((x, top + 8), "GPS Lng: " + str(gpsLng) + "°", fill=255)
            draw.text((x, top + 16), "Sattelites: " + str(gpsSat), fill=255)
            draw.text((x, top + 24), "Wheel: " + str(wheel), fill=255)

            image = image.transpose(3)
            
            disp.image(image)
            disp.show()

