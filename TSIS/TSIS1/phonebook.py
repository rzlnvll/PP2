import csv
import json
import os
import sys
from connect import connect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def file_path(filename):
    return os.path.join(BASE_DIR, filename)


def run_sql_file(filename):
    path = file_path(filename)
    conn = connect()
    cur = conn.cursor()
    try:
        with open(path, "r", encoding="utf-8") as file:
            cur.execute(file.read())
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def print_table(rows):
    if not rows:
        print("No results")
        return
    for row in rows:
        print("-" * 90)
        print(" | ".join(str(value) if value is not None else "" for value in row))


def safe_date(value):
    value = (value or "").strip()
    return value if value else None


def safe_phone_type(value):
    value = (value or "mobile").strip().lower()
    if value not in ("home", "work", "mobile"):
        return "mobile"
    return value


def get_group_id(cur, group_name):
    group_name = (group_name or "Other").strip() or "Other"
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def save_contact(cur, name, surname, email, birthday, group_name, phone=None, phone_type="mobile", overwrite=True):
    group_id = get_group_id(cur, group_name)

    if overwrite:
        cur.execute("""
            INSERT INTO contacts(name, surname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name, surname)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id
        """, (name, surname, email or None, safe_date(birthday), group_id))
    else:
        cur.execute("""
            INSERT INTO contacts(name, surname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name, surname) DO NOTHING
            RETURNING id
        """, (name, surname, email or None, safe_date(birthday), group_id))

    result = cur.fetchone()
    if result is None:
        cur.execute("SELECT id FROM contacts WHERE name=%s AND surname=%s", (name, surname))
        result = cur.fetchone()

    contact_id = result[0]

    if phone:
        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone)
            DO UPDATE SET type = EXCLUDED.type
        """, (contact_id, phone, safe_phone_type(phone_type)))

    return contact_id


# ---------- setup ----------

def create_schema():
    run_sql_file("schema.sql")
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")
    print("Clean schema created. Functions and procedures loaded.")


def load_functions_and_procedures():
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")
    print("Functions and procedures loaded")


# ---------- import / export ----------

def insert_from_csv():
    conn = connect()
    cur = conn.cursor()
    try:
        with open(file_path("contacts.csv"), "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                save_contact(
                    cur,
                    row["name"].strip(),
                    row["surname"].strip(),
                    row.get("email", "").strip(),
                    row.get("birthday", "").strip(),
                    row.get("group", "Other").strip(),
                    row.get("phone", "").strip(),
                    row.get("phone_type", "mobile").strip()
                )
        conn.commit()
        print("CSV imported")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def export_to_json():
    filename = input("Output JSON file name [contacts.json]: ").strip() or "contacts.json"
    path = filename if os.path.isabs(filename) else file_path(filename)

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
    """)
    contacts = cur.fetchall()

    data = []
    for contact_id, name, surname, email, birthday, group_name in contacts:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s ORDER BY id", (contact_id,))
        phones = cur.fetchall()
        data.append({
            "name": name,
            "surname": surname,
            "email": email,
            "birthday": str(birthday) if birthday else None,
            "group": group_name,
            "phones": [
                {"phone": phone, "type": phone_type}
                for phone, phone_type in phones
            ]
        })

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()
    print("Exported to", path)


