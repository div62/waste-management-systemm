
from database import connect_db, create_tables
create_tables()
def fetch_one(sql, params=()):

    conn = connect_db()
    try:
        return conn.execute(sql, params).fetchone()
    finally:
        conn.close()
def fetch_all(sql, params=()):
    conn = connect_db()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def run_write(sql, params=()):
    conn = connect_db()
    try:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def generate_id(table_name, prefix):
    records = fetch_all("SELECT id FROM " + table_name)
    highest_number = 0
    for record in records:
        current_id = str(record[0])
        if current_id.startswith(prefix):
            number_part = current_id[len(prefix):]
            if number_part.isdigit() and int(number_part) > highest_number:
                highest_number = int(number_part)
    return prefix + str(highest_number + 1).zfill(3)


def ask_optional(label, current):
    text = input("Enter new " + label + " [" + str(current) + "]: ").strip()
    return text if text else current


def ask_number(label):
    while True:
        text = input(label).strip()
        try:
            value = float(text)
        except ValueError:
            print("Please enter a number, like 5 or 12.5.")
            continue
        if value <= 0:
            print("Please enter a number greater than 0.")
            continue
        return value


def ask_optional_number(label, current):
    while True:
        text = input("Enter new " + label + " [" + str(current) + "]: ").strip()
        if not text:
            return current
        try:
            value = float(text)
        except ValueError:
            print("Please enter a number, or press Enter to keep the current value.")
            continue
        if value <= 0:
            print("Please enter a number greater than 0.")
            continue
        return value
# user
def show_user(user):
    print("User ID:", user[0])
    print("Name:", user[1])
    print("Phone:", user[2])
    print("City:", user[3])

def add_user():
    print("\n ⬜ Add New User ")
    user_id = generate_id("users", "U")
    print("Generated User ID:", user_id)
    name = input("Enter user name: ")
    phone = input("Enter phone number: ")
    city = input("Enter city: ")
    run_write("INSERT INTO users (id, name, phone, city) VALUES (?, ?, ?, ?)",
              (user_id, name, phone, city))
    print("\nUser added successfully!")

def view_users():
    print("\n  ⬜ Registered Users ")
    users = fetch_all("SELECT * FROM users")
    if not users:
        print("No users registered yet.")
        return
    for user in users:
        print()
        show_user(user)

def search_user():
    print("\n ⬜ Search User ")
    user_id = input("Enter User ID to search: ")
    user = fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if user:
        print("\nUser Found!")
        show_user(user)
    else:
        print("User not found!")

def update_user():
    print("\n ⬜ Update User ")
    user_id = input("Enter User ID to update: ")
    user = fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user:
        print("User not found!")
        return
    print("Leave blank to keep the existing value.")
    name = ask_optional("name", user[1])
    phone = ask_optional("phone", user[2])
    city = ask_optional("city", user[3])
    run_write("UPDATE users SET name = ?, phone = ?, city = ? WHERE id = ?",
              (name, phone, city, user_id))
    print("\nUser updated successfully!")

