# Vehicle GPS Improvement

Modern GPS is currently accurate on average to around approximately 2-5 m. In urban areas, with large buildings or tree coverage, GPS is even less accurate, sometimes having errors up to around 10 m. GPS is often used by cars as the main part of their navigation system. As modern cars continue to implement their own navigation systems, there is room for improving the positioning of these systems even more.

This project attempts to improve GPS error by implementing a secondary positioning system for a car to use alongside GPS. This secondary positioning system relies on the orientation of the vehicle and the size of its wheels in order to track its location. In order to combine the secondary positioning system with GPS, a [Kalman Filter](https://en.wikipedia.org/wiki/Kalman_filter) algorithm was implemented. Kalman filters are ideal for systems which are continuously changing. They have the advantage that they are light on memory, and they are very fast, making them well suited for real time problems and embedded systems. 

Although there is much more room for improvement and ideas, the design featured in this project consistently allows for better positioning accuracy in building dense areas, and at times when GPS signal cuts out.

## Design

The system design for this project consisted of several different sensors and two boards (controllers). An Arduino Uno was used to output all of the sensor measurements. The Arduino Uno was connected with a GPS, IMU, Hall Effect Sensor, and Altimeter. The Arduino Uno was able to efficiently collect data from all three sensors and output it to the Raspberry Pi 4. The Raspberry Pi 4 was used in order to execute the Kalman Filter. Finally, an OLED display was used in order to display the coordinates computed by the Raspberry Pi 4 to the user.

Solely using a Rapsberry Pi would have been more viable, as it is equipped with an I2C and serial port, however the main focus of this project was implementing the Kalman filter rather than spending too much time trying to get different sensors to work. Thus, the Arduino was very helpful with its many useful libraries. Below the schematic for the final design is shown.

<p align="center">
  <img src="https://i.imgur.com/09ZYpva.png" width="613" height="438">
</p>
Furthermore, here is what the project actually looked like, with everything mounted up to an RC car. Using an RC car allowed for many different test runs where the true vehicle path was able to be reconstructed precisely. This way it was possible to very accurately gauge the error from the algorithm and adjust appropriately.

&nbsp;

<p align="center">
  <img src="https://i.imgur.com/PaFHG6l.png" width="672" height="426">
</p>

## Development

The Arduino Uno was developed so that it would output sensor measurements any time there was a new reading from a sesnor. This data was then transferred to the Raspberry Pi 4 via serial port. Afterward, the sensor measurements were combined using a Kalman filter to determine position. After calculation, the computed GPS coordinate was sent to the OLED display.

A Kalman filter is an algorithm that uses a series of measurements observed over time, containing statistical noise/inaccuracies, and produces estimates of unknown variables that tends to be more accurate. Kalman filters are ideal for systems which are continuously changing. They are commonly used in navigation applications, particularly in the aircraft field. Below are the algorithms which were developed for this project (both the secondary positioning system and the Kalman Filter).

&nbsp;

<p align="center">
  <img src="https://i.imgur.com/UV8jKdG.png" width="95%" height="95%">
</p>

## Results/Usage

Testing was limited in this stage of the project, however I was able to achieve positive results with the algorithm which you can see below.


<p align="center">
  <img src="https://i.imgur.com/tKpTdKr.png" width="500" height="401">
</p>
