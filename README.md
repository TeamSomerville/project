# project

## API Setup

###Nginx
The nginx reverse proxy file is located at /etc/nginx/nginx.conf
To restart ```sudo systemctl restart nginx```

###Gunicorn
The application server is gunicorn and is listening on port 8000. The config file is at /etc/systemd/system/gunicorn.service
* To enable
```sudo systemctl enable gunicorn```
* to start
```sudo systemctl start gunicorn```
* to restart
```sudo systemctl restart gunicorn```
* to reload after code change
```sudo systemctl daemon-reload```
* to check the status
```sudo systemctl status gunicorn```

###Deployment
This is done through executing the deploy_api.sh script. This script will copy the api code to /project/api by deleting the target directories and doing a fresh copy. Subsequently the virtual environment is activated and gunicorn is reloaded.
After a successful deployment the website can browsed through http://sp21-cs411-07.cs.illinois.edu

