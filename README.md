# task_manager

Basic Backend-API for task manager.

## Installation Guide
1\. Clone the repo:
> $ git clone https://github.com/Ineshin-exe/task_manager.git

2\. Set your parameters in follow files:
- "docker-compose.yml"
- "./task_manager/.env"

3\. Build and up with docker-compose:
> $ docker-compose up -d --build

4\. Database's migrations:
> $ docker-compose exec web python manage.py makemigrations 

> $ docker-compose exec web python manage.py migrate

5 (Optional). Run tests:
> $ docker-compose exec web python manage.py test



## API Guide
### 1. Authentication:

### POST /api/auth/registration/
Register new user in database. Returns an API-key.

#### JSON params
|Field|Type|Description|
|---------|--------|----------------|
|nickname |string  |User's nickname|
|password1|string  |User's password|
|password2|string  |Password repeat|

### POST /api/auth/login/
Returns an API-key.

#### JSON params
|Field|Type|Description|
|--------|--------|----------------|
|nickname|string  |User's nickname|
|password|string  |User's password|



### 2. Task object:
#### Task structure
|Field|Type|Description|
|------|-----------------|---------|
|owner      |user    |User object. (Read-only)|
|id         |integer |Id of the task. (Read-only)|
|title      |string  |Task's title. Max_length = 64.|
|description|string  |Task's description.|
|createdAt  |string  |Date-Time field, format: DD-MM-YYYY HH-MM-SS|
|deadline   |string  |Date field, format: DD-MM-YYYY|
|status     |string  |One of status: **New**, **Planned**, **In progress**, **Completed**|

#### Authentication requires with API-key.
|Key|Value|
|--------|--------|
|Authorization|Token {API-Key}|

### GET /api/task-list/
Returns a list of task objects.  
##### Can be filtered by **deadline** or/and **status**  
> example URL: /api/task-list/?status=New&deadline=2020-09-30

### POST /api/task-create/
Create a new task object.

### GET /api/task/{id}/
Returns a task object.

### PATCH /api/task/{id}/
Modify a task object. Returns a modified task object on success.

### DELETE /api/task/{id}/
Delete a task object. Returns message on success.

### 3. Changelog object
#### Changelog structure
|Field|Type|Description|
|------|-----------------|---------|
|id        |integer|Id of changelog.|
|changeTime|string |Time of task's changelog.|
|data      |string |Last revision of parent task. Data in JSON format.|
|task      |integer|Id of parent task.|

#### Field "data" structure
|Field|Type|Description|
|-----------|--------|---------|
|title      |string  |Task's title. Max_length = 64|
|description|string  |Task's description.|
|deadline   |string  |Date field, format: DD-MM-YYYY|
|status     |string  |One of status: **New**, **Planned**, **In progress**, **Completed**|

### GET /api/task/{id}/changelog/
Returns a changelog object by task id.
