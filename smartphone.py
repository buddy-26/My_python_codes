class smartphone():
    def __init__(self, model, battary_perc):
        self.phone= model
        self.battary= battary_perc
        
    def stream_video(self, minutes):
        loss = minutes * 2
        self.battary= self.battary - loss
        if self.battary <= 0:
            self.battary = 0
            return "DEAD"
        print(f"\nvideo streaming... power lose {self.battary}% in {minutes} mins.")
        return "ALIVE"
    
    def charge_phone(self, minutes):
        gain= minutes * 5
        self.battary = self.battary+ gain
        if self.battary > 100:
           self.battary = 100
        print(f"\npower charged {self.battary}% in {minutes} mins")
        return "CHARGED"

phone = "redmi"
battary = 100        

obj= smartphone(phone, battary)

while True:
    
    print("\n__phone's featuer's__")
    print("\n1. stream video")
    print("2. charging")
    print("3. switched off")
    
    user_input = input("\n__choose your options__: ")

    if user_input == "1":
        mins = int(input("enter streaming time period: "))
        status = obj.stream_video(mins)
        if status == "DEAD":
            print("\n__BATTARY DRAINED__")
            print("\n__SWITCHED OFF__")
            break
    elif user_input == "2":
        if obj.battary == 100:
            print("phone allrady charged")
            continue        
        mins= int(input("enter charging time period: "))
        obj.charge_phone(mins)
           
    elif user_input== "3":
        print("phone switched off")
        break
    else:
        print("wrong input enter the right one")






        