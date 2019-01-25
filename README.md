
# Automatic Characterization Bench Base Stations

  

This package is a library that provides functions to drive automated test **equipment** and **device under test**.

  

## Installation

Install ACBBS :

    $ pip install git+https://lchagnoleau@bitbucket.sigfox.com/scm/acbbs/acbbs.git

Add your user in specific group :

    $ sudo usermod -a -G syslog user

  

## Configuration

ACBBS will search its configuration from a database. So, before to launch ACBBS, you need to put at least one configuration into database. For it, you should use **acbbs-config**:

For help :

    $ acbbs-config -h

For add configuration :
  
    $ acbbs-config -w configuration_TAPMV4.0.json

## Logs

Scripts and drivers store all of theses log in **/var/log/acbbs/**.

To have all logs in real time in a specific terminal, enter this command :

    $ tail -f /var/log/acbbs/allCarac.log

## Execute

Use **acbbs-scheduler** for launch testcases. For display help :

    $ acbbs-scheduler -h

To launch it :

    $ acbbs-scheduler -d configuration_TAPMV4.0 --channel 1,2 -m "TEST"

Where :

 - --channel can be 1,2,3,4,5,6,7,8 and correspond of available channel.
 - -m is the comment.
 - -d is configuration we will use

For list all available configuration use :

    $ acbbs-config -l
