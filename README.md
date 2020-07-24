# Vehicle GPS Improvement

Modern GPS is currently accurate on average to around approximately 2-5 m. In urban areas, with large buildings or tree coverage, GPS is even less accurate, sometimes having errors up to around 10+ m. GPS is most often used by vehicles as the main part of their navigation system. As modern vehicles continue to implement their own navigation systems, there is room for improving the positioning of these systems even more.

This project attempts to improve GPS error by implementing a secondary positioning system for a vehicle to use alongside GPS. This secondary positioning system relies on the orientation of the vehicle and the size of its wheels in order to track its location. In order to combine the secondary positioning system with GPS, a [Kalman Filter](https://en.wikipedia.org/wiki/Kalman_filter) algorithm was implemented. Kalman filters are ideal for systems which are continuously changing. They have the advantage that they are light on memory, and they are very fast, making them well suited for real time problems and embedded systems. 

Although there is much more room for improvement and ideas, the design featured in this project consistently allows for better positioning accuracy in building dense areas, and at times when GPS signal cuts out.

## Design

The system design for this project consisted of several different sensors and two boards (controllers). An Arduino Uno was used to output all of the sensor measurements. The Arduino Uno was connected with a GPS, IMU, Hall Effect Sensor, and Altimeter. The Arduino Uno was able to efficiently collect data from all three sensors and output it to the Raspberry Pi 4. The Raspberry Pi 4 was used in order to execute the Kalman Filter. Finally, an OLED display was used in order to display the coordinates computed by the Raspberry Pi 4 to the user.

Solely using a Rapsberry Pi would have been more viable, as it is equipped with an I2C and serial port, however the main focus of this project was implementing the Kalman filter rather than spending too much time trying to get different sensors to work. Thus, the Arduino was very helpful with its many useful libraries. Below the schematic for the final design is shown.

<p align="center">
  <img src="https://i.imgur.com/09ZYpva.png" width="613" height="438">
</p>
Furthermore, here is what the project actually looked like, with everything mounted up to an RC car.
&nbsp;
&nbsp;
&nbsp;


<p align="center">
  <img src="https://i.imgur.com/PaFHG6l.png" width="672" height="426">
</p>



## Development

In order to develop this secondary positioning system, a variety of sensors are used including an IMU, hall effect sensor, and altimeter. Then, in order to combine these two positioning systems, I used a Kalman Filter. All of my testing and design was done using an RC car in order to simulate a real vehicle.

In order to fuse the 

A Kalman filter is an algorithm that uses a series of measurements observed over time, containing statistical noise/inaccuracies, and produces estimates of unknown variables that tends to be more accurate. Kalman filters are ideal for systems which are continuously changing. They have the advantage that they are light on memory (they don’t need to keep any history other than the previous state), and they are very fast, making them well suited for real time problems and embedded systems.

Below is the algorithm which was used for implementing both the secondary positioning system and the Kalman Filter.

<p align="center">
  <img src="https://i.imgur.com/rqvfQbo.png" width="800" height="483">
</p>

https://i.imgur.com/PIl4pCA.jpg

## Results/Usage

Testing was limited in this stage of the project, however I was able to achieve positive results with the algorithm which you can see below.


<p align="center">
  <img src="https://i.imgur.com/tKpTdKr.png" width="500" height="401">
</p>
