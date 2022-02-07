## Restaurant Menu voting system

### Installation process (with Docker)

* Clone this repository
* Create a file `.env` and copy all data from `.env-sample` file
* Run this command: `docker-compose build`
* Run this command: `docker-compose up`
* Open another terminal and run `docker ps` and you will see list of containers and one will have name ending `_app_1`, copy the name
* Run this command `docker exec -it cornercase_task_app_1 bash`, here instead of cornercase_task_app_1, paste your copy name, this will open app container
* Now in the app container run below commands:
  * `python manage.py migrate`
  * `python manage.py createsuperuser` (provide username, email and password)
  * `python manage.py test` (Run all test cases)


### Installation process (without Docker)

* Clone this repository
* Create a file `.env` and copy all data from `.env-sample` file
* Create your virtual environment by `python3 -m venv venv`
* Turn it on
* Install all packages from `requirements.txt` file by this command `pip install -r requirements.txt`
* Create you postgresql database
* Open this file `core/config/local.py` and set database info
* Run all migrations by `python manage.py migrate`
* Create superuser by `python manage.py createsuperuser`
* Run all unit-test by `python manage.py test`
* Run the server `python manage.py runserver`
* Swagger doc: `http://localhost:8000/swagger/`


#### In your postman import `menu-voting API.postman_collection.json` for API collection