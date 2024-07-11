
from uuid import uuid4
from datetime import datetime

import sqlite3
import bcrypt
import html

def sanitize_data(data):
    clean_data = {}
    for k in data:
        value = data[k]
        if isinstance(value, str):
            sanitized_value = html.escape(value)
            clean_data[k] = sanitized_value
        elif isinstance(value, int):
            clean_data[k] = value
        else:
            # Handle other data types as needed
            clean_data[k] = value

    return clean_data
        


class Table:
    def __init__(self, table_name, 
                 db: sqlite3.Connection, 
                 cursor : sqlite3.Cursor, make_uuid = True, created_at = True):
        self.table_name = table_name
        self.db = db
        self.cursor = cursor
        self.make_uuid = make_uuid
        self.created_at = created_at
        self.types = {
            "<class 'str'>": 'TEXT',
            "<class 'int'>": 'INTEGER',
            "<class 'bytes'>": 'BLOB',
            "INDEX": 'INTEGER PRIMARY KEY'
        }

    
    def get_types(self, data):

        if self.make_uuid:
            data['uuid'] = str(uuid4())
        
        if self.created_at:
            data['created_at'] = str(datetime.now())

        cols = []
        for k in data:
            cols.append(f'{k} {self.types[str(type(data[k]))]}')

        return ', '.join(cols)
    
    def get_column_names(self):
        column_names = self.cursor.execute(f'''SELECT * FROM 
        {self.table_name} LIMIT 1''').description

        return [description[0] for description in column_names]

    def Insert(self, data : dict):

        data = sanitize_data(data)

        q = f'''
            CREATE TABLE IF NOT EXISTS
            {self.table_name}

            (_index {self.types['INDEX']}, {self.get_types(data)})
        '''

        #print(q)

        self.cursor.execute(q)

        q = f'''
         INSERT INTO {self.table_name} ({','.join(data.keys())})
         VALUES ({','.join(['?' for _ in range(len(data.keys()))])})
        '''

        #print(q)

        self.cursor.execute(q, tuple([v for v in data.values()]))
        self.db.commit()

        return self.GetBy(**data)
    

    @classmethod
    def is_number_in_range(self, number, a, b):
        if number >= a and number <= b:
            return True
        else:
            return False


    
    def hash_password(self, password: str):
        return bcrypt.hashpw(
            password = password.encode(), salt = bcrypt.gensalt()
        )
    
    def check_password(self, password, hashed_password):
        password = password.encode()

        return bcrypt.checkpw(password, hashed_password)
   
    def show_results(self, results) -> list:
        rows = []

        for result in results:
            rows.append({k:v for k, v in zip(self.get_column_names(), result)})

        return rows
    

    def InsertMany(self, data_list : list) -> list:
        for data in data_list:
            self.Insert(data = data)
        
        return self.GetALL()
    

    def Register(self, data, password_hash = True):

        # check if user is not exists by email
        try:
            if self.GetBy(email = data['email']):
                return False
        except sqlite3.OperationalError:
            pass
        
        if 'password' in data:
            if password_hash:
                data['password'] = self.hash_password(data['password'])
            
            data['password'] = data['password']
        
        
        self.Insert(data = data)
        return self.GetBy(email = data['email'])
    

    def LogIn(self, data):

        data = sanitize_data(data)

        # find the user by email
        user = self.FindOne(email = data['email'])
        if user:
            # get the hashed password of this user
            user_password = user['password']

            if isinstance(user_password, str):
                if data['password'] == user_password:
                    return user
                
                return

            if self.check_password(data['password'], user_password):
                return user
            
        
    
    
    def GetALL(self) -> list:
        results = self.cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()
        return self.show_results(results)
    

    def GetByID(self, uuid : str) -> dict:
        q = f'''
        SELECT * FROM {self.table_name} WHERE uuid = "{uuid}"
         '''
        result = self.cursor.execute(q).fetchone()
        self.db.commit()

        return {k:v for k, v in zip(self.get_column_names(), result)}
    
    def GetBy(self, **args) -> list:
        filter_key_vals = ''
        
        for k, v in args.items():
            filter_key_vals += f'AND {k} = "{v}" '

        # Remove the first and in text
        filter_key_vals = filter_key_vals[3:].strip()
        #print(filter_key_vals)

        q = f'''
        SELECT * FROM {self.table_name} WHERE {filter_key_vals}
         '''.strip()
        
        results = self.cursor.execute(q).fetchall()

        self.db.commit()
        return self.show_results(results)
    
    def FindBy(self, **args) -> list:
        return self.GetBy(**args)
    
    def FindOne(self, **args) -> dict:
        records = self.FindBy(**args)
        if records:
            return records[0]
    
    def FilterBy(self, **args) -> list:
        return self.GetBy(**args)
    
    def Filter(self, filter_keys : dict) -> dict:
        # Get all records
        records = self.GetALL()
        filtred_records = {}

        for column in filter_keys.keys():
            #print(column, filter_keys[column])

            if 'larger_than' in filter_keys[column]:
                value = filter_keys[column]['larger_than']
                if isinstance(value, int):
                    filtred_records['larger_than'] = [a for a in filter(lambda rec : rec[column] > value, records)] 
                
 

            if 'less_than' in filter_keys[column]:
                value = filter_keys[column]['less_than']
                if isinstance(value, int):
                    filtred_records['less_than'] = [a for a in filter(lambda rec : rec[column] < value, records)]

             
            if 'not' in filter_keys[column]:
                value = filter_keys[column]['not']
                if isinstance(value, int):
                    filtred_records['not'] = [a for a in filter(lambda rec : rec[column] != value, records)]


            
            if 'equal' in filter_keys[column]:
                value = filter_keys[column]['equal']
                if isinstance(value, int):
                    filtred_records['equal'] = [a for a in filter(lambda rec : rec[column] == value, records)]


            if 'range' in filter_keys[column]:
                value = filter_keys[column]['range']
                if isinstance(value, list):
                    a = value[0]
                    b = value[1]
                    filtred_records['range'] = [a for a in filter(
                        lambda rec : self.is_number_in_range(rec[column], a, b), 
                        records
                    )]

            
            
            
        return filtred_records
                        

                
    

    def Update(self, uuid, data: dict) -> dict:

        data = sanitize_data(data)
        

        filter_keys = ''
        
        for k in data:
            filter_keys += f'{k} = ? , '

        # remove the last , in 
        filter_keys = filter_keys[:-2]
        #print(filter_keys)

        q = f'''UPDATE {self.table_name} SET {filter_keys} 
        WHERE uuid = "{uuid}"  '''.strip()

        #print(q)

        self.cursor.execute(q, tuple([v for v in data.values()]))
        self.db.commit()

        return self.GetByID(uuid = uuid)
    

    def UpdateMany(self, data : dict, **args) -> list:
        records = self.GetBy(**args)
        for record in records:
            self.Update(uuid = record['uuid'], data = data)

        return self.FilterBy(**data)

    def Delete(self, uuid) -> bool:
        q = f'DELETE FROM {self.table_name} WHERE uuid = ?'
        self.cursor.execute(q, (uuid,))
        self.db.commit()

        return True
    

    def DeleteMany(self, **args) -> bool:
        records = self.GetBy(**args)
        for record in records:
            self.Delete(uuid = record['uuid'])

        return True
    

    

class SmileDB:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def table(self, table_name, make_uuid = True, created_at = True) -> Table:
        return Table(table_name, self.conn, self.cursor, make_uuid, created_at)
    

