from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            pass

def get_last_visitor():
    if not os.path.exists(FILENAME):
        return None
    
    with open(FILENAME, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    last_line = lines[-1].strip()
    parts = last_line.split(' | ')
    
    if len(parts) == 2:
        name = parts[0]
        timestamp_str = parts[1]
        timestamp = datetime.fromisoformat(timestamp_str)
        return name, timestamp
    
    return None

def add_visitor(visitor_name):
    ensure_file()
    last_visitor_info = get_last_visitor()
    
    if last_visitor_info:
        last_name, last_timestamp = last_visitor_info
        
        if last_name == visitor_name:
            raise DuplicateVisitorError(f"Visitor '{visitor_name}' is already the last visitor!")
        
        time_elapsed = datetime.now() - last_timestamp
        if time_elapsed.total_seconds() < 300:
            raise EarlyEntryError(f"Must wait 5 minutes between different visitors. Only {time_elapsed.total_seconds():.0f} seconds have passed.")
    
    with open(FILENAME, 'a') as f:
        f.write(f"{visitor_name} | {datetime.now().isoformat()}\n")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
