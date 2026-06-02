import sqlite3
import pandas as pd
import sys
import random
import string

# ==========================================
# BLOCK 1: MASTER SECURITY (Login Logic)
# ==========================================
MASTER_PIN = "7890"  # Aap ise badal sakte hain
print("--- 🛡️ WELCOME TO SECURE VAULT 🛡️ ---")
input_pin = input("Enter Master PIN: ")

if input_pin != MASTER_PIN:
    print("❌ Access Denied! Galat PIN.")
    sys.exit()

# ==========================================
# BLOCK 2: DATABASE CONNECTION (SQL)
# ==========================================
conn = sqlite3.connect('my_vault.db')
cur = conn.cursor()
# Primary Key 'site' ko banaya hai taki duplicates na ho
cur.execute("CREATE TABLE IF NOT EXISTS Vault (site TEXT PRIMARY KEY, password TEXT)")
conn.commit()

# ==========================================
# BLOCK 3: ENCRYPTION LOGIC (Security)
# ==========================================
# Ye function passwords ko "secret language" mein badalta hai
def encrypt(text):
    return "".join(chr(ord(c) + 5) for c in text)

# Ye function secret language ko wapas asli text banata hai
def decrypt(text):
    return "".join(chr(ord(c) - 5) for c in text)

# ==========================================
# BLOCK 4: PASSWORD GENERATOR (Automation)
# ==========================================
def generate_pass():
    length = 12
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for i in range(length))
    print(f"\n💡 Suggested Strong Password: {password}")
    return password

# ==========================================
# BLOCK 5: MAIN FUNCTIONS (CRUD Operations)
# ==========================================

# A. Password Add karna
def add_password():
    site = input("Enter Site/App Name: ").lower().strip()
    gen_choice = input("Do you want to generate a random password? (y/n): ").lower()
    
    if gen_choice == 'y':
        password = generate_pass()
    else:
        password = input(f"Enter password for {site}: ")
    
    secret_pass = encrypt(password)
    try:
        cur.execute("INSERT INTO Vault VALUES (?, ?)", (site, secret_pass))
        conn.commit()
        print(f"✅ Saved password for {site}!")
    except sqlite3.IntegrityError:
        print("⚠️ Error: Ye site pehle se hai. Update option use karein.")

# B. Table View (Pandas + Sorting)
def show_all():
    # ORDER BY site ASC se A-Z sort hota hai
    query = "SELECT * FROM Vault ORDER BY site ASC"
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("\n📭 Vault khaali hai!")
    else:
        # Decrypting each password for the display
        df['password'] = df['password'].apply(decrypt)
        print("\n--- YOUR SAVED PASSWORDS (Sorted A-Z) ---")
        print(df.to_string(index=False))

# C. Password Update karna
def update_password():
    site = input("Kiska password badalna hai?: ").lower().strip()
    cur.execute("SELECT site FROM Vault WHERE site = ?", (site,))
    
    if cur.fetchone():
        new_pass = input(f"Enter new password for {site}: ")
        secret_pass = encrypt(new_pass)
        cur.execute("UPDATE Vault SET password = ? WHERE site = ?", (secret_pass, site))
        conn.commit()
        print("🔄 Update Successful!")
    else:
        print("❌ Site nahi mili.")

# ==========================================
# BLOCK 6: MAIN MENU LOOP
# ==========================================
while True:
    print("\n" + "="*30)
    print("1. Add New Password")
    print("2. View All Passwords (Table)")
    print("3. Update Password")
    print("4. Generate Random Password")
    print("5. Exit")
    
    choice = input("\nSelect Option: ")

    if choice == '1':
        add_password()
    elif choice == '2':
        show_all()
    elif choice == '3':
        update_password()
    elif choice == '4':
        generate_pass()
    elif choice == '5':
        print("🔒 Vault Locked. Goodbye!")
        conn.close()
        break
    else:
        print("🚫 Invalid choice!")
