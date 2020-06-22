# Vehicle GPS Improvement

Modern GPS is currently accurate on average to around approximately 2-5 m. In urban areas, with large buildings or tree coverage, GPS is even less accurate, sometimes having errors up to around 10+ m. GPS is most often used by vehicles as the main part of their navigation system. As modern vehicles continue to implement their own navigation systems, there is room for improving the positioning of these systems even more.

This project attempts to improve GPS error by implementing a secondary positioning system for a vehicle to use alongside GPS. This secondary positioning system relies on the orientation of the vehicle and the size of its wheels in order to track its location.

In order to develop this secondary positioning system, a variety of sensors are used including an IMU, hall effect sensor, and altimeter. Then, in order to combine these two positioning systems, I used a Kalman Filter.

All of my testing and design was done using an RC car in order to simulate a real vehicle.

Although there is much more room for improvement and ideas, this project consistently allows for better positioning accuracy in building dense areas and at times when GPS signal cuts out.

## Design

<p align="center">
  <img src="https://i.imgur.com/09ZYpva.png" width="613" height="438">
</p>

<p align="center">
  <img src="https://i.imgur.com/jboK9KN.png" width="672" height="426">
</p>

## Development

<p align="center">
  <img src="https://i.imgur.com/Bhq02v5.jpg" width="417" height="791">
</p>

## Results

<p align="center">
  <img src="https://i.imgur.com/tKpTdKr.png" width="500" height="401">
</p>
