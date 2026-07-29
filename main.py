import sqlite3

def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            UNIQUE(name, phone, email)
        )
    ''')
    
    conn.commit()
    conn.close()

def show_menu():
    print("Contact Book")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Edit Contact")
    print("4. Delete Contact")
    print("5. Exit")

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email address: ")

    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO contacts (Name, Phone, Email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        conn.commit()
        print(f"Contact for '{name}' added successfully")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        
def view_contacts():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, phone, email FROM contacts")
    rows = cursor.fetchall()

    if not rows:
        print("Your contact book is empty.")
        return []

    print("Your Contacts")
    for row in rows:
        db_id, name, phone, email = row
        print(f"ID: {db_id} | Name: {name} | Phone: {phone} | Email: {email}")

    return rows

def edit_contact():
    rows = view_contacts()
    if not rows:
        return
    try:
        contact_id = int(input("Enter the ID of the contact to edit: "))

        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, email FROM contacts WHERE id =?", (contact_id,))
        person = cursor.fetchone()

        if not person:
            print("Contact ID not found.")
            conn.close()
            return
        current_name, current_phone, current_email = person

        print(f"Editing Contact ID {contact_id}:")
        print("1. Edit Name")
        print("2. Edit Phone")
        print("3. Edit Email")
        print("4. Edit ALL")
        field_choice = input("Choose option (1-4): ")

        new_name, new_phone, new_email = current_name, current_phone, current_email

        if field_choice == "1":
            new_name = input(f"New name [{current_name}]: ") or current_name
        elif field_choice == "2":
            new_phone = input(f"New phone [{current_phone}]: ") or current_phone
        elif field_choice == "3":
            new_email = input(f"New email [{current_email}]: ") or current_email
        elif field_choice == "4":
            new_name = input(f"New name [{current_name}]: ") or current_name
            new_phone = input(f"New phone [{current_phone}]: ") or current_phone
            new_email = input(f"New email [{current_email}]: ") or current_email
        else:
            print("Invalid option.")
            conn.close()
            return

        try:
            cursor.execute('''
                UPDATE contacts 
                SET name = ?, phone = ?, email = ? 
                WHERE id = ?
            ''', (new_name, new_phone, new_email, contact_id))
            conn.commit()
            print("Contact updated successfully!")
        except sqlite3.IntegrityError:
            print("Edit cancelled! Those details match another existing contact.")
            
        conn.close()

    except ValueError:
        print("Please enter a valid number.")


def delete_contact():
    rows = view_contacts()
    if not rows:
        print("Your contact book is empty.")
        return
    try:
        contact_id = int(input("Enter the ID of the contact to delete: "))

        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        if contact_id > 0:
            conn.commit()
            print("Contact Deleted successfully.")
        else:
            print("ID not found.")
    except ValueError:
        print("Please Enter a valid ID.")

while True:
    show_menu()
    choice = input("Choose an option (1-5):")
    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        edit_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        break
    else:
        print("Invalid Choice")