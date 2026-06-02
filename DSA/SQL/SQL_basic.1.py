# TOPIC: SQL Basics (SQLite3)
# Logic: Python ke andar hi database banana aur use manage karna.

#CRUD: Create, Read, Update, Delete

import sqlite3

# 1. Database se connect karo
conn = sqlite3.connect('automation_data.db')
cur = conn.cursor()

# 2. Table banao (C - Create)
cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, status TEXT)")

# 3. Data insert karo
cur.execute("INSERT INTO Users (name, status) VALUES ('Rahul', 'Active')")
conn.commit()

# 4. Data read karo (R - Read)
cur.execute("SELECT * FROM Users")
all_users = cur.fetchall()
print(f"Users in DB: {all_users}")

# 5. Data update karo (U - Update)
cur.execute("UPDATE Users SET status='Inactive' WHERE name='Rahul'")
conn.commit()

conn.close()
