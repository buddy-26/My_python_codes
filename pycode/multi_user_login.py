import hashlib
import json
import os

DATABASE_FILE = "user_data.txt"

# step1 & 2: Functions (0 Spaces)
def load_users():
    if not os.path.exists(DATABASE_FILE):
        return {}
    try:
        with open (DATABASE_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("[WARNING] Invalid text format or empty file.")
        return {}
    except Exception as e:
        print(f"[ERROR]: {e}")
        return{}

def save_users(data):
    try:
        with open (DATABASE_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"\n[INFO] {len(data)} users data saved in {DATABASE_FILE}")
    except Exception as e:
        print(f"[ERROR] Data save karne mein problem: {e}")

# -------------------------------------------------------------
# step3: MAIN PROGRAM EXECUTION (0 Spaces)
# -------------------------------------------------------------
user_data = load_users()
is_running = True

while is_running:
    # 4 Spaces: Main Menu
    print("\n-------------------------------------------")
    print("--- MULTI USER LOGIN SYSTEM ---")
    print("mode menu: [1]: sign up | [2]: log in | [3]: exit")
    choice = input("select your mode: ")
    
    # -------------------------------------------------------------
    # SIGN UP (choice == '1')
    if choice == '1': # <-- 4 Spaces
        print ("\n ___sign up___")
        new_email = input("enter your email: ").lower()
        
        # Logic Fix: If registered, continue. Else, proceed.
        if new_email in user_data:
            print ("\n[ERROR] this email is already signed up")
            continue # <-- 12 Spaces: Loop will restart
            
        # Password setting logic (8 Spaces)
        new_password = input("enter new password: ")
        encode_new_password = new_password.encode('utf-8')
        new_password_hash = hashlib.sha256(encode_new_password).hexdigest()
        
        user_data[new_email] = new_password_hash
        print ("\n___signup successful___")
        
    # -------------------------------------------------------------
    # LOGIN (choice == '2')
    elif choice == '2': # <-- 4 Spaces
        print ("\n ___login___")
        login_email = input("login your email: ").lower()
        
        # 1. Email Check
        if login_email not in user_data:
            print ("[DENIED] Invalid email or not registered.")
            continue # <-- 12 Spaces: Loop will restart
            
        # 2. Password Check Logic (8 Spaces)
        stored_hash = user_data[login_email]
        login_password = input("enter your login password: ")
        
        # Hashing logic
        encode_login_password = login_password.encode('utf-8')
        login_password_hash = hashlib.sha256(encode_login_password).hexdigest()
        
        # 3. Final Comparison
        if login_password_hash == stored_hash:
            print ("\n___login successful___")
        else: # <-- 8 Spaces
            print ("[incorrect password]")

    # -------------------------------------------------------------
    # EXIT (choice == '3')
    elif choice == '3': # <-- 4 Spaces
        save_users(user_data)
        is_running = False
        print ("\n___program ended___")
        
    # -------------------------------------------------------------
    # INVALID COMMAND (Else)
    else: # <-- 4 Spaces
        print ("\n[INVALID] invalid command. Please select 1, 2, or 3.")
