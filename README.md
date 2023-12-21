# python_orm
A python orm plugin for creating and managing Relation Database. The plugin creates tables, selects data from tables, inserts, updates, and deletes rows from tables. Has database migration functionality.

## Engine

The engine of the python_orm is an entry point of the plugin. The engine create connection, sql adapter, creates tables, runs migration. 
Creates engine:

```python
from python_orm import DbUrl, Engine

db_url = DbUrl(
    driver='psycopg2',
    host='localhost',
    database='test',
    user='postgres',
    password='1234',
    port='5432',
)
engine = Engine(db_url=db_url)
```

Supported drivers:
- psycopg2
- sqlite3

The engine class has a on_create entry point. the argument of this function is `create_table` function which you can use for creating tables. The `on_create` function is called once if your database was not initialized before. In other cases please use the `on_update` callback:

```python
from python_orm import Migration, Engine


def _on_create(create_tables):
    create_tables([User, Project])

engine = Engine(
    db_url=db_url, 
    version=1, 
    on_create=_on_create,
)
```

The engine class is also a migration entry point. You can pass the `version` of the database and the `on_update` callback to the Engine constructor:

```python
from python_orm import Migration, Engine

def _on_update(migration: Migration, old_version: int, current_version: int):
    pass

engine = Engine(
    db_url=db_url, 
    version=1, 
    on_update=_on_update,
)
```

## Migration

`Migration` class supports the following features: create the table, delete the table, add the column, delete the column, and rename the table.

### Create the table
Creates table by table tamplate(`Model`). The first arg is the table template.

```python
from python_orm import Model, Column, Integer, Migration, Engine
class Test(Model):
    __tablename__ = 'test'
    value = Column(name='value', type=Integer())
        
def _on_update(migration: Migration, old_version: int, current_version: int):
    migration.create_table(Test)
    
engine = Engine(db_url, 1, on_update=migrate)
```

### Delete the table
Deletes table by table name. The first arg is the table name.

```python
from python_orm import Migration, Engine
     
def _on_update(migration: Migration, old_version: int, current_version: int):
    migration.delete_table('test')
    
engine = Engine(db_url, 1, on_update=migrate)
```

### Add the column
Addes volumn(`Column`) to table by table name. The first arg is the table name. The second args is the column.

```python
from python_orm import Column, String, Migration, Engine
     
def _on_update(migration: Migration, old_version: int, current_version: int):
    migration.add_column('test', Column(name='value2', type=String()))
    
engine = Engine(db_url, 1, migrate)
```

### Delete the column
Deletes the column by table name. The first arg is the table name. The second arg is the column name. 

```python
from python_orm import Column, String, Migration, Engine
     
def _on_update(migration: Migration, old_version: int, current_version: int):
    migration.delete_column('test', 'value')
    
engine = Engine(db_url, 1, migrate)
```

### Rename the table
Renames the table name. The first arg is the current table name. The second arg is the new table name.

```python
from python_orm import Column, String, Migration, Engine
     
def _on_update(migration: Migration, old_version: int, current_version: int):
    migration.change_table_name('test', 'test1')
    
engine = Engine(db_url, 1, migrate)
```

## Close connection

Use `engine.disconnect`

## Drop all tables

Use `engine.drop_all_tables`

## Creating tables.

Next time please use migration capability.
If you need to manually run creating all tables you should call `engine`.`create_all_tables`.

## Table Tamplates.

To create a table template you should declare the class with Model parent:

```python
from python_orm import Model

class Test(Model)
```

To add a column you should add a `Column` argument:

```python
from python_orm import Model, Class, String

class Test(Model)
    value = Column(name='value', type=String())
```


Column types supports: `Integer`, `String`, `PrimaryKey`, `DATETIME`, `BOOLEAN`.

To add the table name you should add a `__tablename__` argument:
```python
from python_orm import Model, Class, String

class Test(Model)
    __tablename__ = 'test'
    value = Column(name='value', type=String())
```