def import_from_json():
    filename = input("JSON file name [contacts.json]: ").strip() or "contacts.json"
    path = filename if os.path.isabs(filename) else file_path(filename)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = connect()
    cur = conn.cursor()
    try:
        for item in data:
            name = item["name"].strip()
            surname = item["surname"].strip()

            cur.execute("SELECT id FROM contacts WHERE name=%s AND surname=%s", (name, surname))
            duplicate = cur.fetchone()

            if duplicate:
                answer = input(f"{name} {surname} exists. skip / overwrite? ").strip().lower()
                if answer == "skip":
                    continue
                if answer != "overwrite":
                    print("Unknown answer. Skipped.")
                    continue
                cur.execute("DELETE FROM phones WHERE contact_id=%s", (duplicate[0],))

            contact_id = save_contact(
                cur,
                name,
                surname,
                item.get("email", ""),
                item.get("birthday"),
                item.get("group", "Other"),
                overwrite=True
            )

            for phone in item.get("phones", []):
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone)
                    DO UPDATE SET type = EXCLUDED.type
                """, (contact_id, phone.get("phone"), safe_phone_type(phone.get("type"))))

        conn.commit()
        print("JSON imported")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


# ---------- console operations ----------

def insert_from_console():
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD or empty: ").strip()
    group_name = input("Group [Other]: ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = input("Phone type home/work/mobile [mobile]: ").strip() or "mobile"

    conn = connect()
    cur = conn.cursor()
    try:
        save_contact(cur, name, surname, email, birthday, group_name, phone, phone_type)
        conn.commit()
        print("Contact saved")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.name, c.surname
    """, (f"%{group_name}%",))
    print_table(cur.fetchall())
    cur.close()
    conn.close()


def search_by_email():
    text = input("Email search text: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, surname, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name, surname
    """, (f"%{text}%",))
    print_table(cur.fetchall())
    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")
    choice = input("Choose: ").strip()

    order_options = {
        "1": "c.name, c.surname",
        "2": "c.birthday NULLS LAST, c.name",
        "3": "c.date_added, c.name"
    }
    order_by = order_options.get(choice)
    if not order_by:
        print("Wrong choice")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.surname, c.email, c.birthday, c.date_added, g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order_by}
    """)
    print_table(cur.fetchall())
    cur.close()
    conn.close()


def paginated_navigation():
    try:
        limit = int(input("Page size: ").strip())
    except ValueError:
        print("Page size must be a number")
        return

    offset = 0
    while True:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM public.get_contacts_page(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        print("\nPage offset:", offset)
        print_table(rows)

        command = input("next / prev / quit: ").strip().lower()
        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Unknown command")


def search_with_function():
    query = input("Search text: ").strip()
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.search_contacts(%s)", (query,))
    print_table(cur.fetchall())
    cur.close()
    conn.close()


def add_phone_proc():
    name = input("Contact first name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type home/work/mobile: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL public.add_phone(%s::varchar, %s::varchar, %s::varchar)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def move_to_group_proc():
    name = input("Contact first name: ").strip()
    group_name = input("New group: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL public.move_to_group(%s::varchar, %s::varchar)", (name, group_name))
        conn.commit()
        print("Contact moved")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def delete_contact():
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM contacts WHERE name=%s AND surname=%s", (name, surname))
        conn.commit()
        print("Contact deleted")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def show_menu():
    print("\nPHONEBOOK MENU")
    print("1. Create clean schema + load functions/procedures")
    print("2. Reload functions and procedures")
    print("3. Import from CSV")
    print("4. Add contact from console")
    print("5. Filter by group")
    print("6. Search by email")
    print("7. Sort contacts")
    print("8. Paginated navigation")
    print("9. Export to JSON")
    print("10. Import from JSON")
    print("11. Add phone using procedure")
    print("12. Move contact to group using procedure")
    print("13. Search using search_contacts function")
    print("14. Delete contact")
    print("0. Exit")


def main():
    actions = {
        "1": create_schema,
        "2": load_functions_and_procedures,
        "3": insert_from_csv,
        "4": insert_from_console,
        "5": filter_by_group,
        "6": search_by_email,
        "7": sort_contacts,
        "8": paginated_navigation,
        "9": export_to_json,
        "10": import_from_json,
        "11": add_phone_proc,
        "12": move_to_group_proc,
        "13": search_with_function,
        "14": delete_contact,
    }

    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "0":
            break

        action = actions.get(choice)
        if action is None:
            print("Wrong choice")
            continue

        try:
            action()
        except Exception as error:
            print("ERROR:", error)
            print("Tip: first run option 1, then option 3.")


if __name__ == "__main__":
    main()
