from function import (add_user, view_users, search_user, update_user, delete_user,add_waste,
    view_waste,search_waste,update_waste,delete_waste)
print("      ♻️  BinGO",       "\nSmart Waste Management System")
while True:
    print("\n1. User Management")
    print("2. Waste Management")
    print("3. City & Area Management")
    print("4. Service Provider Management")
    print("5. Location-Based Service Availability")
    print("6. Smart Provider Matching")
    print("7. Collection Management")
    print("8. Scheduling")
    print("9. Request Management")
    print("10. Billing")
    print("11. Dashboard & A2nalytics")
    print("12. Reports")
    print("13. Exit")
    choice = input("\nEnter your choice (1-13): ")
    if choice == "1":
       while True:
        print("\n User Management ")
        print("1. Add User")
        print("2. View Users")
        print("3. Search User")
        print("4. Update User")
        print("5. Delete User")
        print("6. Back to Main Menu")
        user_choice = input("Enter your choice: ")
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
            print("Invalid choice! Try again.")
    elif choice == "2":
        while True:
            print("\n Waste Management ")
            print("1. Add Waste Type")
            print("2. View Waste Types")
            print("3. Search Waste Type")
            print("4. Update Waste Type")
            print("5. Delete Waste Type")
            print("6. Back to Main Menu")
            waste_choice = input("Enter your choice: ")
            if waste_choice == "1":
               add_waste()
            elif waste_choice == "2":
                view_waste()
            elif waste_choice == "3":
                search_waste()
            elif waste_choice == "4":
                update_waste() 
            elif  waste_choice == "5":
                delete_waste()     
            elif waste_choice == "6":
                break
            else:
               print("Invalid choice! Please try again.")

    elif choice == "4":
        print("Service Provider Management selected")
    elif choice == "5":
        print("Location Based Service Availability selected")
    elif choice == "6":
        print("Smart Provider Matching selected ")
    elif choice == "7":
        print("Collection Management selected")
    elif choice == "8":
        print("Scheduling selected")
    elif choice == "9":
        print("Request Management selected")
    elif choice == "10":
        print("Billing selected!")
    elif choice == "11":
        print("Dashboard & Analytics selected")
    elif choice == "12":
        print("Reports selected!")
    elif choice == "13":
        print("\nThank you for using BinGO! ♻️")
        break
    else:
        print("Invalid choice! Please enter a number from 1 to 13.")