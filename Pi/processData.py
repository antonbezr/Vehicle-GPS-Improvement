import numpy as np
import csv

# CONSTANTS
wheel = 7.8 * np.pi / 3 / 100
pitch_offset = 2.01
I = np.matrix([[1.0, 0.0, 0.0],
               [0.0, 1.0, 0.0],
               [0.0, 0.0, 1.0]])
update_interval = 1500

# VARIABLES
uno_gps_updated = 0
uno_gps_lat = 0
uno_gps_lng = 0
uno_gps_course = 0
uno_gps_speed_mph = 0
uno_gps_satellites = 0
uno_yaw = 0
uno_pitch = 0
uno_wheel = 0
uno_altimeter_updated = 0
uno_altimeter = 0
uno_millis = 0

prev_time_speed = 0
speed = 0
altimeter = 0
pitch = 0
height = 0
wheel_count = 0
heading_initiated = False
delta_x = 0
delta_y = 0
yaw_set = 0

x = 0
x_list = 0
P = 0


def loadData(raw_path):
    global uno_gps_updated, uno_gps_lat, uno_gps_lng, uno_gps_course, uno_gps_speed_mph, uno_gps_satellites
    global uno_yaw, uno_pitch, uno_wheel, uno_altimeter_updated, uno_altimeter, uno_millis
    global prev_time_speed, speed, altimeter, pitch, height, wheel_count
    global heading_initiated, delta_x, delta_y, yaw_set, x, x_list, P

    data = np.loadtxt(raw_path, delimiter=',', dtype=str, comments="$")

    # TODO: UPDATE uno & FIX NUMBERS, implement max distance change 50m (avoid gps latency error)
    uno_gps_updated = list(map(float, data[0:10000, 0]))
    uno_gps_lat = list(map(float, data[0:10000, 1]))
    uno_gps_lng = list(map(float, data[0:10000, 2]))
    uno_gps_course = list(map(float, data[0:10000, 3]))
    uno_gps_satellites = list(map(float, data[0:10000, 4]))
    uno_yaw = list(map(float, data[0:10000, 5]))
    uno_pitch = list(map(float, data[0:10000, 6]))
    uno_wheel = list(map(float, data[0:10000, 7]))
    uno_altimeter_updated = list(map(float, data[0:10000, 8]))
    uno_altimeter = list(map(float, data[0:10000, 9]))
    uno_millis = list(map(float, data[0:10000, 10]))

    prev_time_speed = 0
    speed = 0
    altimeter = 0
    pitch = 0
    height = 0
    wheel_count = 0
    heading_initiated = False
    delta_x = 0
    delta_y = 0
    yaw_set = 0

    x = np.array([0.0, 0.0, 0.0])
    x = x.reshape(3, 1)
    x_list = np.array([[0.0, 0.0, 0.0]])

    P = np.matrix([[0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0]])


def updateSpeed(i):
    global prev_time_speed, speed

    time_diff = uno_millis[i] - prev_time_speed

    # If wheel spins, determine speed in m/s
    if uno_wheel[i] != uno_wheel[i - 1]:
        speed = wheel / time_diff * 1000
        prev_time_speed = uno_millis[i]

    # If wheel not spinning set speed to zero
    if time_diff > 1000: speed = 0


def mapXY(i):
    global altimeter, pitch, height, wheel_count, delta_x, delta_y, yaw_set

    # Getting initial values for altimeter and IMU pitch
    if i == 1:
        altimeter = uno_altimeter[i]
        pitch = uno_pitch[i]

    # Smoothing altimeter (constantly)
    if uno_altimeter_updated[i] == 1:
        smooth = max(-0.0475 * speed + 0.95 + 0.95, 0)
        altimeter = smooth * altimeter + (1 - smooth) * uno_altimeter[i]

    # Determine starting altitude
    if uno_wheel[i] == 1:
        height = altimeter

    if uno_wheel[i] != uno_wheel[i - 1] and x[0][0] != 0 and x[1][0] != 0 and heading_initiated:

        # Smoothing IMU pitch (only while moving)
        pitch = 0.9 * pitch + 0.1 * uno_pitch[i]

        # Calculate change in height from altimeter and pitch
        delta_height_pitch = wheel * np.sin((pitch - pitch_offset) * np.pi / 180)
        delta_height_altimeter = altimeter - height

        # Approximate real change in height
        if np.abs(delta_height_pitch) < np.abs(delta_height_altimeter):
            height += delta_height_pitch
            delta_height = delta_height_pitch
        else:
            height += delta_height_altimeter
            delta_height = delta_height_altimeter

        # Finding horizontal distance traveled
        deg = (x[2][0] + uno_yaw[i] - yaw_set) * np.pi / 180
        flat_distance = np.sqrt(wheel ** 2 - delta_height ** 2)
        delta_x += flat_distance * np.cos(deg)
        delta_y += flat_distance * np.sin(deg)

        wheel_count += 1


