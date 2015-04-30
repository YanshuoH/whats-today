# whats-today
Vocabulary learning strategy

## Requirements
* Python 2.7
* Dev Enviroment: Windows 7, 8.1

## Installation
* Install virtualenv for dev: ``` easy_install virtualenv ```
* Install create virtual env_variables using virtualenv: ``` virtualenv flask ```
* Install moduels in file: flask_install, eg. ``` flask\Scripts\pip install flask ```
* Install npm modules: ``` npm install ```
  * Above that, for windows, modules like gulp and react-tools should be installed using ```-g```
* Install bower components: ``` bower install ```
* Compile jsx file to js: ```jsx app/static/jsx/ app/static/js/```
* Create basic database: ```flask/Scripts/python manager.py createdb```

## Run
* ``` flask/Scripts/python manager.py runserver ```
* Navigator: ``` http://localhost:5000  ```

## Developement
* Jsx watching: ```jsx --watch app/static/jsx/ app/static/js```

## Deploiement (ENV: Centos 7 - DigitalOcean)
Assuming you have MySQL, PYTHON 2.6+, Nginx etc already.

Principal thoughts explained in example of [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)

```the web client <-> the web server <-> the socket <-> uWSGI <-> Python```
* Use uWSGI run app with serveral workers
* Create socket to connect with Nginx
* Use Nginx as webserver

Here's how to proceed
* Git clone
* ```virtualenv flask```
* ```flask/bin/pip install -r requirements.txt```
* ```flask/bin/pip install mysql-python```
* Don't forget to follow the **installation** instructions:
* Setup env variable for DB path :
  * ```$ WHATSTODAY_DATABASE_URL=mysql://example:example@localhost/example```
  * Then write it to the ENV ```export WHATSTODAY_DATABASE_URL```
  * Create database user:
    ```
    mysql> create database whatstoday character set utf8 collate utf8_bin;
    mysql> create user 'whatstoday'@'localhost' identified by 'whatstoday';
    mysql> grant all privileges on whatstoday.* to 'whatstoday'@'localhost';
    mysql> flush privileges;
    mysql> quit;
    ```
  
  * Create database using createdb commande in manager.py
    ```
    DATABASE_URL=mysql://whatstoday:whatstoday@localhost/whatstoday 
    flask/bin/python manager.py createdb
    ```
* Setup uWSGI
  * Check your chown-socket in whatstoday.ini file, make sure it's ok for public (usually it's fine with chmod 664)
  * Create a service to handle the uWSGI process:
    ```sudo vim /etc/systemd/system/whatstoday.service```
  * Write something like this:
    ```
    Description=uWSGI instance to serve whatstoday
    After=network.target
    
    [Service]
    Group=apache
    WorkingDirectory=/home/user/apps/whats-today
    Environment="PATH=/home/user/apps/whats-today/flask/bin"
    ExecStart=/home/user/apps/whats-today/flask/bin/uwsgi --ini whatstoday.ini
    
    [Install]
    WantedBy=multi-user.target
    ```
  * Now you can start your socket:
    ``` 
    sudo systemctl start myproject
    sudo systemctl enable myproject
    ```
 * Setup Nginx
   * You may want to add a server block in 'conf.d' or 'sites-enabled' in Nginx
   * Here's an example:
     ```
     upstream whatstoday {
         server unix:/home/user/apps/whats-today/whatstoday.sock;
     }
 
     server {
         listen 8000;
         server_name 127.0.0.1;
 
         location / {
             include uwsgi_params;
             uwsgi_pass whatstoday;
         }
 
         location /static {
             alias /home/user/apps/whats-today/app/static;
         }
     }
     ```
   * Also make sure your Nginx runs by correct user-group

     ```
      sudo vim /etc/nginx/nginx.conf
      // In Nginx, an example
      user user apache;
     ```

   * Before running Nginx, check syntax ``` sudo nginx -t ```
   * Run Nginx

     ```
     sudo systemctl start nginx
     sudo systemctl enable nginx
     ```
   * http://YOUR_IP_OR_DOMAIN:8000/

## Always TODOS
* Use flask-cache - nginx to cache assets
* Minify react's JS files
* Logger
* Mailer system
* Pagination of list page
* Weibo connect
* Unit tests (for god's sake...)
