import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    with open('contacts.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()


def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update_contact(name, new_phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE first_name=%s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()

def search_by_name(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE first_name=%s",
        (name,)
    )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()
#

def delete_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE first_name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()


create_table()

while True:
    print("\n1 Insert")
    print("2 Import CSV")
    print("3 Show")
    print("4 Update")
    print("5 Search")
    print("6 Delete")
    print("7 Exit")

    choice = input("Choose: ")

    if choice == '1':
        name = input("Name: ")
        phone = input("Phone: ")
        insert_contact(name, phone)

    elif choice == '2':
        insert_from_csv()

    elif choice == '3':
        show_contacts()

    elif choice == '4':
        name = input("Name: ")
        new_phone = input("New phone: ")
        update_contact(name, new_phone)

    elif choice == '5':
        name = input("Name: ")
        search_by_name(name)

    elif choice == '6':
        name = input("Name: ")
        delete_contact(name)

    elif choice == '7':
        break