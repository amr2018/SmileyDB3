# SmileDB

SmileDB is a library built on sqlite3 to make working with databases easier

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O4O1TUHOK)

## Install
```
pip install SmileDB
```

## Usage:
To use the SmileDB class, you would typically instantiate an object of the class and provide the path or name of the SQLite database file as a parameter. For example:


```python
from SmileDB import SmileDB
db = SmileDB("mydatabase.db")
```

You can then call the `table()` method on the db object to create a new table in the database:


```python
my_table = db.table("my_table")
```

The `table()` method returns a Table object (my_table in this example) that can be used to perform operations on the created table.



## Insert or add new record

```python

db = SmileDB('database.db')

tasks = db.table('tasks')

tasks.Insert(
    data = {
        'name': 'This is task name 2', 
        'description': 'This task description 2',
        'coins': 50,
        'workers': 80
    }
)

```

## Insert list of data

```python
list_data = [
    {'name': 'test 1', 'description': 'test 1', 'coins': 50, 'workers': 10},
    {'name': 'test 2', 'description': 'test 2', 'coins': 500, 'workers': 20},
    {'name': 'test 3', 'description': 'test 3', 'coins': 100, 'workers': 50},
    {'name': 'test 4', 'description': 'test 4', 'coins': 5000, 'workers': 80}
]

tasks.InsertMany(data_list=list_data)
```

# If you want to make a login system, SmileDB makes it easy for you.

Register a new user 

```python
db = SmileDB('database.db')

users = db.table('users')

users.Register(data = {'email': 'test@example.com', 'password': '2020'})

```

# Note
By default, the function 'Register' makes a hash for any password automatically.
If you want to keep it as plain text, make sure that the value of 
'password_hash' argument is False


```python
db = SmileDB('database.db')

users = db.table('users')

users.Register(
    data = {'email': 'test666@example.com', 'password': '2020'},
    password_hash = False
)

```

## Login 

```python
db = SmileDB('database.db')

users = db.table('users')


result = users.LogIn(
    data = {'email': 'test666@example.com', 'password': '2020'},
)

print(result)
```

## Result
```
{'_index': 3, 'email': 'test666@example.com', 'password': '2020', 'uuid': '2626a962-d5d7-49fa-98f1-53d4bd722ee9', 'created_at': '2024-07-11 11:10:46.319231'}
```


## Get all records
```python
print(tasks.GetALL())
```

## Get records by id
```python
print(tasks.GetByID(uuid='e927c787-bf9a-4ec7-b575-2efacd90728e'))
```

## Get records by any column like name
```python
print(tasks.GetBy(name = 'This is task name'))
```
You can use also `FindBy` or `FilterBy` function it will give you the same result

## Get one record by any column like workers in this example

```python
tasks = db.table('tasks')
print(tasks.FindOne(workers = 80))
```

## Result

```
{'_index': 4, 'name': 'test 4', 'description': 'test 4', 'coins': 5000, 
'workers': 80, 'uuid': '1fad0ed8-fbbc-4fc9-8e46-3f6c355dbf84', 'created_at': '2024-07-11 10:42:26.818831'}
```


## Filtring records by any column

use `larger_than`, `less_than`, `not`, `equal`, `range`

```python
print(tasks.Filter(filter_keys = {'coins': {'less_than': 50}}))
```

## example of how to use `range` filter

```python
result = tasks.Filter(filter_keys={'workers': {'range': [20, 80]}})
print(result)
```

## Result
```
{'range': [
    {'_index': 2, 'name': 'test 2', 'description': 'test 2', 'coins': 500, 'workers': 20, 'uuid': 'ef0b06ce-1abd-46db-836c-166b57cc57e7', 'created_at': '2024-07-11 10:42:26.599986'},

    {'_index': 3, 'name': 'test 3', 'description': 'test 3', 'coins': 100, 'workers': 50, 'uuid': '5fc3ddd0-4316-4de2-bdf7-c9536d487526', 'created_at': '2024-07-11 10:42:26.709459'}, 
    
    {'_index': 4, 'name': 'test 4', 'description': 'test 4', 'coins': 5000, 'workers': 80, 'uuid': '1fad0ed8-fbbc-4fc9-8e46-3f6c355dbf84', 'created_at': '2024-07-11 10:42:26.818831'}
]
}
```



## Update record by uuid
```python
result = tasks.Update(
    uuid='31c37a83-02db-4e8d-9d62-124888626892',
    data = {'coins': 1}
)

print(result)
```

## Result
```
{'_index': 5, 'name': 'This is task name 2', 'description': 'This task description 2', 'coins': 1, 'workers': 80, 'uuid': '31c37a83-02db-4e8d-9d62-124888626892', 'created_at': '2024-07-11 10:24:26.020235'}
```

## Update many by name or any other column name

```python
result = tasks.UpdateMany(
    data = {'coins': 1000},
    name = 'This is task name 2'
)

print(result)
```

## Result
```
[
    {'_index': 2, 'name': 'This is task name 2', 'description': 'This task description 2', 'coins': 1000, 'workers': 80, 'uuid': 'e927c787-bf9a-4ec7-b575-2efacd90728e', 'created_at': '2024-07-11 10:09:48.163728'}, 

    {'_index': 3, 'name': 'This is task name 2', 'description': 'This task description 2', 'coins': 1000, 'workers': 80, 'uuid': '9d74c2ea-b943-4aa9-bd06-52ba1beecc5b', 'created_at': '2024-07-11 10:23:49.426697'}, 
    
    {'_index': 4, 'name': 'This is task name 2', 'description': 'This task description 2', 'coins': 1000, 'workers': 80, 'uuid': '93ed7665-f6e3-40be-ab3b-8d609eaf1896', 'created_at': '2024-07-11 10:24:16.574957'}, 
    
    {'_index': 5, 'name': 'This is task name 2', 'description': 'This task description 2', 'coins': 1000, 'workers': 80, 'uuid': '31c37a83-02db-4e8d-9d62-124888626892', 'created_at': '2024-07-11 
    10:24:26.020235'
    }
]
```


## Delete record by uuid

```python
tasks.Delete(uuid='b3bd4856-28f2-4d24-aaca-c22724d2e0a1')
```


## Delete records by name or any other column name

```python
tasks.DeleteMany(
    name = 'This is task name 2'
)
```

# Credits

## sqlite3:
The sqlite3 library is part of the Python Standard Library, which means it is included with Python itself. You can import and use the sqlite3 module directly in your Python code without needing to install any additional

## bcrypt:
Modern password hashing for your software and your servers

