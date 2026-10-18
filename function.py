users = []
def add_user():
    print("\n Add New User ")
    user_id = input("Enter User ID: ")
    for user in users:
        if user["id"] == user_id:
            print("Error: User ID already exists!")
            return
    name = input("Enter user name: ")
    phone = input("Enter phone number: ")
    city = input("Enter city: ")
    user = {
        "id": user_id,
        "name": name,
        "phone": phone,
        "city": city
    }
    users.append(user)
    print("\nUser added successfully!")
def view_users():
    print("\n  Registered Users ")
    if not users:
        print("No users registered yet.")
        return
    for user in users:
        print("User ID:", user["id"])
        print("Name:", user["name"])
        print("Phone:", user["phone"])
        print("City:", user["city"])
def search_user():
    print("\n Search User ")
    user_id = input("Enter User ID to search: ")
    for user in users:
        if user["id"] == user_id:
            print("\nUser Found!")
            print("Name:", user["name"])
            print("Phone:", user["phone"])
            print("City:", user["city"])
            return
    print("User not found!")
def update_user():
    print("\n Update User ")
    user_id = input("Enter User ID to update: ")
    for user in users:
        if user["id"] == user_id:
            name = input(f"Enter new name [{user['name']}]: ")
            phone = input(f"Enter new phone [{user['phone']}]: ")
            city = input(f"Enter new city [{user['city']}]: ")
            if name:
                user["name"] = name
            if phone:
                user["phone"] = phone
            if city:
                user["city"] = city
            print("\nUser updated successfully!")
            return
    print("User not found!")
def delete_user():
    print("\n Delete User ")
    user_id = input("Enter User ID to delete: ")
    for user in users:
        if user["id"] == user_id:
            confirm = input(f"Delete user {user['name']}? (yes/no): ")
            if confirm == "yes":
                users.remove(user)
                print("User deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("User not found!")
 
waste_types = []
def add_waste():
    print("\n Add Waste Type ")
    waste_id = input("Enter Waste ID: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            print("Error: Waste ID already exists!")
            return
    name = input("Enter Waste Name: ")
    category = input("Enter Waste Category: ")
    description = input("Enter Description: ")
    waste = {
        "id": waste_id,
        "name": name,
        "category": category,
        "description": description
    }
    waste_types.append(waste)
    print("\nWaste type added successfully!")
def view_waste():
    print("\n Registered Waste Types ")
    if not waste_types:
        print("No waste types registered yet.")
        return
    for waste in waste_types:
        print("Waste ID:", waste["id"])
        print("Waste Name:", waste["name"])
        print("Category:", waste["category"])
        print("Description:", waste["description"])
def search_waste():
        print("\n  Search Waste Type ")
        waste_id = input("Enter Waste ID to search: ")
        for waste in waste_types:
            if waste["id"] == waste_id:
                print("\nWaste Type Found!")
                print("Waste ID:", waste["id"])
                print("Waste Name:", waste["name"])
                print("Category:", waste["category"])
                print("Description:", waste["description"])
                return
        print("Waste type not found!")
def update_waste():
    print("\n Update Waste Type ")
    waste_id = input("Enter Waste ID to update: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            print("Leave a  blank")
            name = input(f"Enter new name [{waste['name']}]: ")
            category = input(f"Enter new category [{waste['category']}]: ")
            description = input(  f"Enter new description [{waste['description']}]: ")
            if name:
                waste["name"] = name
            if category:
                waste["category"] = category
            if description:
                waste["description"] = description
            print("\nWaste type updated successfully!")
            return
    print("Waste type not found!")
def delete_waste():
    print("\n  Delete Waste Type ")
    waste_id = input("Enter Waste ID to delete: ")
    for waste in waste_types:
        if waste["id"] == waste_id:
            confirm = input( f"Delete waste type {waste['name']}? (yes/no): "  )
            if confirm.lower() == "yes":
                waste_types.remove(waste)
                print("Waste type deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("Waste type not found!")    

cities = []
def add_city():
    print("\n Add City ")
    city_id = input("Enter City ID: ")
    for city in cities:
        if city["id"] == city_id:
            print("Error: City ID already exists!")
            return
    name = input("Enter City Name: ")
    state = input("Enter State Name: ")
    city = {
        "id": city_id,
        "name": name,
        "state": state
    }
    cities.append(city)
    print("\nCity added successfully!")
def view_cities():
    print("\n Registered Cities ")
    if not cities:
        print("No cities registered yet.")
        return
    for city in cities:
        print("City ID:", city["id"])
        print("City Name:", city["name"])
        print("State:", city["state\n"])  
def search_cities():
    print("\n Search City ")
    city_id = input("Enter City ID to search: ")
    for city in cities:
        if city["id"] == city_id:
            print("\nCity Found!")
            print("City ID:", city["id"])
            print("City Name:", city["name"])
            print("State:", city["state"])
            return
    print("City not found!")   
def update_city():
    print("\n Update City ")
    city_id = input("Enter City ID to update: ")
    for city in cities:
        if city["id"] == city_id:
            name = input(f"Enter new city name [{city['name']}]: ")
            state = input(f"Enter new state name [{city['state']}]: ")
            if name:
                city["name"] = name
            if state:
                city["state"] = state
            print("\nCity updated successfully!")
            return
    print("City not found!")
def delete_city():
    print("\n Delete City ")
    city_id = input("Enter City ID to delete: ")
    for city in cities:
        if city["id"] == city_id:
            confirm = input(
                f"Delete city {city['name']}? (yes/no): "
            )
            if confirm.lower() == "yes":
                cities.remove(city)
                print("\nCity deleted successfully!")
            else:
                print("Deletion cancelled.")
            return
    print("City not found!")
