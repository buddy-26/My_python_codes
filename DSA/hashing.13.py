# TOPIC: Hashing (Unique Key Generation)
# Logic: Data ko ek unique index mein badal dena.

def simple_hash(string, table_size):
    # Har character ki value ko add karke index nikalna
    return sum(ord(char) for char in string) % table_size

print(f"Index for 'rahul': {simple_hash('rahul', 10)}")
print(f"Index for 'amit': {simple_hash('amit', 10)}")
