# BLOCK.1(the setup)
import sqlite3
import pandas as pd
import hashlib
import sys
import os

# Database path fix (CodeBox ke folder mein hi bane)
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "smart_vault.db")

db = sqlite3.connect(db_path)
cursor = db.cursor()

# Tables creation
cursor.execute("CREATE TABLE IF NOT EXISTS Vault (site TEXT, ID TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS security (key_hash TEXT)")
db.commit()

# Helper Functions
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def encrypt(text, shift):
    return "".join(chr(ord(c) + shift) for c in text)

def decrypt(text, shift):
    return "".join(chr(ord(c) - shift) for c in text)

# Global Variables logic
master_key = None
shift = 0

def auth():
    global master_key, shift
    cursor.execute("SELECT key_hash FROM security")
    row = cursor.fetchone()
    
    if row is None:
        print("\n" + "-"*25 + "\n__Setup Your Master Key__\n" + "-"*25)
        new_key = input("Enter Your Master Key: ")
        cursor.execute("INSERT INTO security VALUES (?)", (get_hash(new_key), ))
        db.commit()
        master_key = new_key
    else:
        entered_key = input("\nEnter Master Key To Unlock: ")
        if get_hash(entered_key) == row[0]:
            print("\n__Access Granted__")
            master_key = entered_key
        else:
            print("__Access Denied: Invalid Master Key__")
            return False
            
    shift = ord(master_key[0])
    return True

# --- NEW WRAPPER FUNCTIONS FOR CODEBOX ---
# Ye functions user se input lenge taaki CodeBox error na de

def run_encrypt():
    
    """CodeBox se seedha chalane ke liye wrapper"""
    if not auth(): return
    text = input("Enter text to Encrypt: ")
    s = int(input("Enter shift (number): "))
    print(f"🔒 Encrypted: {encrypt(text, s)}")

def run_decrypt():
    """CodeBox se seedha chalane ke liye wrapper"""
    if not auth(): return
    text = input("Enter text to Decrypt: ")
    s = int(input("Enter shift (number): "))
    print(f"🔓 Decrypted: {decrypt(text, s)}")

# BLOCK.2(data entry)
def add_password():
    if not auth(): return
    print("\n")
    site = input("Enter Site/App Name: ").lower()
    user_id = input("Enter Your Id Here: ")
    passwd = input("Enter Password: ")
    safe_pass = encrypt(passwd, shift)
    cursor.execute("INSERT INTO Vault VALUES (?, ?, ?)", (site, user_id, safe_pass))
    db.commit()
    print(f"\n__'{site.capitalize()}' Password Successfully Saved__")

# BLOCK.3(the viewer)
def show_table():
    if not auth(): return
    query = "SELECT * FROM Vault ORDER BY site ASC"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print("\n__Vault Is Empty__")
    else:
        print("__Your Saved Passwords__\n" + "-•" * 15)
        df['password'] = df['password'].apply(lambda x: decrypt(x, shift))
        df.index = df.index + 1
        print(df.to_string(index=True))

def search_site():
    if not auth(): return
    site_name = input("Enter Site/App Name: ").lower()
    query = "SELECT * FROM vault WHERE LOWER(site) = ?"
    df = pd.read_sql_query(query, db, params=(site_name,))
    if df.empty:
        print(f"\n__'{site_name.capitalize()}' is not in list__")
    else:
        df['password'] = df['password'].apply(lambda x: decrypt(x, shift))
        df.index = df.index + 1
        print(df.to_string(index=True))

def delete_account():
    if not auth(): return
    print("\n")
    site = input("Enter Site/App Name: ").lower()
    user_name = input("Enter ID: ")
    cursor.execute("DELETE FROM Vault WHERE site = ? AND ID = ?", (site, user_name))
    db.commit()
    print(f"\n__'{site.capitalize()}' ({user_name}) Successfully Deleted__")

def function_calls():
    """Main Menu of Password Manager"""
    while True:
        print("\n" + "•~" * 15 + "\n__PASSWORD MANAGER__\n1. Add \n2. Show \n3. Search \n4. Delete \n5. Exit")
        print("-"*15)
        choice = input("Select Option: ")
        print("-"*15)
        if choice == '1': add_password()
        elif choice == '2': show_table()
        elif choice == '3': search_site()
        elif choice == '4': delete_account()
        elif choice == '5':
            print("__manager closed__")
            break
            
        else:
            print("invalid option")

if __name__ == "__main__":
    function_calls()