import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "tracker.db")
db = sqlite3.connect(db_path)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
url TEXT,
target_price REAL,
current_price REAL) """)
db.commit()

# बेहतर हेडर्स - ताकि Amazon को लगे कि हम असली Chrome ब्राउज़र हैं
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
    "Referer": "https://www.google.com/"
}

def add_product():
    url = input("Enter Product Link: ")
    try:
        target = float(input("Enter Your Target Price: "))
        cursor.execute("INSERT INTO products(name, url, target_price, current_price) VALUES(?, ?, ?, ?)", ("Pending...", url, target, 0.0))
        db.commit()
        print("__Product Is Successfully Added__")
    except ValueError:
        print("__Invalid Price__")

def check_all_saved_products():
    cursor.execute("SELECT * FROM products")
    items = cursor.fetchall()
    
    if not items:
        print("\n__List Is Empty__")
        return
    print("\n__Checking Prices__ Please Wait...")
    for item in items:
        p_id, p_name, p_url, p_target, p_current = item
        try:
            res = requests.get(p_url, headers=HEADERS,)
            soup = BeautifulSoup(res.content, "html.parser")
            #for find name and price
            title_el = soup.find(id="productTitle")
            price_el = soup.find("span", {"class": "a-price-whole"})
            if title_el and price_el:
                title = title_el.get_text().strip()
                price_raw = price_el.get_text().replace(',','').replace('₹', '')
                current_price = float(price_raw)
                #Database update
                cursor.execute("UPDATE products SET name = ?, current_price = ? WHERE id = ?", (title[:50], current_price, p_id))
                db.commit()
                print(f"\n{title[:40]}...")
                print(f"\ncurrent: ₹{current_price} | target: {p_target}")
                if current_price <= p_target:
                    print("STATUS: __PRICE DROPED!__")
                else:
                    print("STATUS: __PRICE STILL ABOVE FROM TARGET__")
            else:
                 print(f"Could Not Find Datafor Prodent ID {p_id}, Check Link Lr Captcha.")
                 time.sleep(2)
        except Exception as e:
            print(f"System Error on Id {p_id}: {e}")

def show_tracking_list():
    query = "SELECT id, name, target_price, current_price FROM products"
    df = pd.read_sql_query(query, db)
    if df.empty:
        print("__List Is Empty__")
    else:
        print("\n__YOUR WHATCHLIST__")
        df.index = df.index + 1
        df.columns = ['DB_ID', 'Product_Name', 'Target (₹)', 'Last_price (₹)']
        print(df.to_string(index=True))

def delete_product():
    show = show_tracking_list()
    if show:
        try:
            prod_id = int(input("\nEnter the DB_ID to delete: "))
            cursor.execute("DELETE FROM products WHERE id = ?", (prod_id, ))
            db.commit()
            print(f"__Product ID {prod_id} deleted__")
        except:
            print("__INVALID ID__")

def function_manager():
    while True:
        print("\n")
        print("__Database Is Ready__")
        print("\n")
        print("__PRICE MONITOR__")
        print("1. Add New Product")
        print("2. Run Price Check")
        print("3. Show My Watchlist")
        print("4. Delete Product")
        print("5. Exit")
        
        choice = input("\nSelect Option From (1-5): ")
    
        if choice == '1':
            add_product()
        elif choice == '2':
            check_all_saved_products()
        elif choice == '3':
            show_tracking_list()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            print("__TRACKER CLOSED__")
            break
        else:
            print("__Invalid Option__")
    