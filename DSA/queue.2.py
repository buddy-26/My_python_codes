# TOPIC: Queue (FIFO - First In First Out)
# Logic: Task scheduling ke liye sabse best.

task_queue = ["Send_Email_1", "Download_File_2", "Upload_Photo_3"]

# Naya task aane par line mein piche lagao
task_queue.append("Update_Database_4")

# Jo pehle tha use process karke bahar nikalo
while task_queue:
    current_task = task_queue.pop(0) # Index 0 matlab pehla wala
    print(f"Processing: {current_task}")
