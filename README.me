# Synopsis

This is a very sloppy project I made myself for a Raspberry Pi-powered smart thermostat. This is by no means a polished, complete project. I would be very happy to see people forking this and creating bigger and better versions. The project consists of three parts:

1. The HVAC controller (Raspberry Pi)
2. One or more temperature sensors (Raspberry Pi)
3. Remote web interface (LAMP stack)

I purposely separated the HVAC controller from the temperature sensors because I can add more, which will give a better "average" temperature throughout my living space, but it can also look at a single sensor if desired.

# Motivation

The thermostat that came with my apartment is not very predictable. Plus, I'm lazy, and I hate having to get up out of bed to adjust the temperature. I wanted something where I could adjust it from my phone or my laptop, wherever I happen to be. Plus, I wanted to be able to specify a temperatue range that would kick on either the air conditioner or the heater.

The best stuff comes from the pursuit of everyday convienence.

# Hardware

In addition to the Raspberry Pi's, you will need some additional hardware, and know some basic knowledge about them. The main components are:

* [SainSmart 4-channel relay module](http://www.amazon.com/gp/product/B0057OC5O8/ref=oh_aui_detailpage_o00_s01?ie=UTF8&psc=1) for the HVAC controller Pi
* [DS18B20 Digital temperature sensor](http://www.adafruit.com/product/374) for the temperature sensor Pi's
* Necessary jumper wires to connect everything

# Installation

### Web interface

After cloning the project, you should first set up the LAMP stack on your server. Note that as it is currently programmed, an SSL certificate is required. In the **Interface** directory, there is a file <code>db\_structure.sql</code> which defines the structure of the MySQL database this interface uses. This should _probably_ not be uploaded to your webserver.

Before continuing, you will need to add a row in the **controllers** table along with the **sensors** table in order for the scripts on the HVAC controller Pi and temperature sensor Pi, respectively, to make authenticated requests. Check out the functions in <code>config.php</code> to create the necessary key hashes and salts.

The rest of the files in the **Interface** directory are used in the actual web interface. You will need to modify the top and bottom of the <code>config.php</code> file to replace the placeholders with the required information.

### HVAC Controller Pi

The files for the HVAC controller are in the **HVAC Controller** directory. These files should be placed inside the <code>/home/pi/thermostat</code> directory of the Raspberry Pi running Raspbian.

Again, you will need to look through the files and replace any sections with placeholders (which I've denoted with **XXXXX** strings) with the proper information.

The HVAC controller uses three Python scripts, running simultaneously:

* <code>puller.py</code> which accesses the **get_settings.php** API enpoint from the web server.
* <code>hvaccontrol.py</code> which controls the relay panel. This is sort of the main brain of the project.
* <code>statuspusher.py</code> which updates the web server with the current status with information like what the fan is doing, what the compressor is doing, etc.

There is also a <code>hvaccontroller_cleanup.py</code> script which should be run in the event of the Raspberry Pi shutting down, just to ensure the relays all turn off.

### Temperature Sensor Pi

The files for the temperature sensors are in the **Sensor** directory. Similarly to the HVAC controller Pi, the temperature sensor Pi's require the placeholders to be changed to their proper values based on your database and file structures.

The sensors use only two Python scripts, also running simultaneously:
* <code>sensor.py</code> which reads from the DS18B20 Digital temperature sensor
* <code>temppusher.py</code> which updates its corresponding row in the **sensors** table of the remote database.

## Contributors

I'm really not too great with the whole open source thing, but feel free to add issues, pull requests, all that jazz.

Once again, I apologize how sloppy all of this is.

## License

The MIT License (MIT)

Copyright (c) 2014 William Thomas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
