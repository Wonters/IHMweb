# Automatic Characterization Bench Base Stations

This package is a library that provides functions to drive automated test **equipment** and **device under test**.

## Installation
- Install ACBBS :
	```sh
	$ git clone ...
	```
	```sh
	$ cd acbbs
	```
	```sh
	$ python setup.py install
	```
- Add your user in specific group :
	```sh
	$ sudo usermod -a -G syslog user
	```

## Configuration
Before to execute scripts, edit the acbbs configuration according to that you wanna do by editing theses files :

 - **configuration.json** : global configuration. Configure ate parameters (IP, cables loss, etc...). Edit Scheduler section to set testcases to play and at which temperature. Don't forget to configure database IP and parameters.
 - **configuration_TAPMVx.x.json** : individual test case configuration depending of DUT.

## Logs
Scripts and drivers store all of theses log in **/var/log/acbbs/**.
To have all logs in real time in a specific terminal, enter this command :
```sh
$ tail -f /var/log/acbbs/allCarac.log
```
## Execute
To start scripts enter the following command :
```sh
$ python scheduler.py -d TAPMVx.x
```
Where **"TAPMVx.x"** can be TAPMV3.0 or TAPMV4.0

## ToDo
- **Climatic Chamber** drivers.
