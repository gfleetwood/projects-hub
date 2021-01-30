## Overview

kiyo is an IOT device that monitors the current usage of an application to determine whether it is on or off. This status is displayed on a web app, and a change in status sends a text message to the user.

## Development

This the tutorial I followed to build the [MVP](https://learn.openenergymonitor.org/electricity-monitoring/ct-sensors/how-to-build-an-arduino-energy-monitor-measuring-current-only?redirected=true). Instead of an Arduino Mega I used an ESP32 to connect to the Internet. This code is in the `energy_monitor` folder. The `client` folder contains the code for the simple Flask app that displays the sensor reading and status. The status is determined from a very simple gradient calculation of the last two readings once at least five readings have been collected. 

The texting service is through Twilio, but is not fully developed. What I mean is that I received 40 texts in about a minute during testing, and have only commented out the code since then. A complete solution would implement the logic with some nuance, such as only texting when the device is off. That being said, even that is open to the deluge mentioned previously since the sensor is a bit iffy.

I've lost motivation for this work, but any future development would implement the electronic mechanisms to reduce the variability in sensor readings.
