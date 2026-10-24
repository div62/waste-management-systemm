from database import connect_db, create_tables
create_tables()

users = []
def add_user():
    print("\n ⬜ Add New User ")
    user_id = input("Enter User ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone():
        print("Error: User ID already exists!")
        conn.close()
        return
    name = input("Enter user name: ")
    phone = input("Enter phone number: ")
    city = input("Enter city: ")
    cursor.execute("""
        INSERT INTO users (id, name, phone, city)
        VALUES (?, ?, ?, ?)
    """, (user_id, name, phone, city))
    conn.commit()
    conn.close()
    print("\nUser added successfully!")
def view_users():
    print("\n  ⬜ Registered Users ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    if not users:
        print("No users registered yet.")
        return
    for user in users:
        print("\nUser ID:", user[0])
        print("Name:", user[1])
        print("Phone:", user[2])
        print("City:", user[3])
def search_user():
    print("\n ⬜ Search User ")
    user_id = input("Enter User ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("\nUser Found!")
        print("User ID:", user[0])
        print("Name:", user[1])
        print("Phone:", user[2])
        print("City:", user[3])
    else:
        print("User not found!")
def update_user():
    print("\n ⬜ Update User ")
    user_id = input("Enter User ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        print("Leave blank to keep the existing value.")
        name = input(f"Enter new name [{user[1]}]: ")
        phone = input(f"Enter new phone [{user[2]}]: ")
        city = input(f"Enter new city [{user[3]}]: ")
        if name:
            user_name = name
        else:
            user_name = user[1]
        if phone:
            user_phone = phone
        else:
            user_phone = user[2]
        if city:
            user_city = city
        else:
            user_city = user[3]
        cursor.execute("""
            UPDATE users
            SET name = ?, phone = ?, city = ?
            WHERE id = ?
        """, (user_name, user_phone, user_city, user_id))
        conn.commit()
        print("\nUser updated successfully!")
    else:
        print("User not found!")
    conn.close()
def delete_user():
    print("\n ⬜ Delete User ")
    user_id = input("Enter User ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        confirm = input(f"Delete user {user[1]}? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            print("User deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("User not found!")

    conn.close()
waste_types = []
def add_waste():
    print("\n ⬜ Add Waste Type ")
    waste_id = input("Enter Waste ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM waste_types WHERE id = ?", (waste_id,))
    if cursor.fetchone():
        print("Error: Waste ID already exists!")
        conn.close()
        return
    name = input("Enter Waste Name: ")
    category = input("Enter Waste Category: ")
    description = input("Enter Waste Description: ")
    cursor.execute("""
        INSERT INTO waste_types (id, name, category, description)
        VALUES (?, ?, ?, ?)
    """, (waste_id, name, category, description))
    conn.commit()
    conn.close()
    print("\nWaste Type added successfully!")
def view_waste():
    print("\n ⬜ Registered Waste Types ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM waste_types")
    waste_types = cursor.fetchall()
    conn.close()
    if not waste_types:
        print("No waste types registered yet.")
        return
    for waste in waste_types:
        print("Waste ID:", waste[0])
        print("Waste Name:", waste[1])
        print("Category:", waste[2])
        print("Description:", waste[3])
def search_waste():
    print("\n ⬜ Search Waste Type ")
    waste_id = input("Enter Waste ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_types WHERE id = ?",
        (waste_id,)
    )
    waste = cursor.fetchone()
    conn.close()
    if waste:
        print("\nWaste Type Found!")
        print("Waste ID:", waste[0])
        print("Waste Name:", waste[1])
        print("Category:", waste[2])
        print("Description:", waste[3])
    else:
        print("Waste Type not found!") 
def update_waste():
    print("\n ⬜ Update Waste Type ")
    waste_id = input("Enter Waste ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_types WHERE id = ?",
        (waste_id,)
    )
    waste = cursor.fetchone()
    if waste:
        name = input(f"Enter new Waste Name [{waste[1]}]: ")
        category = input(f"Enter new Category [{waste[2]}]: ")
        description = input(f"Enter new Description [{waste[3]}]: ")
        if name:
            waste_name = name
        else:
            waste_name = waste[1]
        if category:
            waste_category = category
        else:
            waste_category = waste[2]
        if description:
            waste_description = description
        else:
            waste_description = waste[3]
        cursor.execute("""
            UPDATE waste_types
            SET name = ?, category = ?, description = ?
            WHERE id = ?
        """, (waste_name, waste_category, waste_description, waste_id))
        conn.commit()
        print("\nWaste Type updated successfully!")
    else:
        print("Waste Type not found!")
    conn.close()   
def delete_waste():
    print("\n ⬜ Delete Waste Type ")
    waste_id = input("Enter Waste ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_types WHERE id = ?",
        (waste_id,)
    )
    waste = cursor.fetchone()
    if waste:
        confirm = input(f"Delete waste type {waste[1]}? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM waste_types WHERE id = ?",
                (waste_id,)
            )
            conn.commit()
            print("Waste Type deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("Waste Type not found!")
    conn.close()
cities = []
def add_city():
    print("\n ⬜ Add City ")
    city_id = input("Enter City ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cities WHERE id = ?", (city_id,))
    if cursor.fetchone():
        print("Error: City ID already exists!")
        conn.close()
        return
    name = input("Enter City Name: ")
    state = input("Enter State Name: ")
    cursor.execute("""
        INSERT INTO cities (id, name, state)
        VALUES (?, ?, ?)
    """, (city_id, name, state))
    conn.commit()
    conn.close()
    print("\nCity added successfully!")
def view_cities():
    print("\n ⬜ Registered Cities ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()
    conn.close()
    if not cities:
        print("No cities registered yet.")
        return
    for city in cities:
        print("City ID:", city[0])
        print("City Name:", city[1])
        print("State:", city[2])
def search_cities():
    print("\n ⬜ Search City ")
    city_id = input("Enter City ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities WHERE id = ?", (city_id,))
    city = cursor.fetchone()
    conn.close()
    if city:
        print("\nCity Found!")
        print("City ID:", city[0])
        print("City Name:", city[1])
        print("State:", city[2])
    else:
        print("City not found!")
def search_cities():
    print("\n ⬜ Search City ")
    city_id = input("Enter City ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities WHERE id = ?", (city_id,))
    city = cursor.fetchone()
    conn.close()
    if city:
        print("\nCity Found!")
        print("City ID:", city[0])
        print("City Name:", city[1])
        print("State:", city[2])
    else:
        print("City not found!")
def update_city():
    print("\n ⬜ Update City ")
    city_id = input("Enter City ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cities WHERE id = ?",
        (city_id,)
    )
    city = cursor.fetchone()
    if city:
        print("Leave blank to keep the existing value.")
        name = input(f"Enter new City Name [{city[1]}]: ")
        state = input(f"Enter new State [{city[2]}]: ")
        if name:
            new_name = name
        else:
            new_name = city[1]
        if state:
            new_state = state
        else:
            new_state = city[2]
        cursor.execute("""
            UPDATE cities
            SET name = ?, state = ?
            WHERE id = ?
        """, (new_name, new_state, city_id))
        conn.commit()
        print("City updated successfully!")
    else:
        print("City not found!")
    conn.close()
def delete_city():
    print("\n ⬜ Delete City ")
    city_id = input("Enter City ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cities WHERE id = ?", (city_id,))
    city = cursor.fetchone()
    if city:
        confirm = input(f"Delete city {city[1]}? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM cities WHERE id = ?",
                (city_id,)
            )
            conn.commit()
            print("City deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("City not found!")
    conn.close()
collections=[]
def add_collection():
    print("\n ⬜ Add Waste Collection ")
    collection_id = input("Enter Collection ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM waste_collections WHERE id = ?",
        (collection_id,)
    )
    if cursor.fetchone():
        print("Error: Collection ID already exists!")
        conn.close()
        return
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Quantity of Waste (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    provider_id = input("Enter Service Provider ID: ")
    collection_date = input("Enter Collection Date (DD/MM/YYYY): ")
    status = input("Enter Collection Status: ")
    cursor.execute("""
        INSERT INTO waste_collections
        (id, waste_type, quantity, city_id, area_id,
         provider_id, collection_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        collection_id, waste_type, quantity, city_id,
        area_id, provider_id, collection_date, status
    ))
    conn.commit()
    conn.close()
    print("\nWaste Collection added successfully!")
def view_collections():
    print("\n ⬜ Registered Waste Collections ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM waste_collections")
    collections = cursor.fetchall()
    conn.close()
    if not collections:
        print("No waste collections registered yet.")
        return
    for collection in collections:
        print("Collection ID:", collection[0])
        print("Waste Type:", collection[1])
        print("Quantity (kg):", collection[2])
        print("City ID:", collection[3])
        print("Area ID:", collection[4])
        print("Service Provider ID:", collection[5])
        print("Collection Date:", collection[6])
        print("Collection Status:", collection[7])         
def search_collection():
    print("\n ⬜ Search Waste Collection ")
    collection_id = input("Enter Collection ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_collections WHERE id = ?",
        (collection_id,)
    )
    collection = cursor.fetchone()
    conn.close()
    if collection:
        print("\nWaste Collection Found!")
        print("Collection ID:", collection[0])
        print("Waste Type:", collection[1])
        print("Quantity (kg):", collection[2])
        print("City ID:", collection[3])
        print("Area ID:", collection[4])
        print("Service Provider ID:", collection[5])
        print("Collection Date:", collection[6])
        print("Collection Status:", collection[7])
    else:
        print("Waste Collection not found!")
def update_collection():
    print("\n ⬜ Update Waste Collection ")
    collection_id = input("Enter Collection ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_collections WHERE id = ?",
        (collection_id,)
    )
    collection = cursor.fetchone()
    if collection:
        waste_type = input(f"Enter new Waste Type [{collection[1]}]: ")
        quantity = input(f"Enter new Quantity (kg) [{collection[2]}]: ")
        city_id = input(f"Enter new City ID [{collection[3]}]: ")
        area_id = input(f"Enter new Area ID [{collection[4]}]: ")
        provider_id = input(f"Enter new Provider ID [{collection[5]}]: ")
        collection_date = input(f"Enter new Collection Date [{collection[6]}]: ")
        status = input(f"Enter new Status [{collection[7]}]: ")
        if waste_type:
            new_waste_type = waste_type
        else:
            new_waste_type = collection[1]
        if quantity:
            new_quantity = quantity
        else:
            new_quantity = collection[2]
        if city_id:
            new_city_id = city_id
        else:
            new_city_id = collection[3]
        if area_id:
            new_area_id = area_id
        else:
            new_area_id = collection[4]
        if provider_id:
            new_provider_id = provider_id
        else:
            new_provider_id = collection[5]
        if collection_date:
            new_collection_date = collection_date
        else:
            new_collection_date = collection[6]
        if status:
            new_status = status
        else:
            new_status = collection[7]
        cursor.execute("""
            UPDATE waste_collections
            SET waste_type = ?, quantity = ?, city_id = ?,
                area_id = ?, provider_id = ?, collection_date = ?,
                status = ?
            WHERE id = ?
        """, (
            new_waste_type, new_quantity, new_city_id,
            new_area_id, new_provider_id, new_collection_date,
            new_status, collection_id
        ))
        conn.commit()
        print("\nWaste Collection updated successfully!")
    else:
        print("Waste Collection not found!")
    conn.close() 
def delete_collection():
    print("\n ⬜ Delete Waste Collection ")
    collection_id = input("Enter Collection ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM waste_collections WHERE id = ?",
        (collection_id,)
    )
    collection = cursor.fetchone()
    if collection:
        confirm = input(
            f"Delete collection {collection[0]}? (yes/no): "
        )
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM waste_collections WHERE id = ?",
                (collection_id,)
            )
            conn.commit()
            print("Waste Collection deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("Waste Collection not found!")
    conn.close()

providers = []
def add_provider():
    print("\n ⬜ Add Service Provider ")
    provider_id = input("Enter Provider ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM providers WHERE id = ?",(provider_id,))
    if cursor.fetchone():
        print("Error: Provider ID already exists!")
        conn.close()
        return
    name = input("Enter Provider Name: ")
    service_type = input("Enter Service Type: ")
    city_id = input("Enter City ID: ")
    cursor.execute("""
        INSERT INTO providers (id, name, service_type, city_id)
        VALUES (?, ?, ?, ?)
    """, (provider_id, name, service_type, city_id))
    conn.commit()
    conn.close()
    print("\nService Provider added successfully!")
def view_providers():
    print("\n ⬜ Registered Service Providers ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM providers")
    providers = cursor.fetchall()
    conn.close()
    if not providers:
        print("No service providers registered yet.")
        return
    for provider in providers:
        print("Provider ID:", provider[0])
        print("Provider Name:", provider[1])
        print("Service Type:", provider[2])
        print("City ID:", provider[3]) 
def search_provider():
    print("\n ⬜ Search Service Provider ")
    provider_id = input("Enter Provider ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM providers WHERE id = ?",
        (provider_id,)
    )
    provider = cursor.fetchone()
    conn.close()
    if provider:
        print("\nService Provider Found!")
        print("Provider ID:", provider[0])
        print("Provider Name:", provider[1])
        print("Service Type:", provider[2])
        print("City ID:", provider[3])
    else:
        print("Service Provider not found!")  
def update_provider():
    print("\n ⬜ Update Service Provider ")
    provider_id = input("Enter Provider ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM providers WHERE id = ?",(provider_id,))
    provider = cursor.fetchone()
    if provider:
        name = input(f"Enter new Provider Name [{provider[1]}]: ")
        service_type = input(f"Enter new Service Type [{provider[2]}]: ")
        city_id = input(f"Enter new City ID [{provider[3]}]: ")
        if name:
            new_name = name
        else:
            new_name = provider[1]
        if service_type:
            new_service_type = service_type
        else:
            new_service_type = provider[2]
        if city_id:
            new_city_id = city_id
        else:
            new_city_id = provider[3]
        cursor.execute("""
            UPDATE providers
            SET name = ?, service_type = ?, city_id = ?
            WHERE id = ?
        """, (new_name, new_service_type, new_city_id, provider_id))
        conn.commit()
        print("\nService Provider updated successfully!")
    else:
        print("Service Provider not found!")
    conn.close()
def delete_provider():
    print("\n ⬜ Delete Service Provider ")
    provider_id = input("Enter Provider ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM providers WHERE id = ?",(provider_id,) )
    provider = cursor.fetchone()
    if provider:
        confirm = input(f"Delete provider {provider[1]}? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM providers WHERE id = ?",
                (provider_id,)
            )
            conn.commit()
            print("Service Provider deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("Service Provider not found!")
    conn.close()    

schedules = []
def add_schedule():
    print("\n ⬜ Add Collection Schedule ")
    schedule_id = input("Enter Schedule ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM schedules WHERE id = ?",
        (schedule_id,)
    )
    if cursor.fetchone():
        print("Error: Schedule ID already exists!")
        conn.close()
        return
    collection_id = input("Enter Collection ID: ")
    date = input("Enter Schedule Date (DD/MM/YYYY): ")
    time = input("Enter Schedule Time: ")
    provider_id = input("Enter Provider ID: ")
    status = input("Enter Schedule Status: ")
    cursor.execute("""
        INSERT INTO schedules
        (id, collection_id, date, time, provider_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        schedule_id, collection_id, date,
        time, provider_id, status
    ))
    conn.commit()
    conn.close()
    print("\nCollection Schedule added successfully!")
def view_schedules():
    print("\n ⬜ Registered Collection Schedules ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    conn.close()
    if not schedules:
        print("No schedules registered yet.")
        return
    for schedule in schedules:
        print("Schedule ID:", schedule[0])
        print("Collection ID:", schedule[1])
        print("Schedule Date:", schedule[2])
        print("Schedule Time:", schedule[3])
        print("Provider ID:", schedule[4])
        print("Schedule Status:", schedule[5])
def search_schedule():
    print("\n ⬜ Search Collection Schedule ")
    schedule_id = input("Enter Schedule ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schedules WHERE id = ?",
        (schedule_id,)
    )
    schedule = cursor.fetchone()
    conn.close()
    if schedule:
        print("\nCollection Schedule Found!")   
        print("Schedule ID:", schedule[0])
        print("Collection ID:", schedule[1])
        print("Schedule Date:", schedule[2])
        print("Schedule Time:", schedule[3])
        print("Provider ID:", schedule[4])
        print("Schedule Status:", schedule[5])
    else:
        print("Schedule not found!")
def update_schedule():
    print("\n ⬜ Update Collection Schedule ")
    schedule_id = input("Enter Schedule ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schedules WHERE id = ?",
        (schedule_id,)
    )
    schedule = cursor.fetchone()
    if schedule:
        collection_id = input( f"Enter new Collection ID [{schedule[1]}]: ")
        date = input(f"Enter new Schedule Date [{schedule[2]}]: " )
        time = input(f"Enter new Schedule Time [{schedule[3]}]: ")
        provider_id = input(f"Enter new Provider ID [{schedule[4]}]: ")
        status = input(f"Enter new Schedule Status [{schedule[5]}]: ")
        if collection_id:
            new_collection_id = collection_id
        else:
            new_collection_id = schedule[1]
        if date:
            new_date = date
        else:
            new_date = schedule[2]
        if time:
            new_time = time
        else:
            new_time = schedule[3]
        if provider_id:
            new_provider_id = provider_id
        else:
            new_provider_id = schedule[4]
        if status:
            new_status = status
        else:
            new_status = schedule[5]
        cursor.execute("""
            UPDATE schedules
            SET collection_id = ?, date = ?, time = ?,
                provider_id = ?, status = ?
            WHERE id = ?
        """, (
            new_collection_id, new_date, new_time,
            new_provider_id, new_status, schedule_id
        ))
        conn.commit()
        print("\nCollection Schedule updated successfully!")
    else:
        print("Schedule not found!")
    conn.close()
def delete_schedule():
    print("\n ⬜ Delete Collection Schedule ")
    schedule_id = input("Enter Schedule ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schedules WHERE id = ?",
        (schedule_id,)
    )
    schedule = cursor.fetchone()
    if schedule:
        confirm = input(
            f"Delete schedule {schedule[0]}? (yes/no): "
        )
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM schedules WHERE id = ?",
                (schedule_id,)
            )
            conn.commit()
            print("Collection Schedule deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        print("Schedule not found!")
    conn.close()    

requests = []
def add_request():
    print("\n ⬜ Add Waste Collection Request ")
    request_id = input("Enter Request ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM requests WHERE id = ?",
        (request_id,)
    )
    if cursor.fetchone():
        print("Error: Request ID already exists!")
        conn.close()
        return
    user_id = input("Enter User ID: ")
    waste_type = input("Enter Waste Type: ")
    quantity = input("Enter Quantity of Waste (kg): ")
    city_id = input("Enter City ID: ")
    area_id = input("Enter Area ID: ")
    preferred_date = input("Enter Preferred Date (DD/MM/YYYY): ")
    status = input("Enter Request Status: ")
    cursor.execute("""
        INSERT INTO requests
        (id, user_id, waste_type, quantity, city_id,
         area_id, preferred_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request_id, user_id, waste_type, quantity,
        city_id, area_id, preferred_date, status
    ))
    conn.commit()
    conn.close()
    print("\nWaste Collection Request added successfully!")
def view_requests():
    print("\n ⬜ Registered Waste Collection Requests ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()
    if not requests:
        print("No requests registered yet.")
        return
    for request in requests:
        print("Request ID:", request[0])
        print("User ID:", request[1])
        print("Waste Type:", request[2])
        print("Quantity (kg):", request[3])
        print("City ID:", request[4])
        print("Area ID:", request[5])
        print("Preferred Date:", request[6])
        print("Request Status:", request[7])
def search_request():
    print("\n ⬜ Search Waste Collection Request ")
    request_id = input("Enter Request ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM requests WHERE id = ?",
        (request_id,)
    )
    request = cursor.fetchone()
    conn.close()
    if request:
        print("\nWaste Collection Request Found!")
        print("Request ID:", request[0])
        print("User ID:", request[1])
        print("Waste Type:", request[2])
        print("Quantity (kg):", request[3])
        print("City ID:", request[4])
        print("Area ID:", request[5])
        print("Preferred Date:", request[6])
        print("Request Status:", request[7])
    else:
        print("Request not found!")
def update_request():
    print("\n ⬜ Update Waste Collection Request ")
    request_id = input("Enter Request ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM requests WHERE id = ?",
        (request_id,)
    )
    request = cursor.fetchone()
    if request:
        user_id = input(f"Enter new User ID [{request[1]}]: ")
        waste_type = input(f"Enter new Waste Type [{request[2]}]: ")
        quantity = input(f"Enter new Quantity (kg) [{request[3]}]: ")
        city_id = input(f"Enter new City ID [{request[4]}]: ")
        area_id = input(f"Enter new Area ID [{request[5]}]: ")
        preferred_date = input(
            f"Enter new Preferred Date [{request[6]}]: "
        )
        status = input(f"Enter new Request Status [{request[7]}]: ")
        if user_id:
            new_user_id = user_id
        else:
            new_user_id = request[1]
        if waste_type:
            new_waste_type = waste_type
        else:
            new_waste_type = request[2]
        if quantity:
            new_quantity = quantity
        else:
            new_quantity = request[3]
        if city_id:
            new_city_id = city_id
        else:
            new_city_id = request[4]
        if area_id:
            new_area_id = area_id
        else:
            new_area_id = request[5]
        if preferred_date:
            new_preferred_date = preferred_date
        else:
            new_preferred_date = request[6]
        if status:
            new_status = status
        else:
            new_status = request[7]
        cursor.execute("""
            UPDATE requests
            SET user_id = ?, waste_type = ?, quantity = ?,
                city_id = ?, area_id = ?, preferred_date = ?,
                status = ?
            WHERE id = ?
        """, (
            new_user_id, new_waste_type, new_quantity,
            new_city_id, new_area_id, new_preferred_date,
            new_status, request_id
        ))
        conn.commit()
        print("\nWaste Collection Request updated successfully!")
    else:
        print("Request not found!")
    conn.close()
def delete_request():
    print("\n ⬜ Delete Waste Collection Request ")
    request_id = input("Enter Request ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM requests WHERE id = ?",
        (request_id,)
    )
    request = cursor.fetchone()
    if request:
        print("\nRequest Found!")
        print("Request ID:", request[0])
        print("User ID:", request[1])
        print("Waste Type:", request[2])
        confirm = input("Delete this request? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM requests WHERE id = ?",
                (request_id,)
            )
            conn.commit()
            print("Request deleted successfully!")
        else:
            print("Request deletion cancelled!")
    else:
        print("Request not found!")
    conn.close()

bills = []
def generate_bill():
    print("\n ⬜ Generate Bill ")
    bill_id = input("Enter Bill ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM bills WHERE id = ?",
        (bill_id,)
    )
    if cursor.fetchone():
        print("Error: Bill ID already exists!")
        conn.close()
        return
    user_id = input("Enter User ID: ")
    collection_id = input("Enter Collection ID: ")
    quantity = float(input("Enter Quantity of Waste (kg): "))
    rate = float(input("Enter Rate per kg: "))
    total_amount = quantity * rate
    payment_status = input("Enter Payment Status: ")
    cursor.execute("""
        INSERT INTO bills
        (id, user_id, collection_id, quantity, rate,
         total_amount, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        bill_id, user_id, collection_id, quantity,
        rate, total_amount, payment_status
    ))
    conn.commit()
    conn.close()
    print("\nBill generated successfully!")
    print("Total Amount: ₹", total_amount)
def view_bills():
    print("\n ⬜ Registered Bills ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bills")
    bills = cursor.fetchall()
    conn.close()
    if not bills:
        print("No bills generated yet.")
        return
    for bill in bills:
        print("Bill ID:", bill[0])
        print("User ID:", bill[1])
        print("Collection ID:", bill[2])
        print("Quantity (kg):", bill[3])
        print("Rate per kg: ₹", bill[4])
        print("Total Amount: ₹", bill[5])
        print("Payment Status:", bill[6])
def search_bill():
    print("\n ⬜ Search Bill ")
    bill_id = input("Enter Bill ID to search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bills WHERE id = ?",
        (bill_id,)
    )
    bill = cursor.fetchone()
    conn.close()
    if bill:
        print("\nBill Found!")
        print("Bill ID:", bill[0])
        print("User ID:", bill[1])
        print("Collection ID:", bill[2])
        prin
def update_bill():
    print("\n ⬜ Update Bill ")
    bill_id = input("Enter Bill ID to update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bills WHERE id = ?",
        (bill_id,)
    )
    bill = cursor.fetchone()
    if bill:
        user_id = input(f"Enter new User ID [{bill[1]}]: ")
        collection_id = input(f"Enter new Collection ID [{bill[2]}]: ")
        quantity = input(f"Enter new Quantity [{bill[3]}]: ")
        rate = input(f"Enter new Rate per kg [{bill[4]}]: ")
        payment_status = input(f"Enter new Payment Status [{bill[6]}]: ")
        if user_id:
            new_user_id = user_id
        else:
            new_user_id = bill[1]
        if collection_id:
            new_collection_id = collection_id
        else:
            new_collection_id = bill[2]
        if quantity:
            new_quantity = float(quantity)
        else:
            new_quantity = bill[3]
        if rate:
            new_rate = float(rate)
        else:
            new_rate = bill[4]
        new_total_amount = new_quantity * new_rate
        if payment_status:
            new_payment_status = payment_status
        else:
            new_payment_status = bill[6]
        cursor.execute("""
            UPDATE bills
            SET user_id = ?, collection_id = ?, quantity = ?,
                rate = ?, total_amount = ?, payment_status = ?
            WHERE id = ?
        """, (
            new_user_id, new_collection_id, new_quantity,
            new_rate, new_total_amount, new_payment_status,
            bill_id
        ))
        conn.commit()
        print("\nBill updated successfully!")
        print("Updated Total Amount: ₹", new_total_amount)
    else:
        print("Bill not found!")
    conn.close()
def delete_bill():
    print("\n ⬜ Delete Bill ")
    bill_id = input("Enter Bill ID to delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bills WHERE id = ?",
        (bill_id,)
    )
    bill = cursor.fetchone()
    if bill:
        print("\nBill Found!")
        print("Bill ID:", bill[0])
        print("User ID:", bill[1])
        print("Collection ID:", bill[2])
        print("Total Amount: ₹", bill[5])
        print("Payment Status:", bill[6])
        confirm = input("Delete this bill? (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute(
                "DELETE FROM bills WHERE id = ?",
                (bill_id,)
            )
            conn.commit()
            print("Bill deleted successfully!")
        else:
            print("Bill deletion cancelled!")
    else:
        print("Bill not found!")
    conn.close()