To add a Foregn key, please add a `ForignKey` argument:

```python
from python_orm import Model, Class, String, ForignKey

class Test(Model)
    value = Column(name='value', type=Integer())
    __forignkey__ = ForignKey(
        name='fk_test', 
        key_column='value',
        parent_table='test2'
        parent_key_columns='value',
        ondelete='ON CASCADE',
        onupdate='ON UPDATE'
    )
```

If you need to add more than one foreign key just create a list of foreign keys or a second foreign key argument.

## Session
The session creates the database cursor for executing SQL stmp and queries. 

The session is created by the engine:

```python
from python_orm import create_session

session = create_session(engine)
```

Then you should `connect` and `disconnect` the session:

```python
from python_orm import create_session

session = create_session(engine)

session.connect()
# do something
session.disconnect()
```

Or use like a context manager:

```python
from python_orm import create_session

with create_session(engine) as session:
    # do something
```

### Queries

Using the session you can create the quries and then get `first` or `all` Models.

```python
# Fetch the first Model by query.
session.query(User).first()
# or
# Fetch all Models by query.
session.query(User).all()
```

Method `session.query` return `Query` object that allows calls to other `Query` methods.

`where` method. Add where condition to the query. The first argument is the `Column`. The second argument is a value. The third (optional) argument is `condition`, `'='` by default. It should be called before `or_` or `and_`:

```python
users = session.query(User).\
        where(User.email, 'alexm1@str.com').\
        all()
```

`or_` method. Adds 'or' condition to the query. The first argument is the `Column`. The second argument is a value. The third (optional) argument is `condition`, `'='` by default. It should be called after `where_`:

```python
users = session.query(User).\
        where(User.email, 'alexm1@str.com').\
        or_(User.email, 'alexm2@str.com').\
        all()
```

`and_` method. Adds 'and' condition to the query. The first argument is the `Column`. The second argument is a value. The third (optional) argument is `condition`, `'='` by default. It should be called after `where_`:

```python
users = session.query(User).\
        where(User.email, 'alexm1@str.com').\
        and_(User.email, 'alexm2@str.com').\
        all()
```

`limit` method. Adds limit to the query. The first argument is the limit:

```python
users = session.query(User).\
        where(User.email, 'alexm1@str.com').\
        limit(1).\
        all()
```

## Insert

Using the session you can insert item or items to the table.

### Insert item

`session.insert_item` inserts item to the table. Should call `commit` to commit of inserting. Returns an id if the id is auto-incrementing.

```python
now = datetime.now()
item = User(
    age=18,
    email='alexm@str.com',
    is_admin=True,
    create_at=now,
)

id = session.insert_item(item).commit()
```

### Insert items

`session.insert_items` inserts items to the table. Should call `commit` to commit of inserting. Returns an ids if the id is auto-incrementing.

```python
now = datetime.now()
item = User(
    age=18,
    email='alexm@str.com',
    is_admin=True,
    create_at=now,
)

ids = session.insert_items([item]).commit()
```

## Updating

Using the session you can update items in the table. The first arg is a model type. The second arg is the dictionary of updating columns.

```python
session.update(User, {'age': 25}).\
    commit()
```

You can use `where`, `and_`, `or_` methods for specifying updating items. Working similar to `Queries`.`where`, `and_`, `or_` methods. 

## Deleting

Using the session you can delete items in the table. The first arg is a model type.

```python
session.delete(User).\
    where(User.email, 'alexm1@str.com').\
    commit()
```

You can use `where`, `and_`, `or_` methods for specifying deleting items. Working similar to `Queries`.`where`, `and_`, `or_` methods. 

## Table information

Using the session you can get columns or constraints information of the table. The first arg is a model type.

Information about columns:
```python
infos = session.table_info(User).columns_info()
```

Information about constrains:
```python
infos = session.table_info(User).constrains_info()
```