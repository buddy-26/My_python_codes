class Smart_diary:
    def __init__(self, filename):
        self.file = filename
    
    def add_notes(self, text):
        with open(self.file, "a") as file:
            file.write(text+"\n")
        print("your text added")
        
    def view_notes(self):
        try:
            with open(self.file, "r") as file:
                view = file.read().strip()
                if view:
                    print(view)
            
                else:
                    print("file is empty")
        except FileNotFoundError:
            print("file is not avilable")       
            
    def delete_text(self, delete):
        try:
            with open(self.file, "r")as file:
                contant= file.read()
                if delete in contant:
                    updated_contant = contant.replace(delete, "")
                    with open (self.file, "w")as file:
                        file.write(updated_contant)
                        print("text successfully deleted")
                else:
                    print(f"'{delete}' is not in file")
        except FileNotFoundError:
            print("file is not avilable")
    
print("log in/sign up")

user_name = input("enter your name: ")
user_file= user_name + "_diary.txt"
my_diary_obj = Smart_diary(user_file)
        

while True:
    print("select your options")
    print("1. Add Text")
    print("2. view notes")
    print("3. delete text")
    print("4. exit")
    user_input= input("choose your option: ")
    if user_input == "1":
        user_text= input("enter your text: ")
        my_diary_obj.add_notes(user_text)
    elif user_input == "2":
        my_diary_obj.view_notes()
    elif user_input== "3":
        deleting = input("enter text for delete: ")
        my_diary_obj.delete_text(deleting)
    elif user_input == "4":
        break
    else:
        print("wrong input")