import random  # Computer ko random word chunne me madad karne ke liye is module ko bulaya
import nltk    # Python ki sabse badi language library (Natural Language Toolkit) ko bulaya

# --- ASLI DICTIONARY DOWNLOAD KARNA ---
# Jab aap code pehli baar chalayenge, toh yeh internet se duniya ke saare English words download karega (5-10 seconds lagenge)
try:
    nltk.data.find('corpora/words') # Check kar raha hai ki kya words pehle se downloaded hain
except LookupError:
    nltk.download('words') # Agar nahi hain, toh download karega

from nltk.corpus import words # Download hone ke baad words ka data import kiya

class WordAntyakshari:
    # 1. Constructor: Jo game shuru hote hi saari cheezein setup karta hai
    def __init__(self):
        # 🌍 DUNIYA KI ASLI DICTIONARY: Lakho English words ko ek 'set' me daal diya taaki checking fast ho
        self.english_words_set = set(w.lower() for w in words.words())
        
        # 🤖 COMPUTER KE WORDS: Game shuru karne ke liye computer ke paas kuch basic words ki list
        self.computer_stock = ["cat", "tree", "elephant", "tiger", "rabbit", "apple", "lemon", "nature", "egg", "goat"]
        
        self.used_words = []    # Jo words game me use ho jayenge, wo is list me aate jayenge
        self.last_letter = ""   # Yeh variable hamesha aakhri akshar (letter) ko yaad rakhega
        self.user_score = 0     # User ka shuruat ka score 0 set kiya
        self.comp_score = 0     # Computer ka shuruat ka score 0 set kiya

    # 🔍 FUNCTIONAL CHECK (Aapka Anti-Cheat Rule 💡): Yeh function check karega ki word asli hai ya nahi
    def is_meaningful_word(self, word):
        # Agar word lakho words ke samundar (english_words_set) me maujood hai, toh True return karega
        if word in self.english_words_set:
            return True
        # Agar word fake hai (jaise Uhdkf), toh False return karega
        else:
            return False

    # 2. Main Function: Jahan se game ka pura niyam aur loop chalega
    def start_game(self):
        print("🎮 --- WORD ANTYAKSHARI (REAL-WORLD DICTIONARY VERSION) --- 🎮")
        print("(Duniya ka koi bhi asli English word chalega! Quit karne ke liye 'quit' likhein)\n")
        
        # Computer pehla random word chunta hai apne stock me se
        comp_word = random.choice(self.computer_stock)
        self.used_words.append(comp_word)  # Used list me daal diya taaki dobara use na ho
        print(f"🤖 Computer ne pehla word bola: '{comp_word}'")
        
        # [-1] se word ka sabse aakhri letter (jaise cat me se 't') nikal kar save kiya
        self.last_letter = comp_word[-1]

        # Infinite While Loop: Jab tak koi jeetega nahi ya quit nahi karega, yeh chalta rahega
        while True:
            # Scoreboard dikhane ke liye current score print kiya
            print(f"\n📊 SCORE -> Aap: {self.user_score} | Computer: {self.comp_score}")
            print(f"👉 Aapki baari! '{self.last_letter}' se shuru hone wala word likho:")
            
            # User se input liya, extra spaces hataye (.strip) aur sab small letters me kiya (.lower)
            user_input = input("Aapka word: ").strip().lower()

            # Check 1: Agar user ne 'quit' likha toh loop todkar game band karo
            if user_input == "quit":
                print("\n👋 Game khatam! Khelne ke liye shukriya.")
                print(f"🏆 Final Score -> Aap: {self.user_score} | Computer: {self.comp_score}")
                break  # Break command se while loop wahin ruk jata hai

            # Check 2: Agar user ka word us akshar se shuru nahi ho raha jo last_letter me hai
            # user_input[0] ka matlab hai user ke word ka pehla akshar (jaise tree ka 't')
            if user_input[0] != self.last_letter:
                print(f"❌ Galat akshar! Aapko '{self.last_letter}' se shuru hone wala word likhna tha.")
                continue  # Continue se loop bina niche gaye seedhe fir se upar chala jata hai

            # 🚨 Check 3 (Aapka Rule): Kya yeh word sach me ek meaningful word hai? (Asli Dictionary check)
            if not self.is_meaningful_word(user_input):
                print(f"❌ Fake Word Alert! '{user_input}' koi real word nahi hai. Sirf meaningful words likho!")
                continue  # User ko naya mauka dene ke liye loop ko upar bhej diya

            # Check 4: Agar user ka word pehle se hi used_words ki list me maujood hai
            if user_input in self.used_words:
                print("❌ Yeh word pehle hi bola ja chuka hai! Kuch naya socho.")
                continue  # Dobara mauka dene ke liye loop ko upar bhej diya

            # --- AGAR SARE CHECK PASS HO GAYE (USER KA JAWAB SAHI HAI) ---
            print(f"✔️ Sahi jawab!")
            self.used_words.append(user_input)  # User ke word ko used list me block kar diya
            self.user_score += 10               # Sahi jawab par user ke score me 10 points jod diye
            self.last_letter = user_input[-1]   # Ab user ke word ka aakhri akshar naya target ban gaya

            # --- COMPUTER KI BAARI SHURU ---
            found_word = False  # Yeh dekhne ke liye variable banaya ki computer ko word mila ya nahi
            
            # Computer pehle apne stock me se word dhoondhega jo rules ke mutabik ho
            for word in self.computer_stock:
                if word.startswith(self.last_letter) and word not in self.used_words and self.is_meaningful_word(word):
                    print(f"🤖 Computer ne bola: '{word}'")
                    self.used_words.append(word)   # Computer ke word ko used list me dala
                    self.comp_score += 10          # Computer ko 10 points mil gaye
                    self.last_letter = word[-1]    # Computer ke word ka aakhri akshar ab user ke liye target hai
                    found_word = True              # Computer ko word mil gaya, isliye True kiya
                    break                          # Word milte hi for loop ko tod diya

            # 🧠 AGAR COMPUTER KE STOCK ME WORD NAHI MILA: Toh computer asli dictionary me se word dhoondhega!
            if not found_word:
                for word in self.english_words_set:
                    # Sirf wahi word uthayega jo sahi akshar se shuru ho, chota ho (taaki ajeeb na lage) aur used na ho
                    if word.startswith(self.last_letter) and len(word) < 8 and word not in self.used_words:
                        print(f"🤖 Computer ne bola: '{word}'")
                        self.used_words.append(word)
                        self.comp_score += 10
                        self.last_letter = word[-1]
                        found_word = True
                        break

            # Check 5: Agar poori duniya ki dictionary me bhi computer ko koi word nahi mila
            if not found_word:
                print("\n🥳 Computer ke paas koi valid word nahi bacha! AAP JEET GAYE!!! 🎉")
                print(f"🏆 Final Score -> Aap: {self.user_score} | Computer: {self.comp_score}")
                break  # Game ko yahin khatam kar diya kyunki computer haar gaya

# --- GAME KO CHALANE KA SYSTEM ---
game = WordAntyakshari()  # WordAntyakshari class ka ek object (game) banaya
game.start_game()         # Object ke andar wale start_game function ko call kiya game shuru karne ke liye
