import sqlite3
from cryptography.fernet import Fernet
import os

# Load or generate the encryption key
def load_key():
    if not os.path.exists("secret.key"):
        raise FileNotFoundError("secret.key not found. Please run generate_key.py first.")
    with open("secret.key", "rb") as key_file:
        return key_file.read()

key = load_key()
fernet = Fernet(key)

# Connect to database
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS manager (
        website TEXT,
        username TEXT,
        password TEXT
    )
''')

# Main menu
while True:
    print("\n1. Save new password")
    print("2. View saved passwords")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        website = input("Enter website: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        encrypted = fernet.encrypt(password.encode())
        cursor.execute("INSERT INTO manager VALUES (?, ?, ?)", (website, username, encrypted))
        conn.commit()
        print("✅ Password saved!")

    elif choice == "2":
        cursor.execute("SELECT * FROM manager")
        rows = cursor.fetchall()
        print("\n🔐 Saved Passwords:")
        for row in rows:
            try:
                decrypted = fernet.decrypt(row[2]).decode()
                print(f"Website: {row[0]}, Username: {row[1]}, Password: {decrypted}")
            except Exception as e:
                print(f"⚠️ Error decrypting password for {row[0]}: {e}")

    elif choice == "3":
        print("Exiting Password Manager. Goodbye!")
        break

    else:
        print("❌ Invalid choice. Try again.")

conn.close()