def delete_user():
    print("\n ⬜ Delete User ")
    user_id = input("Enter User ID to delete: ")
    user = fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user:
        print("User not found!")
        return
    confirm = input("Delete user " + str(user[1]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM users WHERE id = ?", (user_id,))
        print("User deleted successfully!")
    else:
        print("Deletion cancelled.")
# waste

def show_waste(waste):
    print("Waste ID:", waste[0])
    print("Waste Name:", waste[1])
    print("Category:", waste[2])
    print("Description:", waste[3])


def add_waste():
    print("\n ⬜ Add Waste Type ")
    waste_id = generate_id("waste_types", "W")
    print("Generated Waste ID:", waste_id)
    name = input("Enter Waste Name: ")
    category = input("Enter Waste Category: ")
    description = input("Enter Waste Description: ")
    run_write("INSERT INTO waste_types (id, name, category, description) VALUES (?, ?, ?, ?)",
              (waste_id, name, category, description))
    print("\nWaste Type added successfully!")


def view_waste():
    print("\n ⬜ Registered Waste Types ")
    waste_types = fetch_all("SELECT * FROM waste_types")
    if not waste_types:
        print("No waste types registered yet.")
        return
    for waste in waste_types:
        print()
        show_waste(waste)


def search_waste():
    print("\n ⬜ Search Waste Type ")
    waste_id = input("Enter Waste ID to search: ")
    waste = fetch_one("SELECT * FROM waste_types WHERE id = ?", (waste_id,))
    if waste:
        print("\nWaste Type Found!")
        show_waste(waste)
    else:
        print("Waste Type not found!")


def update_waste():
    print("\n ⬜ Update Waste Type ")
    waste_id = input("Enter Waste ID to update: ")
    waste = fetch_one("SELECT * FROM waste_types WHERE id = ?", (waste_id,))
    if not waste:
        print("Waste Type not found!")
        return
    print("Leave blank to keep the existing value.")
    name = ask_optional("Waste Name", waste[1])
    category = ask_optional("Category", waste[2])
    description = ask_optional("Description", waste[3])
    run_write("UPDATE waste_types SET name = ?, category = ?, description = ? WHERE id = ?",
              (name, category, description, waste_id))
    print("\nWaste Type updated successfully!")


def delete_waste():
    print("\n ⬜ Delete Waste Type ")
    waste_id = input("Enter Waste ID to delete: ")
    waste = fetch_one("SELECT * FROM waste_types WHERE id = ?", (waste_id,))
    if not waste:
        print("Waste Type not found!")
        return
    confirm = input("Delete waste type " + str(waste[1]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM waste_types WHERE id = ?", (waste_id,))
        print("Waste Type deleted successfully!")
    else:
        print("Deletion cancelled.")
# city

def show_city(city):
    print("City ID:", city[0])
    print("City Name:", city[1])
    print("State:", city[2])

def add_city():
    print("\n ⬜ Add City ")
    city_id = generate_id("cities", "C")
    print("Generated City ID:", city_id)
    name = input("Enter City Name: ")
    state = input("Enter State Name: ")
    run_write("INSERT INTO cities (id, name, state) VALUES (?, ?, ?)", (city_id, name, state))
    print("\nCity added successfully!")

def view_cities():
    print("\n ⬜ Registered Cities ")
    cities = fetch_all("SELECT * FROM cities")
    if not cities:
        print("No cities registered yet.")
        return
    for city in cities:
        print()
        show_city(city)

def search_cities():
    print("\n ⬜ Search City ")
    city_id = input("Enter City ID to search: ")
    city = fetch_one("SELECT * FROM cities WHERE id = ?", (city_id,))
    if city:
        print("\nCity Found!")
        show_city(city)
    else:
        print("City not found!")

def update_city():
    print("\n ⬜ Update City ")
    city_id = input("Enter City ID to update: ")
    city = fetch_one("SELECT * FROM cities WHERE id = ?", (city_id,))
    if not city:
        print("City not found!")
        return
    print("Leave blank to keep the existing value.")
    name = ask_optional("City Name", city[1])
    state = ask_optional("State", city[2])
    run_write("UPDATE cities SET name = ?, state = ? WHERE id = ?", (name, state, city_id))
    print("City updated successfully!")

def delete_city():
    print("\n ⬜ Delete City ")
    city_id = input("Enter City ID to delete: ")
    city = fetch_one("SELECT * FROM cities WHERE id = ?", (city_id,))
    if not city:
        print("City not found!")
        return
    confirm = input("Delete city " + str(city[1]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM cities WHERE id = ?", (city_id,))
        print("City deleted successfully!")
    else:
        print("Deletion cancelled.")
#waste collection

def show_collection(collection):
    print("Collection ID:", collection[0])
    print("Waste Type:", collection[1])
    print("Quantity (kg):", collection[2])
    print("City ID:", collection[3])
    print("Area ID:", collection[4])
    print("Service Provider ID:", collection[5])
    print("Collection Date:", collection[6])
    print("Collection Status:", collection[7])

def add_collection():
    print("\n ⬜ Add Waste Collection ")
    collection_id = generate_id("waste_collections", "WC")
    print("Generated Collection ID:", collection_id)
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Quantity of Waste (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    provider_id = input("Enter Service Provider ID: ")
    collection_date = input("Enter Collection Date (DD/MM/YYYY): ")
    status = input("Enter Collection Status: ")
    run_write("""
        INSERT INTO waste_collections
        (id, waste_type, quantity, city_id, area_id, provider_id, collection_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (collection_id, waste_type, quantity, city_id, area_id,provider_id, collection_date, status))
    print("\nWaste Collection added successfully!")

def view_collections():
    print("\n ⬜ Registered Waste Collections ")
    collections = fetch_all("SELECT * FROM waste_collections")
    if not collections:
        print("No waste collections registered yet.")
        return
    for collection in collections:
        print()
        show_collection(collection)

def search_collection():
    print("\n ⬜ Search Waste Collection ")
    collection_id = input("Enter Collection ID to search: ")
    collection = fetch_one("SELECT * FROM waste_collections WHERE id = ?", (collection_id,))
    if collection:
        print("\nWaste Collection Found!")
        show_collection(collection)
    else:
        print("Waste Collection not found!")

def update_collection():
    print("\n ⬜ Update Waste Collection ")
    collection_id = input("Enter Collection ID to update: ")
    collection = fetch_one("SELECT * FROM waste_collections WHERE id = ?", (collection_id,))
    if not collection:
        print("Waste Collection not found!")
        return
    print("Leave blank to keep the existing value.")
    waste_type = ask_optional("Waste Type", collection[1])
    quantity = ask_optional("Quantity (kg)", collection[2])
    city_id = ask_optional("City ID", collection[3])
    area_id = ask_optional("Area ID", collection[4])
    provider_id = ask_optional("Provider ID", collection[5])
    collection_date = ask_optional("Collection Date", collection[6])
    status = ask_optional("Status", collection[7])
    run_write("""
        UPDATE waste_collections
        SET waste_type = ?, quantity = ?, city_id = ?, area_id = ?,
            provider_id = ?, collection_date = ?, status = ?
        WHERE id = ?""",
              (waste_type, quantity, city_id, area_id, provider_id,
               collection_date, status, collection_id))
    print("\nWaste Collection updated successfully!")

def delete_collection():
    print("\n ⬜ Delete Waste Collection ")
    collection_id = input("Enter Collection ID to delete: ")
    collection = fetch_one("SELECT * FROM waste_collections WHERE id = ?", (collection_id,))
    if not collection:
        print("Waste Collection not found!")
        return
    confirm = input("Delete collection " + str(collection[0]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM waste_collections WHERE id = ?", (collection_id,))
        print("Waste Collection deleted successfully!")
    else:
        print("Deletion cancelled.")
# Service providers 

def show_provider(provider):
    print("Provider ID:", provider[0])
    print("Provider Name:", provider[1])
    print("Service Type:", provider[2])
    print("City ID:", provider[3])

def add_provider():
    print("\n ⬜ Add Service Provider ")
    provider_id = generate_id("providers", "P")
    print("Generated Provider ID:", provider_id)
    name = input("Enter Provider Name: ")
    service_type = input("Enter Service Type: ")
    city_id = input("Enter City ID: ")
    run_write("INSERT INTO providers (id, name, service_type, city_id) VALUES (?, ?, ?, ?)",
              (provider_id, name, service_type, city_id))
    print("\nService Provider added successfully!")

def view_providers():
    print("\n ⬜ Registered Service Providers ")
    providers = fetch_all("SELECT * FROM providers")
    if not providers:
        print("No service providers registered yet.")
        return
    for provider in providers:
        print()
        show_provider(provider)

def search_provider():
    print("\n ⬜ Search Service Provider ")
    provider_id = input("Enter Provider ID to search: ")
    provider = fetch_one("SELECT * FROM providers WHERE id = ?", (provider_id,))
    if provider:
        print("\nService Provider Found!")
        show_provider(provider)
    else:
        print("Service Provider not found!")

def update_provider():
    print("\n ⬜ Update Service Provider ")
    provider_id = input("Enter Provider ID to update: ")
    provider = fetch_one("SELECT * FROM providers WHERE id = ?", (provider_id,))
    if not provider:
        print("Service Provider not found!")
        return
    print("Leave blank to keep the existing value.")
    name = ask_optional("Provider Name", provider[1])
    service_type = ask_optional("Service Type", provider[2])
    city_id = ask_optional("City ID", provider[3])
    run_write("UPDATE providers SET name = ?, service_type = ?, city_id = ? WHERE id = ?",
              (name, service_type, city_id, provider_id))
    print("Service Provider updated successfully!")

def delete_provider():
    print("\n ⬜ Delete Service Provider ")
    provider_id = input("Enter Provider ID to delete: ")
    provider = fetch_one("SELECT * FROM providers WHERE id = ?", (provider_id,))
    if not provider:
        print("Service Provider not found!")
        return
    confirm = input("Delete provider " + str(provider[1]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM providers WHERE id = ?", (provider_id,))
        print("Service Provider deleted successfully!")
    else:
        print("Deletion cancelled.")
#  Schedules 

def show_schedule(schedule):
    print("Schedule ID:", schedule[0])
    print("Collection ID:", schedule[1])
    print("Schedule Date:", schedule[2])
    print("Schedule Time:", schedule[3])
    print("Provider ID:", schedule[4])
    print("Schedule Status:", schedule[5])

def add_schedule():
    print("\n ⬜ Add Collection Schedule ")
    schedule_id = generate_id("schedules", "S")
    print("Generated Schedule ID:", schedule_id)
    collection_id = input("Enter Collection ID: ")
    date = input("Enter Schedule Date (DD/MM/YYYY): ")
    time = input("Enter Schedule Time: ")
    provider_id = input("Enter Provider ID: ")
    status = input("Enter Schedule Status: ")
    run_write("""
        INSERT INTO schedules (id, collection_id, date, time, provider_id, status)
        VALUES (?, ?, ?, ?, ?, ?)""",
              (schedule_id, collection_id, date, time, provider_id, status))
    print("\nCollection Schedule added successfully!")

def view_schedules():
    print("\n ⬜ Registered Collection Schedules ")
    schedules = fetch_all("SELECT * FROM schedules")
    if not schedules:
        print("No schedules registered yet.")
        return
    for schedule in schedules:
        print()
        show_schedule(schedule)

def search_schedule():
    print("\n ⬜ Search Collection Schedule ")
    schedule_id = input("Enter Schedule ID to search: ")
    schedule = fetch_one("SELECT * FROM schedules WHERE id = ?", (schedule_id,))
    if schedule:
        print("\nCollection Schedule Found!")
        show_schedule(schedule)
    else:
        print("Schedule not found!")

def update_schedule():
    print("\n ⬜ Update Collection Schedule ")
    schedule_id = input("Enter Schedule ID to update: ")
    schedule = fetch_one("SELECT * FROM schedules WHERE id = ?", (schedule_id,))
    if not schedule:
        print("Schedule not found!")
        return
    collection_id = ask_optional("Collection ID", schedule[1])
    date = ask_optional("Schedule Date", schedule[2])
    time = ask_optional("Schedule Time", schedule[3])
    provider_id = ask_optional("Provider ID", schedule[4])
    status = ask_optional("Schedule Status", schedule[5])
    run_write("""
        UPDATE schedules
        SET collection_id = ?, date = ?, time = ?, provider_id = ?, status = ?
        WHERE id = ?""",
              (collection_id, date, time, provider_id, status, schedule_id))
    print("\nCollection Schedule updated successfully!")

def delete_schedule():
    print("\n ⬜ Delete Collection Schedule ")
    schedule_id = input("Enter Schedule ID to delete: ")
    schedule = fetch_one("SELECT * FROM schedules WHERE id = ?", (schedule_id,))
    if not schedule:
        print("Schedule not found!")
        return
    confirm = input("Delete schedule " + str(schedule[0]) + "? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM schedules WHERE id = ?", (schedule_id,))
        print("Collection Schedule deleted successfully!")
    else:
        print("Deletion cancelled.")
#  Requests 

def show_request(request):
    print("Request ID:", request[0])
    print("User ID:", request[1])
    print("Waste Type:", request[2])
    print("Quantity (kg):", request[3])
    print("City ID:", request[4])
    print("Area ID:", request[5])
    print("Preferred Date:", request[6])
    print("Request Status:", request[7])

def add_request():
    print("\n ⬜ Add Waste Collection Request ")
    request_id = generate_id("requests", "R")
    print("Generated Request ID:", request_id)
    user_id = input("Enter User ID: ")
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Quantity of Waste (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    preferred_date = input("Enter Preferred Date (DD/MM/YYYY): ")
    status = input("Enter Request Status: ")
    run_write("""
        INSERT INTO requests
        (id, user_id, waste_type, quantity, city_id, area_id, preferred_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (request_id, user_id, waste_type, quantity, city_id, area_id,
               preferred_date, status))
    print("\nWaste Collection Request added successfully!")

def view_requests():
    print("\n ⬜ Registered Waste Collection Requests ")
    requests = fetch_all("SELECT * FROM requests")
    if not requests:
        print("No requests registered yet.")
        return
    for request in requests:
        print()
        show_request(request)

def search_request():
    print("\n ⬜ Search Waste Collection Request ")
    request_id = input("Enter Request ID to search: ")
    request = fetch_one("SELECT * FROM requests WHERE id = ?", (request_id,))
    if request:
        print("\nWaste Collection Request Found!")
        show_request(request)
    else:
        print("Request not found!")

def update_request():
    print("\n ⬜ Update Waste Collection Request ")
    request_id = input("Enter Request ID to update: ")
    request = fetch_one("SELECT * FROM requests WHERE id = ?", (request_id,))
    if not request:
        print("Request not found!")
        return
    user_id = ask_optional("User ID", request[1])
    waste_type = ask_optional("Waste Type", request[2])
    quantity = ask_optional("Quantity (kg)", request[3])
    city_id = ask_optional("City ID", request[4])
    area_id = ask_optional("Area ID", request[5])
    preferred_date = ask_optional("Preferred Date", request[6])
    status = ask_optional("Request Status", request[7])
    run_write("""
        UPDATE requests
        SET user_id = ?, waste_type = ?, quantity = ?, city_id = ?,
            area_id = ?, preferred_date = ?, status = ?
        WHERE id = ?""",
              (user_id, waste_type, quantity, city_id, area_id,
               preferred_date, status, request_id))
    print("\nWaste Collection Request updated successfully!")

def delete_request():
    print("\n ⬜ Delete Waste Collection Request ")
    request_id = input("Enter Request ID to delete: ")
    request = fetch_one("SELECT * FROM requests WHERE id = ?", (request_id,))
    if not request:
        print("Request not found!")
        return
    print("\nRequest Found!")
    show_request(request)
    confirm = input("Delete this request? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM requests WHERE id = ?", (request_id,))
        print("Request deleted successfully!")
    else:
        print("Request deletion cancelled!")
#  Bills

def show_bill(bill):
    print("Bill ID:", bill[0])
    print("User ID:", bill[1])
    print("Collection ID:", bill[2])
    print("Quantity (kg):", bill[3])
    print("Rate per kg: ₹", bill[4])
    print("Total Amount: ₹", bill[5])
    print("Payment Status:", bill[6])

def generate_bill():
    print("\n ⬜ Generate Bill ")
    bill_id = generate_id("bills", "B")
    print("Generated Bill ID:", bill_id)
    user_id = input("Enter User ID: ")
    collection_id = input("Enter Collection ID: ")
    quantity = ask_number("Enter Quantity of Waste (kg): ")
    rate = ask_number("Enter Rate per kg: ")
    total_amount = quantity * rate
    payment_status = input("Enter Payment Status: ")
    run_write("""
        INSERT INTO bills
        (id, user_id, collection_id, quantity, rate, total_amount, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (bill_id, user_id, collection_id, quantity, rate, total_amount, payment_status))
    print("\nBill generated successfully!")
    print("Total Amount: ₹", total_amount)

def view_bills():
    print("\n ⬜ Registered Bills ")
    bills = fetch_all("SELECT * FROM bills")
    if not bills:
        print("No bills generated yet.")
        return
    for bill in bills:
        print()
        show_bill(bill)

def search_bill():
    print("\n ⬜ Search Bill ")
    bill_id = input("Enter Bill ID to search: ")
    bill = fetch_one("SELECT * FROM bills WHERE id = ?", (bill_id,))
    if bill:
        print("\nBill Found!")
        show_bill(bill)
    else:
        print("Bill not found!")

def update_bill():
    print("\n ⬜ Update Bill ")
    bill_id = input("Enter Bill ID to update: ")
    bill = fetch_one("SELECT * FROM bills WHERE id = ?", (bill_id,))
    if not bill:
        print("Bill not found!")
        return
    user_id = ask_optional("User ID", bill[1])
    collection_id = ask_optional("Collection ID", bill[2])
    quantity = ask_optional_number("Quantity (kg)", bill[3])
    rate = ask_optional_number("Rate per kg", bill[4])
    payment_status = ask_optional("Payment Status", bill[6])
    total_amount = quantity * rate
    run_write("""
        UPDATE bills
        SET user_id = ?, collection_id = ?, quantity = ?, rate = ?,
            total_amount = ?, payment_status = ?
        WHERE id = ?""",
              (user_id, collection_id, quantity, rate, total_amount, payment_status, bill_id))
    print("\nBill updated successfully!")
    print("Updated Total Amount: ₹", total_amount)

def delete_bill():
    print("\n ⬜ Delete Bill ")
    bill_id = input("Enter Bill ID to delete: ")
    bill = fetch_one("SELECT * FROM bills WHERE id = ?", (bill_id,))
    if not bill:
        print("Bill not found!")
        return
    print("\nBill Found!")
    show_bill(bill)
    confirm = input("Delete this bill? (yes/no): ")
    if confirm.lower() == "yes":
        run_write("DELETE FROM bills WHERE id = ?", (bill_id,))
        print("Bill deleted successfully!")
    else:
        print("Bill deletion cancelled!")