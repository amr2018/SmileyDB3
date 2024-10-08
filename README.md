# SmileyDB3

SmileyDB3 is a library built on sqlite3 to make working with databases easier

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O4O1TUHOK)

## Install
```
pip install SmileyDB3
```

## Usage:
To use the SmileyDB3 class, you would typically instantiate an object of the class and provide the path or name of the SQLite database file as a parameter. For example:


```python
db = SmileyDB3("mydatabase.db")
```

You can then call the `table()` method on the db object to create a new table in the database:


```python
my_table = db.table("my_table")
```

The `table()` method returns a Table object (my_table in this example) that can be used to perform operations on the created table.



## Insert or add new record

```python

db = SmileyDB3('database.db')

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

# If you want to make a login system, SmileyDB3 makes it easy for you.

Register a new user 

```python
db = SmileyDB3('database.db')

users = db.table('users')

users.Register(data = {'email': 'test@example.com', 'password': '2020'})

```

# Note
By default, the function 'Register' makes a hash for any password automatically.
If you want to keep it as plain text, make sure that the value of 
'password_hash' argument is False


```python
db = SmileyDB3('database.db')

users = db.table('users')

users.Register(
    data = {'email': 'test666@example.com', 'password': '2020'},
    password_hash = False
)

```

## Login 

```python
db = SmileyDB3('database.db')

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

use `larger_than`, `less_than`, `not`, `equal`, `between`

### example of how to use `less_than` filter

```python
tasks = db.table('tasks')


print(tasks.Filter(
    filter_keys = {'workers': {'less_than': 100}}
))

```

## Result

```
[{'key': 'workers', 'records': [{'_index': 13, 'workers': 10, 'coins': 20, 'uuid': '5dcabe12-17b3-4a64-928c-a524b6fb6479', 'created_at': '2024-08-11 12:41:05.248027'}, {'_index': 19, 'workers': 50, 'coins': 50, 'uuid': 'f1273e5b-c937-45e4-931c-d1b6d9f31a51', 'created_at': '2024-08-11 12:43:27.156194'}, {'_index': 20, 'workers': 50, 'coins': 50, 'uuid': 'b1c67c92-6a2d-4a72-84a1-b5466d3ca839', 'created_at': '2024-08-11 12:44:17.355148'}, {'_index': 21, 'workers': 50, 'coins': 50, 'uuid': '4b46f78c-98b0-4dad-84c7-ac76af218102', 'created_at': '2024-08-11 12:44:27.422767'}, {'_index': 22, 'workers': 80, 'coins': 500, 'uuid': 'f0eecddd-d046-4fd6-b441-9188a3d73985', 'created_at': '2024-08-11 12:44:38.911006'}, {'_index': 25, 'workers': 71, 'coins': 809, 'uuid': '484bb9e4-647b-4dc2-afac-c3e27a0e613e', 'created_at': '2024-08-11 12:47:30.265126'}, {'_index': 27, 'workers': 50, 'coins': 394, 'uuid': 'da2ee6b2-3653-4cae-b570-510d998f09a2', 'created_at': '2024-08-11 12:47:52.165459'}, {'_index': 29, 'workers': 99, 'coins': 817, 'uuid': 'a6d3b21c-b2ba-4530-9e09-35b00a37e493', 'created_at': '2024-08-11 12:48:34.145886'}, {'_index': 31, 'workers': 71, 'coins': 463, 'uuid': 'c71a7b11-9b3b-4787-89d2-d7f19904e228', 'created_at': '2024-08-11 
12:51:37.325311'}]}]

```

### example of how to use between filter

```python

tasks = db.table('tasks')


print(tasks.Filter(
    filter_keys = {'workers': {'between': [100, 200]}}
))

```

## Result

```
[{'key': 'workers', 'records': [{'_index': 1, 'workers': 200, 'coins': 20, 'uuid': '545145bc-c03e-4228-aece-d5a7e50c996f', 'created_at': '2024-08-11 12:27:05.446859'}, {'_index': 14, 'workers': 100, 'coins': 20, 'uuid': '6d84bceb-5f8f-464b-97b1-f6b46906149b', 'created_at': '2024-08-11 12:41:44.623149'}, {'_index': 15, 'workers': 200, 'coins': 20, 'uuid': '4e25ace6-b167-483d-97bc-6f765f324560', 'created_at': '2024-08-11 12:41:49.830534'}, {'_index': 16, 'workers': 200, 'coins': 20, 'uuid': 'c4542f0d-1238-4631-8518-02c3e67809dd', 'created_at': '2024-08-11 12:42:32.767674'}, {'_index': 17, 'workers': 200, 'coins': 20, 'uuid': '37e6e806-5567-4fc7-bdab-89f520314b5f', 'created_at': '2024-08-11 12:42:51.708270'}]}]
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

## Convert data to CSV, JSON, HTML, etc

```python
tasks.convert().to_csv('out.csv')
tasks.convert().to_json('out.json')
```


# Credits

## sqlite3:
The sqlite3 library is part of the Python Standard Library, which means it is included with Python itself. You can import and use the sqlite3 module directly in your Python code without needing to install any additional

## bcrypt:
Modern password hashing for your software and your servers

