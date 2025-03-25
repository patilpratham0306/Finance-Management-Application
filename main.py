from auth import register_user, login_user
from database import initialize_database
from transactions import add_transaction, view_transactions, update_transaction, delete_transaction
from reports import generate_monthly_report, generate_yearly_report
from budget import set_budget, view_budgets, check_budget
from persistence import backup_data, restore_data

def main():
    # Initialize the database
    initialize_database()

    while True:
        print("\nPersonal Finance Management App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        # Use match statement for the main menu
        match choice:
            case "1":
                register_user()
            case "2":
                user_id = login_user()
                if user_id:
                    transaction_menu(user_id)
            case "3":
                print("Exiting the application. Goodbye!")
                break
            case _:
                print("Invalid choice. Please try again.")

def transaction_menu(user_id):
    """Menu for income/expense tracking, financial reports, budgeting, and data persistence."""
    while True:
        print("\nTransaction Menu")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Generate Monthly Report")
        print("6. Generate Yearly Report")
        print("7. Set Budget")
        print("8. View Budgets")
        print("9. Check Budget Status")
        print("10. Backup Data")
        print("11. Restore Data")
        print("12. Back to Main Menu")
        choice = input("Choose an option: ")

        # Use match statement for the transaction menu
        match choice:
            case "1":
                add_transaction(user_id)
            case "2":
                view_transactions(user_id)
            case "3":
                update_transaction(user_id)
            case "4":
                delete_transaction(user_id)
            case "5":
                generate_monthly_report(user_id)
            case "6":
                generate_yearly_report(user_id)
            case "7":
                set_budget(user_id)
            case "8":
                view_budgets(user_id)
            case "9":
                check_budget(user_id)
            case "10":
                format = input("Enter backup format (csv/json): ").lower()
                backup_data(user_id, format)
            case "11":
                filename = input("Enter the backup filename (e.g., user_1_backup.csv): ")
                restore_data(user_id, filename)
            case "12":
                break
            case _:
                print("Invalid choice. Please try again.")

main()