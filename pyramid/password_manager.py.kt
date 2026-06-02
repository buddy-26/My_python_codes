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

print("__Database is ready__")

#BLOCK.2(data entry)
def add_password():
    site = input("Enter Site/App Name: ")
    user_id = input("Enter Your Id Here: ")
    passwd = input("Enter Password: ")
    safe_pass = encrypt(passwd)
    cursor.execute("INSERT INTO Vault VALUES (?, ?, ?)", (site, user_id, safe_pass))
    db.commit()
    print(f"__{site} Password Succesfully Saved__")

#BLOCK.3( the viewer(pandas))
def show_table():
    query = "SELECT * FROM Vault ORDER BY site ASC"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print("\n__Vault Is Empty__")
    else:
        print("__Your Saved Passwords__")
        print("-•" * 15)
        df['password'] = df['password'].apply(decrypt)
        df.index = df.index + 1
        print(df)

#BLOCK.3(Search function)
def search_site():
    site_name = input("Enter Site/App Name: ").lower()
    query = f"SELECT * FROM Vault WHERE LOWER(site) = '{site_name}'"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print(f"\n__'{site_name}' Is Not In List__")
    else:
        print(f"These ID's Found In '{site_name}'")
        df['password'] = df['password'].apply(decrypt)
        df.index = df.index + 1
        print(df)

#BLOCK.6 (DELETE ACCOUNT)
def delete_account():
    site = input("Enter Site/App Name For Deletation: ")
    user_name = input("Enter ID For Deletation: ")
    cursor.execute("DELETE FROM Vault WHERE site = ? AND ID = ?", (site, user_name))
    db.commit()
    print(f"\n__{site} ({user_name}) Succesfully Deleted__")

while True:
    print("\n")
    print("•~" * 30)
    print("__PASSWORD MANAGER__")
    print("1. Add Passwords")
    print("2. Show All Passwords")
    print("3. Search Site For Passwords")
    print("4. For Delete Site/Password")
    print("5. Exit")
    print("\n")
    print("-" * 30)
    choice = input("Select Option From 1-5: ")
    print("-" * 30)
    if choice == '1':
        add_password()
    elif choice == '2':
        show_table()
    elif choice == '3':
        search_site()
    elif choice == '4':
        delete_account()
    elif choice == '5':
        print("__PROGRAM CLOSED__")
        break
    else:
        print("Invalid Option, Try Again")