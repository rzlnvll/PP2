import csv
from connect import connect

# Create table
def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS phonebook")
    cur.execute("""
        CREATE TABLE phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            UNIQUE(name, surname)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created")

# Load functions and procedures
def load_sql():
    conn = connect()
    cur = conn.cursor()
    with open("functions.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())
    with open("procedures.sql", "r", encoding="utf-8") as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print("Functions and procedures loaded")

# Insert from CSV
def insert_from_csv():
    conn = connect()
    cur = conn.cursor()
    with open("contacts.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cur.execute("""
                INSERT INTO phonebook(name, surname, phone)
                VALUES (%s, %s, %s)
                ON CONFLICT (name, surname)
                DO UPDATE SET phone = EXCLUDED.phone
            """, (row["name"], row["surname"], row["phone"]))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV inserted")

# Insert from console
def insert_from_console():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phonebook(name, surname, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (name, surname)
        DO UPDATE SET phone = EXCLUDED.phone
    """, (name, surname, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("User saved")

# Update contact
def update_contact():
    choice = input("1-change first name, 2-change phone: ")
    conn = connect()
    cur = conn.cursor()
    if choice == "1":
        phone = input("Current phone: ")
        new_name = input("New first name: ")
        cur.execute("UPDATE phonebook SET name=%s WHERE phone=%s", (new_name, phone))
    elif choice == "2":
        name = input("Name: ")
        surname = input("Surname: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s AND surname=%s",
                    (new_phone, name, surname))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated")

# Query contacts
def query_contacts():
    choice = input("1-search by name, 2-search by phone prefix: ")
    conn = connect()
    cur = conn.cursor()
    if choice == "1":
        text = input("Enter name: ")
        cur.execute("""
            SELECT * FROM phonebook
            WHERE name ILIKE %s OR surname ILIKE %s
        """, (f"%{text}%", f"%{text}%"))
    elif choice == "2":
        prefix = input("Enter prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f"{prefix}%",))
    else:
        cur.close()
        conn.close()
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Delete contact
def delete_contact():
    choice = input("1-delete by name+surname, 2-delete by phone: ")
    conn = connect()
    cur = conn.cursor()
    if choice == "1":
        name = input("Name: ")
        surname = input("Surname: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s AND surname=%s", (name, surname))
    elif choice == "2":
        phone = input("Phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted")

# Search with function
def search_with_function():
    pattern = input("Pattern: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.search_contacts(%s::text)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Insert/update one user with procedure
def insert_or_update_with_procedure():
    name = input("Name: ")
    surname = input("Surname: ")
    phone = input("Phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_user(%s, %s, %s)", (name, surname, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Procedure finished")

# Insert many users with procedure
def insert_many_with_procedure():
    n = int(input("How many users: "))
    names = []
    surnames = []
    phones = []
    for i in range(n):
        print("User", i + 1)
        names.append(input("Name: ").strip())
        surnames.append(input("Surname: ").strip())
        phones.append(input("Phone: ").strip())
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CALL public.upsert_many_users(
            %s::text[],
            %s::text[],
            %s::text[],
            %s::text[]
        )
    """, (names, surnames, phones, []))
    bad = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print("Wrong data:")
    print(bad)

# Get page with function
def get_page():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.get_contacts_page(%s::int, %s::int)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Delete with procedure
def delete_with_procedure():
    choice = input("1-delete by name+surname, 2-delete by phone: ")
    conn = connect()
    cur = conn.cursor()
    if choice == "1":
        name = input("Name: ").strip()
        surname = input("Surname: ").strip()
        cur.execute(
            "CALL public.delete_contact_proc(%s::text, %s::text, %s::text)",
            (name, surname, None)
        )
    elif choice == "2":
        phone = input("Phone: ").strip()
        cur.execute(
            "CALL public.delete_contact_proc(%s::text, %s::text, %s::text)",
            (None, None, phone)
        )
    conn.commit()
    cur.close()
    conn.close()
    print("Procedure delete finished")

while True:
    print("\n1.Create table")
    print("2.Load functions and procedures")
    print("3.Insert from CSV")
    print("4.Insert from console")
    print("5.Update contact")
    print("6.Query contacts")
    print("7.Delete contact")
    print("8.Search with function")
    print("9.Insert/update one user with procedure")
    print("10.Insert many users with procedure")
    print("11.Get page with function")
    print("12.Delete with procedure")
    print("0.Exit")
    choice = input("Choose: ")
    if choice == "1":
        create_table()
    elif choice == "2":
        load_sql()
    elif choice == "3":
        insert_from_csv()
    elif choice == "4":
        insert_from_console()
    elif choice == "5":
        update_contact()
    elif choice == "6":
        query_contacts()
    elif choice == "7":
        delete_contact()
    elif choice == "8":
        search_with_function()
    elif choice == "9":
        insert_or_update_with_procedure()
    elif choice == "10":
        insert_many_with_procedure()
    elif choice == "11":
        get_page()
    elif choice == "12":
        delete_with_procedure()
    elif choice == "0":
        break