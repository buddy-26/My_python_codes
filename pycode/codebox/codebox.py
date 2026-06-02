import sqlite3
import importlib
import inspect
import hashlib
import os
import sys
import time

class CodeBox:
    # ---------------------------------------------------------
    # BLOCK 1: INITIALIZATION
    # Setup database connection and create required tables
    # ---------------------------------------------------------
    def __init__(self):
        self.db = sqlite3.connect("codebox_master.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registry (
                key TEXT PRIMARY KEY,
                file_name TEXT,
                func_name TEXT,
                display_name TEXT
            )
        """)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS secret (master_hash TEXT)")
        self.db.commit()

    # ---------------------------------------------------------
    # BLOCK 2: UTILITIES
    # Clear terminal screen for a clean user interface
    # ---------------------------------------------------------
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    # ---------------------------------------------------------
    # BLOCK 3: SECURITY MANAGEMENT
    # Handle master password creation and login verification
    # ---------------------------------------------------------
    def set_or_check_password(self):
        self.cursor.execute("SELECT master_hash FROM secret")
        row = self.cursor.fetchone()
        
        if not row:
            p = input("First Time Setup - Create Master Password: ")
            h = hashlib.sha256(p.encode()).hexdigest()
            self.cursor.execute("INSERT INTO secret VALUES (?)", (h,))
            self.db.commit()
            return True
        else:
            self.clear_screen()
            p = input("Enter Master Password: ")
            h = hashlib.sha256(p.encode()).hexdigest()
            if h == row[0]:
                return True
            else:
                print("Incorrect Password!")
                return False

    # ---------------------------------------------------------
    # BLOCK 4: ACCOUNT SETTINGS
    # Allow user to update the existing master password
    # ---------------------------------------------------------
    def change_master_password(self):
        old_p = input("Enter Current Password: ")
        old_h = hashlib.sha256(old_p.encode()).hexdigest()
        
        self.cursor.execute("SELECT master_hash FROM secret")
        current_hash = self.cursor.fetchone()[0]
        
        if old_h == current_hash:
            new_p = input("Enter New Password: ")
            confirm_p = input("Confirm New Password: ")
            if new_p == confirm_p:
                new_h = hashlib.sha256(new_p.encode()).hexdigest()
                self.cursor.execute("UPDATE secret SET master_hash = ?", (new_h,))
                self.db.commit()
                print("Password Updated Successfully!")
            else:
                print("Passwords do not match!")
        else:
            print("Verification Failed!")
        input("\nPress Enter to continue...")

    # ---------------------------------------------------------
    # BLOCK 5: FILE NAVIGATION
    # Browse folders and select Python files interactively
    # ---------------------------------------------------------
    def get_path_interactively(self):
        current_dir = os.getcwd()
        while True:
            self.clear_screen()
            print(f"Location: {current_dir}")
            try:
                items = os.listdir(current_dir)
            except PermissionError:
                print("Access Denied!")
                current_dir = os.path.dirname(current_dir)
                continue

            folders = [d for d in items if os.path.isdir(os.path.join(current_dir, d))]
            py_files = [f for f in items if f.endswith('.py')]

            print("0. [Select This Folder]")
            idx = 1
            for d in folders:
                print(f"{idx}. Folder: {d}/")
                idx += 1
            for f in py_files:
                print(f"{idx}. File: {f}")
                idx += 1
            
            choice = input("\n[b] Back | [q] Cancel | Number: ").lower()
            if choice == '0': return current_dir
            elif choice == 'b': current_dir = os.path.dirname(current_dir)
            elif choice == 'q': return None
            else:
                try:
                    all_items = folders + py_files
                    selected = all_items[int(choice)-1]
                    new_path = os.path.join(current_dir, selected)
                    if os.path.isdir(new_path): current_dir = new_path
                    else: return new_path
                except: print("Invalid Selection!")

    # ---------------------------------------------------------
    # BLOCK 6: TOOL REGISTRATION
    # Extract functions from a file and save them to the database
    # ---------------------------------------------------------
    def bulk_register_tools(self):
        full_path = self.get_path_interactively()
        if not full_path: return
        
        folder_path = os.path.dirname(full_path)
        file_name = os.path.basename(full_path).replace('.py', '')

        if folder_path not in sys.path:
            sys.path.append(folder_path)

        try:
            module = importlib.import_module(file_name)
            funcs = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
            
            if not funcs:
                print("No functions found!")
                return

            print(f"\nFunctions in {file_name}:")
            for i, f in enumerate(funcs, 1):
                print(f"{i}. {f}")

            choices = input("\nEnter numbers (e.g. 1,2) or 'all': ")
            selected_indices = list(range(len(funcs))) if choices.lower() == 'all' else [int(x.strip()) - 1 for x in choices.split(",")]

            for idx in selected_indices:
                f_name = funcs[idx]
                key = input(f"Short Key (Alias) for {f_name}: ").lower()
                d_name = input(f"Display Name for {f_name}: ")
                self.cursor.execute("INSERT OR REPLACE INTO registry VALUES (?, ?, ?, ?)", (key, file_name, f_name, d_name))
            
            self.db.commit()
            print("Registration Successful!")
        except Exception as e:
            print(f"Error: {e}")
        input("\nPress Enter...")

    # ---------------------------------------------------------
    # BLOCK 7: DATA VISUALIZATION
    # Show all registered tools grouped by their source file
    # ---------------------------------------------------------
    def show_all_tools(self):
        self.clear_screen()
        print("CODEBOX MASTER INVENTORY")
        self.cursor.execute("SELECT file_name, func_name, key, display_name FROM registry ORDER BY file_name")
        rows = self.cursor.fetchall()
        
        if not rows:
            print("\nNo tools registered.")
        else:
            current_file = ""
            for f_name, fn_name, key, d_name in rows:
                if f_name != current_file:
                    print(f"\nSource: {f_name}.py")
                    current_file = f_name
                print(f"  [{key}] -> {d_name} ({fn_name})")
        
        print("\n[reg] Register | [del] Delete | [chp] Password | [q] Exit")

    # ---------------------------------------------------------
    # BLOCK 8: MAIN CONTROL LOOP
    # Handle user input to navigate and execute tools
    # ---------------------------------------------------------
    def run(self):
        if not self.set_or_check_password(): return

        while True:
            self.show_all_tools()
            choice = input("\nAction: ").lower()

            if choice == 'q': break
            elif choice == 'reg': self.bulk_register_tools()
            elif choice == 'chp': self.change_master_password()
            elif choice == 'del':
                k = input("Key to delete: ")
                self.cursor.execute("DELETE FROM registry WHERE key=?", (k,))
                self.db.commit()
            else:
                self.cursor.execute("SELECT file_name, func_name FROM registry WHERE key=?", (choice,))
                res = self.cursor.fetchone()
                if res:
                    mod = importlib.import_module(res[0])
                    getattr(mod, res[1])()
                    input("\nExecution Finished. Press Enter...")
                else:
                    print("Invalid Key!")

if __name__ == "__main__":
    CodeBox().run()
