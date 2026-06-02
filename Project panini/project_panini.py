import os
import sqlite3
import pandas as pd

folder_path= os.path.dirname(os.path.abspath(__file__))

db_path= os.path.join(folder_path, 'project_panini.db')

#database ready
conn= sqlite3.connect(db_path)
cursor= conn.cursor()

#create table
cursor.execute('''CREATE TABLE IF NOT EXISTS dhatu_master(id INTEGER PRIMARY KEY AUTOINCREMENT,
mool_dhatu Text not null,
adesh_dhatu TEXT NOT NULL,
english_name TEXT NOT NULL,
dhatu_type TEXT NOT NULL)''')

conn.commit()

#clear old data
cursor.execute("DELETE FROM dhatu_master")

#data entry
dhatus_list= [("पठ्", "पठ्", "path", "Vyanjan"),
("चल्", "चल्", "chal", "Vyanjan"),
("हस्", "हस्", "has", "Vyanjan"),
("गम्", "गच्छ्", "gam", "Adesh"),
("पा", "पिब्", "pa", "Adesh"),
("दृश्", "पश्य्", "drish", "Adesh")]

cursor.executemany('''
INSERT INTO dhatu_master (mool_dhatu, adesh_dhatu, english_name, dhatu_type) 
VALUES (?, ?, ?, ?)''', dhatus_list)

conn.commit()

#user input
print("\n--PROJECT PANINI--")

print("[AVILABLE DHATUS IN DATABASE]")

cursor.execute("SELECT mool_dhatu, english_name FROM dhatu_master")
saari_dhatus= cursor.fetchall()

for row in saari_dhatus:
    hindi_naam= row[0]
    english_naam= row[1]
    
    print(f"{hindi_naam} ({english_naam})")

user_input= input("enter dhatu: ")
clear_input= user_input.lower().strip()

cursor.execute('''SELECT adesh_dhatu, dhatu_type, mool_dhatu FROM dhatu_master WHERE mool_dhatu = ? OR english_name = ?''', (clear_input, clear_input))

result = cursor.fetchone()

if result is not None:
    adesh_dhatu = result[0]
    dhatu_type = result[1]
    asli_naam = result[2]
    print(f"\n[success]: {asli_naam}")
    print(f"base dhatu roop: {adesh_dhatu}| type: {dhatu_type}")
    
    if adesh_dhatu.endswith("्"):
        saaf_dhatu= adesh_dhatu[0:-1]
        pratham= [saaf_dhatu+"ति", saaf_dhatu+"तः", saaf_dhatu+"न्ति"]
        madhyam= [saaf_dhatu+"सि", saaf_dhatu+"थः", saaf_dhatu+"थ"]
        uttam= [saaf_dhatu+"ामि", saaf_dhatu+"ावः", saaf_dhatu+ "ामः"]
        
        matrix_data= {"Ekvachana": [pratham[0], madhyam[0], uttam[0]],
        "dwivachana":[pratham[1], madhyam[1], uttam[1]],
        "bahuvachana": [pratham[2], madhyam[2], uttam[2]]
        }
        
        row_labels= ["pratham purush", "madhyam purush", "uttam purush"]
        df= pd.DataFrame(matrix_data, index=row_labels)
        print(f"\n==============================================")
        print(f" लट् लकार (Present Tense) Table for: {asli_naam}")
        print(f"==============================================")
        print(df.to_string()) # .to_string() se grid ekdum saaf dikhegi
    
    else:
        saaf_dhatu= adesh_dhatu
else:
    print("wrong input")
    

	
	