import tkinter as tk

# 1. विंडो बनाना
root = tk.Tk()
root.title("Mera ATM")
root.geometry("300x200") # विंडो का साइज

# 2. एक फंक्शन जो बटन दबाने पर चलेगा
def bol_hi():
    print("Aapne Button Dabaya! 🎉")

# 3. बटन (Widget) बनाना
btn = tk.Button(root, text="Click Me!", command=bol_hi)
btn.pack(pady=20) # 'pack' का मतलब है उसे स्क्रीन पर चिपका दो

# 4. विंडो को चालू रखना
root.mainloop()
