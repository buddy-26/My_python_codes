# TOPIC: SQL Joins (Connecting Tables)
# Logic: Do alag-alag tables ka data unki common ID se match karke nikalna.

import sqlite3

conn = sqlite3.connect('company.db')
cur = conn.cursor()

# Maano do tables hain: Employees aur Departments
# Hum unhe 'dept_id' par join kar rahe hain
query = """
SELECT Employees.name, Departments.dept_name
FROM Employees
INNER JOIN Departments ON Employees.dept_id = Departments.id
"""

# cur.execute(query) 
# print(cur.fetchall())

conn.close()
