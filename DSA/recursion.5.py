# TOPIC: Recursion (Self-Calling Function)
# Logic: Deep nesting (folder ke andar folder) ko handle karne ke liye.

def scan_folders(folder_name):
    print(f"Scanning Folder: {folder_name}")
    
    # Maano isme do sub-folders hain
    sub_folders = ["Music", "Photos"]
    
    for sub in sub_folders:
        # Function khud ko dobara call karega andar jaane ke liye
        # scan_folders(sub) 
        # (Yahan sirf concept dikhane ke liye print hai)
        print(f"--- Found Subfolder: {sub}")

scan_folders("Root_Mobile_Storage")
