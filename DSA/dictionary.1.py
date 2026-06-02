# TOPIC(1): Dictionary (Fast Data Lookup)
# Logic: Key-Value pair. Ye bina loop chalaye turant data dhund leta hai.

user_data = {
    "rahul123": {"name": "Rahul", "balance": 5000},
    "amit_45": {"name": "Amit", "balance": 1200}
}

# Kisi bhi user ka data turant nikalna
username = "rahul123"
if username in user_data:
    print(f"User Found: {user_data[username]['name']}")
