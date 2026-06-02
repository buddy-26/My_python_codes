import sqlite3
import importlib
import inspect
import hashlib
import os
import sys
import time
import getpass

class CodeBox:
    def __init__(self):
        # Base directory jahan ye codebox.py rakha hai
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(self.base_dir, "codebox_master.db")
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
              
        # MISTAKE FIX: Table creation mein 'display_name' hi rakha hai
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registry (
                key TEXT PRIMARY KEY,
                file_name TEXT,
                func_name TEXT,
                display_name TEXT,
                full_path TEXT  -- Naya Column: Takki file kahin bhi ho, mil jaye
            )
        """)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS secret (master_hash TEXT)")
        self.db.commit()

        # Database migration: Agar purana DB hai toh naya column add karo bina delete kiye
        try:
            self.cursor.execute("ALTER TABLE registry ADD COLUMN full_path TEXT")
            self.db.commit()
        except: pass

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def set_or_check_password(self):
        self.cursor.execute("SELECT master_hash FROM secret")
        row = self.cursor.fetchone()
        if not row:
            p = input("🆕 First Time Setup - Create Master Password: ")
            h = hashlib.sha256(p.encode()).hexdigest()
            self.cursor.execute("INSERT INTO secret VALUES (?)", (h,))
            self.db.commit()
            return True
        else:
            self.clear_screen()
            p = getpass.getpass("🔐 Enter Master Password: ")
            h = hashlib.sha256(p.encode()).hexdigest()
            if h == row[0]: return True
            else:
                print("❌ Incorrect Password!"); return False

    def change_master_password(self):
        old_p = input("🔑 Enter Current Password: ")
        old_h = hashlib.sha256(old_p.encode()).hexdigest()
        self.cursor.execute("SELECT master_hash FROM secret")
        if old_h == self.cursor.fetchone()[0]:
            new_p = input("🆕 Enter New Password: ")
            confirm_p = input("🔄 Confirm New Password: ")
            if new_p == confirm_p:
                new_h = hashlib.sha256(new_p.encode()).hexdigest()
                self.cursor.execute("UPDATE secret SET master_hash = ?", (new_h,))
                self.db.commit()
                print("✅ Password Updated!")
            else: print("❌ Mismatch!")
        else: print("❌ Wrong Password!")
        input("\nPress Enter...")

    def get_path_interactively(self):
        current_dir = os.path.dirname(self.base_dir)
        root_limit = "/storage/emulated/0" 
        while True:
            self.clear_screen()
            print(f"📍 Location: {current_dir}")
            try:
                items = sorted(os.listdir(current_dir))
            except Exception:
                print("❌ Access Denied!"); current_dir = os.path.dirname(current_dir)
                time.sleep(1); continue

            folders = [d for d in items if os.path.isdir(os.path.join(current_dir, d))]
            py_files = [f for f in items if f.endswith('.py')]
            print("\n✅ [s] -> SELECT THIS FOLDER")
            print("-" * 35)
            all_items = folders + py_files
            for i, item in enumerate(all_items, 1):
                icon = "📁" if item in folders else "📄"
                print(f"{i}. {icon} {item}")
            
            choice = input("\n[s] Select | [b] Back | [q] Cancel | #: ").lower()
            if choice == 's': return current_dir
            elif choice == 'b':
                if current_dir.strip('/') == root_limit.strip('/'):
                    print("⚠️ Limit Reached!"); time.sleep(1)
                else: current_dir = os.path.dirname(current_dir)
            elif choice == 'q': return None
            else:
                try:
                    selected = all_items[int(choice)-1]
                    new_path = os.path.join(current_dir, selected)
                    if os.path.isdir(new_path): current_dir = new_path
                    else: return new_path
                except: print("⚠️ Invalid Choice!"); time.sleep(1)

    def bulk_register_tools(self):
        full_path = self.get_path_interactively()
        if not full_path: return
        
        # Path logic fixed
        if os.path.isfile(full_path):
            folder_path = os.path.dirname(full_path)
            file_name = os.path.basename(full_path).replace('.py', '')
        else:
            folder_path = full_path
            print("❌ Select a .py file, not just a folder!"); time.sleep(1); return

        if folder_path not in sys.path: sys.path.append(folder_path)

        try:
            module = importlib.import_module(file_name)
            funcs = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
            if not funcs: print("❌ No functions found!"); return

            print(f"\n📂 Functions in {file_name}:")
            for i, f in enumerate(funcs, 1): print(f"{i}. {f}")

            choices = input("\nEnter numbers or 'all': ").lower()
            is_all = choices == 'all'
            selected_indices = list(range(len(funcs))) if is_all else [int(x.strip()) - 1 for x in choices.split(",")]

            for idx in selected_indices:
                f_name = funcs[idx]
                if is_all:
                    key = "".join([p[0] for p in f_name.split("_")])[:4] if "_" in f_name else f_name[:2]
                    temp_key, count = key, 1
                    while True:
                        self.cursor.execute("SELECT 1 FROM registry WHERE key=?", (temp_key,))
                        if not self.cursor.fetchone(): key = temp_key; break
                        temp_key = f"{key}{count}"; count += 1
                    d_name = f_name.replace("_", " ").title()
                else:
                    key = input(f"🔑 Key for {f_name}: ").lower()
                    d_name = input(f"🏷️ Display Name: ")
                
                # AB HUM FULL_PATH BHI SAVE KAR RAHE HAIN
                self.cursor.execute("INSERT OR REPLACE INTO registry VALUES (?, ?, ?, ?, ?)", 
                                  (key, file_name, f_name, d_name, folder_path))
            
            self.db.commit()
            print("\n✅ Registered Successfully!")
        except Exception as e: print(f"❌ Error: {e}")
        input("\nPress Enter...")

    def search_tools(self):
        query = input("\n🔍 Search Tool: ").lower()
        # MISTAKE FIX: yahan 'display_name' use kiya hai SQL mein
        self.cursor.execute("""
            SELECT key, file_name, display_name, func_name FROM registry 
            WHERE key LIKE ? OR display_name LIKE ? OR func_name LIKE ?
            ORDER BY display_name ASC
        """, (f"{query}%", f"{query}%", f"{query}%"))
        results = self.cursor.fetchall()
        if not results: print(f"❌ No results for '{query}'")
        else:
            print(f"\n🔎 Results (A-Z):")
            print("-" * 45)
            for key, f_name, d_name, fn_name in results:
                print(f"[{key}] -> {d_name} (📄 {f_name}.py)")
            print("-" * 45)
        input("\nPress Enter...")

    def show_all_tools(self):
        self.clear_screen()
        print("⚡ CODEBOX MASTER MENU ⚡")
        self.cursor.execute("SELECT file_name, key, display_name FROM registry ORDER BY file_name")
        rows = self.cursor.fetchall()
        if not rows: print("\n⚠️ No tools registered.")
        else:
            curr = ""
            for f_name, key, d_name in rows:
                if f_name != curr:
                    print(f"\n📂 Source: {f_name}.py")
                    curr = f_name
                print(f"   [{key}] -> {d_name}")
        print("\n" + "="*20)
        print("\n[1] ➕ Register")
        print("[2] 🔍 Search")
        print("[3] 🗑️ Delete")
        print("[4] 🔑 Password")
        print("[5] 📂 Backup")
        print("[6] ❌ Quit\n" + "\n" + "="*20)
        

    def backup_data(self):
        import shutil
        # Backups folder ka rasta
        backup_folder = os.path.join(self.base_dir, "Backups")
        if not os.path.exists(backup_folder): 
            os.makedirs(backup_folder)
        
        # Samay ke hisaab se file ka naam (taaki purane backups delete na hon)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_file = os.path.join(backup_folder, f"backup_{timestamp}.db")
        
        try:
            # Main database ki copy banana
            shutil.copy2(os.path.join(self.base_dir, "codebox_master.db"), backup_file)
            print(f"\n✅ Backup Successful!")
            print(f"📂 Location: {backup_file}")
        except Exception as e:
            print(f"❌ Backup Failed: {e}")
        
        input("\nPress Enter to continue...")


    def run(self):
        if not self.set_or_check_password(): return
        while True:
            self.show_all_tools()
            choice = input("\n🚀 Enter Key or Action: ").lower()
            if choice == '6':
                break
            elif choice == '1':
                self.bulk_register_tools()
            elif choice == '2':
                self.search_tools()
            elif choice == '3':
                k = input("🗑️ Key to delete: "); self.cursor.execute("DELETE FROM registry WHERE key=?", (k,))
                self.db.commit()
            elif choice == '4':
                self.change_master_password()
            elif choice == '5':
                self.backup_data()
            else:
                # AB HUM DATABASE SE FILE KA POORA RASTA (FULL_PATH) BHI NIKAL RAHE HAIN
                self.cursor.execute("SELECT file_name, func_name, full_path FROM registry WHERE key=?", (choice,))
                res = self.cursor.fetchone()
                if res:
                    try:
                        f_name, fn_name, f_path = res
                        # AGAR PATH SAVE HAI TO USE SYSTEM MEIN ADD KARO
                        if f_path and f_path not in sys.path:
                            sys.path.append(f_path)
                        
                        mod = importlib.import_module(f_name)
                        importlib.reload(mod)
                        getattr(mod, fn_name)()
                        input("\n🏁 Finished. Press Enter...")
                    except Exception as e: print(f"❌ Error: {e}"); input()
                else: print("⚠️ Invalid Key!")

if __name__ == "__main__":
    CodeBox().run()
