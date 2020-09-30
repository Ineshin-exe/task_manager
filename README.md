# task_manager
____



____
# API Guide

## Authentication

### POST /api/auth/registration/
Register new user in database. Returns a API-key.

#### JSON params
|Field|Type|Description|
|---------|--------|----------------|
|nickname |string  |Nickname of user|
|password1|string  |Password of user|
|password2|string  |Retype password |

### POST /api/auth/login/
Returns a API-key.

#### JSON params
|Field|Type|Description|
|--------|--------|----------------|
|nickname|string  |Nickname of user|
|password|string  |Password of user|

###

## Task object
#### Task structure
|Field|Type|Description|
|------|-----------------|---------|
|owner      |user    |User object. (Read-only)|
|id         |integer |Id of task. (Read-only)|
|title      |string  |Title of task. Max_length = 64|
|description|string  |Description of task.|
|createdAt  |string  |Date-Time field, format: DD-MM-YYYY HH-MM-SS|
|deadline   |string  |Date field, format: DD-MM-YYYY|
|status     |string  |One of status: **New**, **Planned**, **In progress**, **Completed**|

#### Requires authentication with API-key.
|Key|Value|
|--------|--------|
|Authorization|Token {API-Key}|

### GET /api/task-list/
Returns a list of task objects.
Can be filtered by **deadline** or/and **status**
example URL: /api/task-list/?status=New&deadline=2020-09-30

### POST /api/task-create/
Create a new task object.

### GET /api/task/{id}/
Returns a task object.

### PATCH /api/task/{id}/
Modify a task object. Returns a modified task object on success.

### DELETE /api/task/{id}/
Delete a task object. Returns message on success.
