from connect import connect

def search_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(f"Name: {row[0]}, Phone: {row[1]}")
    cur.close()
    conn.close()

def upsert(name, phone):
    conn = connect()
    cur = conn.cursor()
    try:
        # Добавляем явное приведение типов прямо в запрос
        cur.execute("CALL upsert_contact(%s::text, %s::text)", (name, phone))
        conn.commit()
        print(f"Успешно: {name} обновлен/добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact_proc(%s)", (value,))
        conn.commit()
        print(f"Record with '{value}' deleted if it existed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def paginate(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    cur.close()
    conn.close()

def bulk_insert():
    names = input("Enter names separated by comma: ").split(',')
    phones = input("Enter phones separated by comma: ").split(',')
    
    
    names = [n.strip() for n in names]
    phones = [p.strip() for p in phones]

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
        conn.commit()
        print("Bulk insert finished.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


while True:
    print("\n--- PhoneBook Menu ---")
    print("1. Search (by pattern)")
    print("2. Upsert (add or update)")
    print("3. Delete (by name or phone)")
    print("4. Pagination")
    print("5. Bulk Insert")
    print("6. Exit")

    choice = input("Choose: ")

    if choice == '1':
        search_pattern(input("Enter pattern: "))
    elif choice == '2':
        upsert(input("Name: "), input("Phone: "))
    elif choice == '3':
        delete_contact(input("Name or phone: "))
    elif choice == '4':
        try:
            lim = int(input("Limit: "))
            offs = int(input("Offset: "))
            paginate(lim, offs)
        except ValueError:
            print("Please enter valid numbers.")
    elif choice == '5':
        bulk_insert()
    elif choice == '6':
        print("Goodbye!")
        break