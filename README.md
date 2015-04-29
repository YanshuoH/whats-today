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

## Deploiement (ENV: Centos 7)
Assuming you have MySQL, PYTHON 2.6+, Apache etc already.
* Git clone
* ```virtualenv flask```
* ```flask/bin/pip install -r requirements.txt```
* ```flask/bin/pip install mysql-python```
* Setup env variable for DB path :
  * ```$ WHATSTODAY_DATABASE_URL=mysql://example:example@localhost/example```
  * Then write it to the ENV ```export WHATSTODAY_DATABASE_URL```
