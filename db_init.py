from msilib import schema
import sqlite3

db_connection = sqlite3.connect('database.db')



with open('db_schema.sql') as f:
    db_connection.executescript(f.read())
    


db_connection.commit()
db_connection.close()

