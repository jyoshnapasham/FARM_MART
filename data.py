import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (Fullname TEXT, Email TEXT, password TEXT, confirmpassword TEXT)')
print ("Table created successfully")
conn.close()