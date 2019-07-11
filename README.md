
# Automatic Characterization Bench Base Stations

  

This package is a library that provides functions to drive automated test **equipment** and **device under test**.

  

## Installation

Install ACBBS :

    $ pip install git+https://{USER}@bitbucket.sigfox.com/scm/acbbs/acbbs.git

Add your user in specific group :

    $ sudo usermod -a -G syslog user

## Logs

Scripts and drivers store all of theses log in **/var/log/acbbs/**.

To have all logs in real time in a specific terminal, enter this command :

    $ tail -f /var/log/acbbs/allCarac.log


Install IHMWEB :

    ## install nginx
    $ sudo apt-get install nginx
    ## configure nginx
    touch /etc/nginx/sites-available/ihmweb-acbbs
    cp the follow configuration:
    server {	
        listen 80; server_name 10.30.3.18; 
        root /home/sigfox/git/ihmweb/ihmweb_acbbs/;
	location = /favicon.ico { access_log off ; log_not_found off; }
        location /static/ {
                alias /home/sigfox/git/ihmweb/ihmweb_acbbs/static/;
                autoindex on;
        	}
	location /ws/progress { 
        	proxy_pass http://127.0.0.1:8000/ws/progress;
		proxy_http_version 1.1;
    		proxy_set_header Upgrade $http_upgrade;
    		proxy_set_header Connection "Upgrade";
        	}
	location /ws/calibprogress {
		proxy_pass http://127.0.0.1:8000/ws/calibprogress;
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "Upgrade";
		}
	location / {
        	proxy_set_header Host $http_host;
        	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        	proxy_redirect off;
        	proxy_pass http://127.0.0.1:8000;
        	}
	}
     create a link with ln to /etc/nginx/sites-enable
     start nginx with sudo service nginx start
     ## run server
     run  daphne in the virtual environnement of the project with the cmd : daphne -p 8000 -b 127.0.0.1 test_bench.asgi:application


## ACCES TO THE IHM

    open your navigator on the local network with the follow url : 10.30.3.18/home/


