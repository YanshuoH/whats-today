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
