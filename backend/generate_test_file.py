# generate_test_file.py

test_file_path = "test_note.txt"

test_content = """
YOUR FILES ARE ENCRYPTED
Send 1 BTC to the address below to decrypt your files.
"""

with open(test_file_path, "w") as f:
    f.write(test_content)

print(f"[INFO] Test file '{test_file_path}' created successfully.")
