guest_list = []

def check_list():
    name = input("enter name: ")
    if name in guest_list:
        print(f"welcome {name}")
    else:
        guest_list.append(name)
        print(f"registerd name, [{name}]")

while True:
    print("welcome to cafe")
    print("1. for check in")
    print("2. for check out")
    
    choice = input("enter your option: ")
    if choice == '1':
        check_list()
    if choice == '2':
        print("cafe closed")
        break