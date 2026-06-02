#BLOCK.1(the setup)
import sqlite3
import pandas as pd

#1.for password encryption
def encrypt(text):
    return "".join(chr(ord(c) + 5) for c in text)

#2.for password decryption
def decrypt(text):
    return "".join(chr(ord(c) - 5) for c in text)

# 1.OPEN OR MAKING FILE
db = sqlite3.connect("smart_vault.db")
cursor = db.cursor()

# 2.CREATE TABLE IN FILE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Vault (
    site TEXT, 
    ID TEXT, 
    password TEXT
)
""")
db.commit()

print(" Database ready hai!")

#BLOCK.2(data entry)
def add_password():
    site = input("enter site/app name: ")
    user_id = input("enter your id here: ")
    passwd = input("enter password: ")
    safe_pass = encrypt(passwd)
    cursor.execute("INSERT INTO vault VALUES (?, ?, ?)", (site, user_id, safe_pass))
    db.commit()
    print(f"{site} password succesfully saved")

#BLOCK.3( the viewer(pandas))
def show_table():
    query = "SELECT * FROM vault ORDER BY site ASC"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print("\nvault is empty")
    else:
        print("__your saved passwords__")
        print(df)
        df['password'] = df['password'].apply(decrypt)

#BLOCK.3(Search function)
def search_site():
    site_name = input("enter site/app name: ").lower()
    query = f"SELECT * FROM vault WHERE LOWER(site) = '{site_name}'"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print(f"\n__'{site_name}' is not in list__")
    else:
        print(f"these ID's found in '{site_name}'")
        print(df)
        df['password'] = df['password'].apply(decrypt)
while True:
    print("\n__PASSWORD MANAGER__")
    print("1. Add passwords")
    print("2. Show all passwords")
    print("3. Search site for passwords")
    print("4. Exit")
    
    choice = input("Select Option From 1-4: ")
    
    if choice == '1':
        add_password()
    elif choice == '2':
        show_table()
    elif choice == '3':
        search_site()
    elif choice == '4':
        print("__PROGRAM CLOSED__")
        break
    else:
        print("Invalid Option, Try Again")