def gpsCovarianceMatrix(i):
    gpsMaxError = 0
    if uno_gps_satellites[i] <= 4: gpsMaxError = 8000
    if uno_gps_satellites[i] == 5: gpsMaxError = 7000
    if uno_gps_satellites[i] == 6: gpsMaxError = 6000
    if uno_gps_satellites[i] == 7: gpsMaxError = 5000
    if uno_gps_satellites[i] == 8: gpsMaxError = 4000
    if uno_gps_satellites[i] >= 9: gpsMaxError = 3000

    # Update R based on the number of available GPS satellites
    T = np.matrix([[gpsMaxError / 4, 0, 0],
                   [0, gpsMaxError / 4, 0],
                   [0, 0, gpsMaxError / 4]])
    T = T ** 2
    return T


def kalmanFilterPredict(i):
    global delta_x, delta_y, yaw_set, x, P, wheel_count

    # Map meters from secondary positioning system to change in lat/lng
    delta_lat = (360 * delta_x) / (40008000)
    delta_lng = (360 * delta_y) / (40075160 * np.cos(x[0][0] / 180 * np.pi))
    delta_heading = (uno_yaw[i] - yaw_set) % 360
    delta_x = 0
    delta_y = 0
    yaw_set = uno_yaw[i]
    u = np.array([delta_lat, delta_lng, delta_heading])
    u = u.reshape(3, 1)

    # Project state ahead
    x = x + u
    x[2][0] = x[2][0] % 360

    # Update Q based on distance traveled from secondary positioning system
    Q = np.matrix([[10 * wheel_count / 4, 0, 0],
                   [0, 10 * wheel_count / 4, 0],
                   [0, 0, 10 * wheel_count / 4]])
    Q = Q ** 2
    wheel_count = 0

    # Project the error covariance ahead
    P = P + Q


def kalmanFilterCorrect(i):
    global x, P, x_list

    R = gpsCovarianceMatrix(i)

    # Compute the Kalman Gain
    K = P * np.linalg.inv(P + R)

    # Update the estimate
    z = np.array([uno_gps_lat[i], uno_gps_lng[i], uno_gps_course[i]])
    z = z.reshape((3, 1))
    z_minus_x = z - x
    if z_minus_x[2][0] > 180: z_minus_x[2][0] = z_minus_x[2][0] % -360
    if z_minus_x[2][0] < -180: z_minus_x[2][0] = z_minus_x[2][0] % 360
    x = x + np.asarray(K * z_minus_x)
    x[2][0] = x[2][0] % 360

    # Update the error covariance
    P = (I - K) * P


def kalmanFilter():
    global heading_initiated, uno_gps_updated, uno_gps_satellites, yaw_set, x, x_list, P

    time_gps = 0
    prev_time_gps = 0
    gps_update_count = 0

    for i in range(1, len(uno_gps_updated)):

        # Update the speed of the car (used for smoothing altimeter)
        updateSpeed(i)

        # Wait to initialize secondary positioning system until heading has been implemented
        if uno_wheel[i] > 100 and gps_update_count > 20: heading_initiated = True

        # Map the secondary positioning system into ground displacement
        mapXY(i)

        time_gps = uno_millis[i] - prev_time_gps
        if uno_gps_updated[i] == 1 and uno_gps_satellites[i] > 0 or (heading_initiated and time_gps > update_interval):
            # When first GPS coordinate is detected, initialize everything
            if heading_initiated == False:
                yaw_set = uno_yaw[i]
                x[0][0] = uno_gps_lat[i]
                x[1][0] = uno_gps_lng[i]
                x[2][0] = uno_gps_course[i]
                P = gpsCovarianceMatrix(i)
                if gps_update_count == 0:
                    x_list[0][0] = x[0][0]
                    x_list[0][1] = x[1][0]
                    x_list[0][2] = x[2][0]
                gps_update_count += 1

            # Perform Kalman Filter
            else:        
                kalmanFilterPredict(i)
                if uno_gps_updated[i] == 1:
                    kalmanFilterCorrect(i)

            # Add coordinate to Kalman Filter list
            x_list = np.append(x_list, x.reshape((1, 3)), axis=0)
            prev_time_gps = uno_millis[i]


def writeToCSV(csv_path, data_type):
    with open(csv_path, mode='w') as m:
        map_writer = csv.writer(m, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if data_type == 0:
            for i in range(len(x_list)):
                map_writer.writerow([x_list[i][0], x_list[i][1]])
        if data_type == 1:
            for i in range(len(uno_gps_updated)):
                if uno_gps_updated[i] == 1:
                    map_writer.writerow([uno_gps_lat[i], uno_gps_lng[i]])

# --------------- EXECUTE KALMAN FILTER(S) ---------------

raw_path = "/Users/anton/Documents/Vehicle GPS Improvement/Raw Path Data/sammamish2.txt"
csv_ekf = "/Users/anton/Downloads/ekf.csv"
csv_gps = "/Users/anton/Downloads/gps.csv"

loadData(raw_path)
kalmanFilter()
writeToCSV(csv_ekf, 0)
writeToCSV(csv_gps, 1)
