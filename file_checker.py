import hashlib
import os
import json

HASH_RECORD_FILE = 'file_hashes.json'

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError) as e:
        print(f"[!] Cannot read {filepath}: {e}")
        return None

def load_previous_hashes():
    if not os.path.exists(HASH_RECORD_FILE):
        return {}
    with open(HASH_RECORD_FILE, 'r') as f:
        return json.load(f)

def save_hashes(hashes):
    with open(HASH_RECORD_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def monitor_files(file_list):
    old_hashes = load_previous_hashes()
    new_hashes = {}
    changes_detected = False

    for file in file_list:
        current_hash = calculate_file_hash(file)
        if current_hash is None:
            continue

        new_hashes[file] = current_hash
        old_hash = old_hashes.get(file)

        if old_hash is None:
            print(f"[+] New file added: {file}")
            changes_detected = True
        elif old_hash != current_hash:
            print(f"[!] File changed: {file}")
            changes_detected = True
        else:
            print(f"[=] No change: {file}")

    save_hashes(new_hashes)
    if not changes_detected:
        print("\nNo changes detected in monitored files.")

# Add test files to check
if __name__ == "__main__":
    files_to_check = [
        "example.txt",
        "data.csv","newfile.txt"
    ]
    monitor_files(files_to_check)
