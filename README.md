
# Automatic Characterization Bench Base Stations

  

This package is a library that provides functions to drive automated test **equipment** and **device under test**.

  

## Installation

Install ACBBS :

    $ git clone ...
	$ cd acbbs
	$ python setup.py install

Add your user in specific group :

    $ sudo usermod -a -G syslog user

  

## Configuration

ACBBS will search its configuration from a database. So, before to launch ACBBS, you need to put at least one configuration into database. For it, you should use **configuration_assistant.py**:

For help :

    $ python configuration_assistant.py -h

For add configuration :
  
    $ python configuration_assistant.py -w configuration_TAPMV4.0.json

## Logs

Scripts and drivers store all of theses log in **/var/log/acbbs/**.

To have all logs in real time in a specific terminal, enter this command :

    $ tail -f /var/log/acbbs/allCarac.log

## Execute

Use **scheduler.py** for launch testcases. For display help :

    $ python scheduler.py -h

To launch it :

    $ python scheduler.py -d configuration_TAPMV4.0 --channel 1,2 -m "TEST"

Where :

 - --channel can be 1,2,3,4,5,6,7,8 and correspond of available channel.
 - -m is the comment.
 - -d is configuration we will use

For list all available configuration use :

    $ python configuration_assistant.py -l
