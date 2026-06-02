#BLOCK.1(the setup)
import sqlite3
import pandas as pd
import hashlib
import sys

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
cursor.execute("""
CREATE TABLE IF NOT EXISTS security (
    key_hash TEXT
)
""")
db.commit()

print("__Database is Ready!__")

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def encrypt(text, shift):
    return "".join(chr(ord(c) + shift) for c in text)

def decrypt(text, shift):
    return "".join(chr(ord(c) - shift) for c in text)

def auth():
    cursor.execute("SELECT key_hash FROM security")
    row = cursor.fetchone()
    if row is None:
        print("__Setup Your Master Key__")
        new_key = input("Enter Your Master Key: ")
        cursor.execute("INSERT INTO security VALUES (?)", (get_hash(new_key), ))
        db.commit()
        return new_key
    else:
        entered_key = input("\nEnter Master Key To Unlock: ")
        if get_hash(entered_key) == row[0]:
            print("\n__Access Granted__")
            return entered_key
        else:
            print("__Access Denide: Invalid Master Key__")
            sys.exit()

master_key = auth()
shift = ord(master_key[0])

#BLOCK.2(data entry)
def add_password():
    site = input("Enter Site/App Name: ").lower()
    user_id = input("Enter Your Id Here: ")
    passwd = input("Enter Password: ")
    safe_pass = encrypt(passwd, shift)
    cursor.execute("INSERT INTO Vault VALUES (?, ?, ?)", (site, user_id, safe_pass))
    db.commit()
    print(f"\n__'{site.capitalize()}' Password Succesfully Saved__")

#BLOCK.3( the viewer(pandas))
def show_table():
    query = "SELECT * FROM Vault ORDER BY site ASC"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print("\n__Vault Is Empty__")
    else:
        print("__Your Saved Passwords__")
        print("-•" * 15)
        df['password'] = df['password'].apply(lambda x: decrypt(x, shift))
        df.index = df.index + 1
    print(df.to_string(index=True))

#BLOCK.3(Search function)
def search_site():
    site_name = input("Enter Site/App Name: ").lower()
    query = f"SELECT * FROM vault WHERE LOWER(site) = ?"
    df = pd.read_sql_query(query, db, params = (site_name, ))
    if df.empty:
        print(f"\n__'{site_name.capitalize()}' is not in list__")
    else:
        print(f"These ID's Found In '{site_name.capitalize()}'")
        df['password'] = df['password'].apply(lambda x: decrypt(x, shift))
        df.index = df.index + 1
    print(df.to_string(index=True))

def delete_account():
    site = input("Enter Site/App Name For Deletation: ").lower()
    user_name = input("Enter ID For Deletation: ")
    cursor.execute("SELECT * FROM Vault WHERE site = ? AND ID = ?", (site, user_name))
    if cursor.fetchone() is None:
        print(f"__'{user_name}' Account Not Found In '{site}'__")
    else:
        cursor.execute("DELETE FROM Vault WHERE site = ? AND ID = ?", (site, user_name))
    db.commit()
    print(f"\n__'{site.capitalize()}' ({user_name}) Succesfully Deleted__")

def change_master_key():
    global shift, master_key
    print("Master Key Changing")
    old_key = input("Enter Current Master Key: ")
    if get_hash(old_key) != get_hash(master_key):
        print("__Invalid Master Key__")
        return
    new_key = input("Enter New Master Key: ")
    new_shift = ord(new_key[0])
    cursor.execute("SELECT * FROM Vault")
    rows = cursor.fetchall()
    for row in rows:
        site, user, old_enc_pwd = row
        real_pwd = decrypt(old_enc_pwd, shift)
        new_enc_pwd = encrypt(real_pwd, new_shift)
        cursor.execute("UPDATE Vault SET password=? WHERE site=? AND ID=?",(new_enc_pwd, site, user))
        cursor.execute("UPDATE security SET key_hash=?", (get_hash(new_key), ))
        db.commit()
        master_key = new_key
        shift = new_shift
        print("__Master Key Changed__")

while True:
    print("\n")
    print("•~" * 30)
    print("__PASSWORD MANAGER__")
    print("1. Add Passwords")
    print("2. Show All Passwords")
    print("3. Search Site For Passwords")
    print("4. For Delete Site/Password")
    print("5. For Change Master Key")
    print("6. Exit")
    print("\n")
    print("-" * 30)
    choice = input("Select Option From 1-6: ")
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
        change_master_key()
    elif choice == '6':
        print("__PROGRAM CLOSED__")
        break
    else:
        print("__Invalid Option, Try Again__")