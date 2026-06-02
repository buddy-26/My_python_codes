import sqlite3
import os
import time

class TaskMaster:
    def __init__(self):
        # Yahan 'os' ka use karke path print karo
        # Aur check karo ki 'tasks.txt' hai ya nahi
        #text file code:
        '''print("file location:", os.getcwd())
        if not os.path.exists("tasks.txt"):
           with open("tasks.txt", "w") as f:
               f.write("__my tasks list__\n")
               print("file created")'''
        #sql db code:
        folder = "task_master"
        #self.folder_checker(folder)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, "tasks.db")
        self.conn = sqlite3.connect(full_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, time TEXT)")
        self.conn.commit()
        
    def folder_checker(self, folder_name):
        try:
            path = os.path.exists(folder_name)
            if not path:
                os.makedirs(folder_name)
                
            else:
                print(f"{folder_name} folder is avilable")
        except Exception as e:
            print(f"somthing is wrong try again {e}")
            
    def add_task(self):
        
        # User se input lo aur file mein 'append' karo
        #text file code
        task = input("enter task: ")
        time_now = time.strftime("%d-%m-%Y %H:%M:%S")
        '''with open("tasks.txt", 'a') as f:
            f.write(f"{time_now} - {task}\n")
            print("tasks saved")'''
        #sql db code:
        self.cursor.execute("INSERT INTO tasks(task,time) VALUES (?, ?)", (task, time_now))
        self.conn.commit()
        
    def show_tasks(self):
        print("my tasks")
        '''with open("tasks.txt", 'r') as f:
            content = f.read()
            print(content)'''
        self.cursor.execute("SELECT * FROM tasks")
        rows = self.cursor.fetchall()
        if not rows:
            print("task list is empty")
        for r in rows:
            print(f"id: {r[0]}, task: {r[1]}, time: {r[2]}")

    def delete_task(self):
        self.show_tasks()
        target_id = input("enter id: ")
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (target_id, ))
            
            if self.cursor.rowcount == 0:
                print("id is not in list")
            else:
                self.conn.commit()
                print(f"{target_id} succesfully deleted")
        except Exception as e:
            print(f"something is wrong try again {e}")
    
    

if __name__ == "__main__":
    # Yahan object banao aur function chalao
    app = TaskMaster()

    while True:
        print("1. add task")
        print("2. show task")
        print("3. delete task")
        print("4. exit")
        
        choice = input("enter your option: ")
        if choice == '1':
            app.add_task()
        elif choice == '2':
            app.show_tasks()
        elif choice == '3':
            app.delete_task()
        elif choice == '4':
            print("__closed__")
            break
        else:
            print("invalid option")