from function import (add_user, view_users, search_user, update_user, delete_user,add_waste, view_waste, search_waste, update_waste, delete_waste,add_city, view_cities, search_cities, update_city, delete_city,add_collection, view_collections, search_collection,update_collection, delete_collection,add_provider, view_providers, search_provider,
update_provider, delete_provider,add_schedule, view_schedules, search_schedule,update_schedule, delete_schedule,add_request, view_requests, search_request,update_request, delete_request,generate_bill, view_bills, search_bill,update_bill, delete_bill)
print("      ♻️  BinGO")
print("Smart Waste Management System")
while True:
    print("\n  MAIN MENU  ")
    print("1. 🚹 User Management")
    print("2. 🗑️  Waste Management")
    print("3. 👥 Collection & Service Provider Management")
    print("4. 🗳️  Scheduling & Request  Management")
    print("5. 🧾 Billing")
    print("6. ➡️  Exit")
    choice = input("\nEnter your choice (1-8): ")
    if choice == "1":
        while True:
            print("\n  USER MANAGEMENT  ")
            print("1. User Operations")
            print("2. City Operations")
            print("3. Back to Main Menu")
            management_choice = input("\nEnter your choice: ")
            if management_choice == "1":
                while True:
                    print("\n   USER OPERATIONS   ")
                    print("1. Add User")
                    print("2. View Users")
                    print("3. Search User")
                    print("4. Update User")
                    print("5. Delete User")
                    print("6. Back")
                    user_choice = input("\nEnter your choice: ")
                    if user_choice == "1":
                        add_user()
                    elif user_choice == "2":
                        view_users()
                    elif user_choice == "3":
                        search_user()
                    elif user_choice == "4":
                        update_user()
                    elif user_choice == "5":
                        delete_user()
                    elif user_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "2":
                while True:
                    print("\n   CITY OPERATIONS   ")
                    print("1. Add City")
                    print("2. View Cities")
                    print("3. Search City")
                    print("4. Update City")
                    print("5. Delete City")
                    print("6. Back")
                    city_choice = input("\nEnter your choice: ")
                    if city_choice == "1":
                        add_city()
                    elif city_choice == "2":
                        view_cities()
                    elif city_choice == "3":
                        search_cities()
                    elif city_choice == "4":
                        update_city()
                    elif city_choice == "5":
                        delete_city()
                    elif city_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "3":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "2":
        while True:
            print("\n   WASTE MANAGEMENT  ")
            print("1. Add Waste Type")
            print("2. View Waste Types")
            print("3. Search Waste Type")
            print("4. Update Waste Type")
            print("5. Delete Waste Type")
            print("6. Back to Main Menu")
            waste_choice = input("\nEnter your choice: ")
            if waste_choice == "1":
                add_waste()
            elif waste_choice == "2":
                view_waste()
            elif waste_choice == "3":
                search_waste()
            elif waste_choice == "4":
                update_waste()
            elif waste_choice == "5":
                delete_waste()
            elif waste_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "3":
        while True:
            print("\n  COLLECTION & SERVICE PROVIDER MANAGEMENT")
            print("1. Service Provider Operations")
            print("2. Collection Operations")
            print("3. Back to Main Menu")
            management_choice = input("\nEnter your choice: ")
            if management_choice == "1":
                while True:
                    print("\n  SERVICE PROVIDER OPERATIONS")
                    print("1. Add Service Provider")
                    print("2. View Service Providers")
                    print("3. Search Service Provider")
                    print("4. Update Service Provider")
                    print("5. Delete Service Provider")
                    print("6. Back")
                    provider_choice = input("\nEnter your choice: ")
                    if provider_choice == "1":
                        add_provider()
                    elif provider_choice == "2":
                        view_providers()
                    elif provider_choice == "3":
                        search_provider()
                    elif provider_choice == "4":
                        update_provider()
                    elif provider_choice == "5":
                        delete_provider()
                    elif provider_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "2":
                while True:
                    print("\n  COLLECTION OPERATIONS")
                    print("1. Add Collection")
                    print("2. View Collections")
                    print("3. Search Collection")
                    print("4. Update Collection")
                    print("5. Delete Collection")
                    print("6. Back")
                    collection_choice = input("\nEnter your choice: ")
                    if collection_choice == "1":
                        add_collection()
                    elif collection_choice == "2":
                        view_collections()
                    elif collection_choice == "3":
                        search_collection()
                    elif collection_choice == "4":
                        update_collection()
                    elif collection_choice == "5":
                        delete_collection()
                    elif collection_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "3":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "4":
        while True:
            print("\n  SCHEDULING & REQUEST MANAGEMENT")
            print("1. Request Operations")
            print("2. Scheduling Operations")
            print("3. Back to Main Menu")
            management_choice = input("\nEnter your choice: ")
            if management_choice == "1":
                while True:
                    print("\n  REQUEST OPERATIONS")
                    print("1. Submit Request")
                    print("2. View Requests")
                    print("3. Search Request")
                    print("4. Update Request")
                    print("5. Delete Request")
                    print("6. Back")
                    request_choice = input("\nEnter your choice: ")
                    if request_choice == "1":
                        add_request()
                    elif request_choice == "2":
                        view_requests()
                    elif request_choice == "3":
                        search_request()
                    elif request_choice == "4":
                        update_request()
                    elif request_choice == "5":
                        delete_request()
                    elif request_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "2":
                while True:
                    print("\n  SCHEDULING OPERATIONS")
                    print("1. Add Schedule")
                    print("2. View Schedules")
                    print("3. Search Schedule")
                    print("4. Update Schedule")
                    print("5. Delete Schedule")
                    print("6. Back")
                    schedule_choice = input("\nEnter your choice: ")
                    if schedule_choice == "1":
                        add_schedule()
                    elif schedule_choice == "2":
                        view_schedules()
                    elif schedule_choice == "3":
                        search_schedule()
                    elif schedule_choice == "4":
                        update_schedule()
                    elif schedule_choice == "5":
                        delete_schedule()
                    elif schedule_choice == "6":
                        break
                    else:
                        print("Invalid choice! Please try again.")
            elif management_choice == "3":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "5":
        while True:
            print("\n  BILLING MANAGEMENT")
            print("1. Generate Bill")
            print("2. View Bills")
            print("3. Search Bill")
            print("4. Update Bill")
            print("5. Delete Bill")
            print("6. Back to Main Menu")
            billing_choice = input("\nEnter your choice: ")
            if billing_choice == "1":
                generate_bill()
            elif billing_choice == "2":
                view_bills()
            elif billing_choice == "3":
                search_bill()
            elif billing_choice == "4":
                update_bill()
            elif billing_choice == "5":
                delete_bill()
            elif billing_choice == "6":
                break
            else:
                print("Invalid choice! Please try again.")
    elif choice == "6":
        print("\nThank you for using BinGO! ♻️")
        break
    else:
        print("Invalid choice! Please enter a number from 1 to 7.")
   