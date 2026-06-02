import sqlite3
import importlib
import inspect
import hashlib
import os
import sys
import time
import termios
import tty

# --- 1. RANGON KI DUNIYA (ANSI COLORS) ---
C_GREEN = "\033[92m"
C_BLUE = "\033[94m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_END = "\033[0m"

# --- 2. PASSWORD MASKING (MAGIC STARS) ---
def get_masked_input(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ch in ('\r', '\n'): # Enter dabaya
            print()
            break
        elif ch == '\x7f': # Backspace handle
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            sys.stdout.write(ch) # Pehle letter dikhao
            sys.stdout.flush()
            time.sleep(0.15)     # Halki si deri
            sys.stdout.write('\b*') # Phir '*' bana do
            sys.stdout.flush()
            password += ch
    return password

class CodeBox:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(self.base_dir, "codebox_master.db")
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
              
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registry (
                key TEXT PRIMARY KEY,
                file_name TEXT,
                func_name TEXT,
                display_name TEXT,
                full_path TEXT
            )
        """)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS secret (master_hash TEXT)")
        self.db.commit()

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def set_or_check_password(self):
        self.cursor.execute("SELECT master_hash FROM secret")
        row = self.cursor.fetchone()
        if not row:
            p = get_masked_input(f"{C_YELLOW}🆕 Setup - Create Password: {C_END}")
            h = hashlib.sha256(p.encode()).hexdigest()
            self.cursor.execute("INSERT INTO secret VALUES (?)", (h,))
            self.db.commit()
            return True
        else:
            self.clear_screen()
            print(f"{C_BOLD}{C_BLUE}--- SECURITY CHECK ---{C_END}")
            p = get_masked_input(f"🔐 Enter Master Password: ")
            h = hashlib.sha256(p.encode()).hexdigest()
            if h == row[0]: return True
            else:
                print(f"{C_RED}❌ Access Denied!{C_END}")
                time.sleep(1)
                return False

    def get_path_interactively(self):
        current_dir = "/storage/emulated/0" # Android Storage
        while True:
            self.clear_screen()
            print(f"{C_BLUE}📍 Path: {current_dir}{C_END}")
            try:
                items = sorted(os.listdir(current_dir))
            except:
                print(f"{C_RED}❌ Access Denied!{C_END}")
                current_dir = os.path.dirname(current_dir); time.sleep(1); continue

            folders = [d for d in items if os.path.isdir(os.path.join(current_dir, d))]
            py_files = [f for f in items if f.endswith('.py')]
            
            print(f"\n{C_GREEN}[s] Select Folder | [b] Back | [q] Exit{C_END}")
            all_items = folders + py_files
            for i, item in enumerate(all_items, 1):
                icon = "📁" if item in folders else "📄"
                color = C_BLUE if item in folders else C_YELLOW
                print(f"{i}. {icon} {color}{item}{C_END}")
            
            choice = input(f"\n🚀 Choice: ").lower()
            if choice == 's': return current_dir
            elif choice == 'b': current_dir = os.path.dirname(current_dir)
            elif choice == 'q': return None
            else:
                try:
                    selected = all_items[int(choice)-1]
                    new_path = os.path.join(current_dir, selected)
                    if os.path.isdir(new_path): current_dir = new_path
                    else: return new_path
                except: print(f"{C_RED}⚠️ Invalid!{C_END}"); time.sleep(1)

    def bulk_register_tools(self):
        full_path = self.get_path_interactively()
        if not full_path or not os.path.isfile(full_path):
            print(f"{C_RED}❌ Select a .py file!{C_END}"); time.sleep(1); return
        
        folder_path = os.path.dirname(full_path)
        file_name = os.path.basename(full_path).replace('.py', '')
        if folder_path not in sys.path: sys.path.append(folder_path)

        try:
            module = importlib.import_module(file_name)
            funcs = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]
            for f_name in funcs:
                key = f_name[:3].lower() # Auto-key (3 chars)
                d_name = f_name.replace("_", " ").title()
                self.cursor.execute("INSERT OR REPLACE INTO registry VALUES (?, ?, ?, ?, ?)", 
                                  (key, file_name, f_name, d_name, folder_path))
            self.db.commit()
            print(f"{C_GREEN}✅ {len(funcs)} functions registered!{C_END}")
        except Exception as e: print(f"{C_RED}❌ Error: {e}{C_END}")
        time.sleep(2)

    def show_all_tools(self):
        self.clear_screen()
        print(f"{C_BOLD}{C_GREEN}⚡ CODEBOX V2 MENU ⚡{C_END}")
        self.cursor.execute("SELECT file_name, key, display_name FROM registry ORDER BY file_name")
        rows = self.cursor.fetchall()
        if not rows: print(f"\n{C_RED}⚠️ No tools registered.{C_END}")
        else:
            curr = ""
            for f_name, key, d_name in rows:
                if f_name != curr:
                    print(f"\n{C_BLUE}📂 Source: {f_name}.py{C_END}")
                    curr = f_name
                print(f"   [{C_YELLOW}{key}{C_END}] -> {d_name}")
        
        print(f"\n{C_BOLD}{'='*30}\n1. ➕ Reg  2. 🔍 Search  3. 🗑️ Del  6. ❌ Quit\n{'='*30}{C_END}")

    def run(self):
        if not self.set_or_check_password(): return
        while True:
            self.show_all_tools()
            choice = input(f"\n🚀 Enter Key: ").lower()
            if choice == '6': break
            elif choice == '1': self.bulk_register_tools()
            else:
                self.cursor.execute("SELECT file_name, func_name, full_path FROM registry WHERE key=?", (choice,))
                res = self.cursor.fetchone()
                if res:
                    f_name, fn_name, f_path = res
                    if f_path not in sys.path: sys.path.append(f_path)
                    try:
                        mod = importlib.import_module(f_name)
                        importlib.reload(mod)
                        getattr(mod, fn_name)()
                        input(f"\n{C_GREEN}🏁 Press Enter...{C_END}")
                    except Exception as e: print(f"{C_RED}❌ Run Error: {e}{C_END}"); input()
                else: print(f"{C_RED}⚠️ Invalid Key!{C_END}"); time.sleep(1)

if __name__ == "__main__":
    CodeBox().run()
