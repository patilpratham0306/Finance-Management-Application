from database import create_connection
from datetime import datetime
from mysql.connector import Error

def add_transaction(user_id):
    """Add a new income or expense entry."""
    try:
        transaction_type = input("Enter type (Income/Expense): ").capitalize()
        category = input("Enter category (e.g., Food, Rent, Salary): ").capitalize()
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-DD-MM): ")
        description = input("Enter description (optional): ")

        # Validate transaction type
        if transaction_type not in ["Income", "Expense"]:
            print("Invalid transaction type. Please enter 'Income' or 'Expense'.")
            return

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-DD-MM.")
            return

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    INSERT INTO transactions (user_id, type, category, amount, date, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, transaction_type, category, amount, date, description))
                connection.commit()
                print("Transaction added successfully!")
            except Error as e:
                print(f"Error adding transaction: {e}")
            finally:
                cursor.close()
                connection.close()
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def view_transactions(user_id):
    """View all transactions for the logged-in user."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC"
            cursor.execute(query, (user_id,))
            transactions = cursor.fetchall()

            if transactions:
                print("\nYour Transactions:")
                for transaction in transactions:
                    print(f"ID: {transaction['transaction_id']}")
                    print(f"Type: {transaction['type']}")
                    print(f"Category: {transaction['category']}")
                    print(f"Amount: {transaction['amount']}")
                    print(f"Date: {transaction['date']}")
                    print(f"Description: {transaction['description']}")
                    print("-" * 30)
            else:
                print("No transactions found.")
        except Error as e:
            print(f"Error fetching transactions: {e}")
        finally:
            cursor.close()
            connection.close()

def update_transaction(user_id):
    """Update an existing transaction."""
    try:
        transaction_id = int(input("Enter the transaction ID to update: "))
        new_amount = float(input("Enter the new amount: "))
        new_description = input("Enter the new description (optional): ")

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    UPDATE transactions
                    SET amount = %s, description = %s
                    WHERE transaction_id = %s AND user_id = %s
                """
                cursor.execute(query, (new_amount, new_description, transaction_id, user_id))
                connection.commit()
                if cursor.rowcount > 0:
                    print("Transaction updated successfully!")
                else:
                    print("No transaction found with the given ID.")
            except Error as e:
                print(f"Error updating transaction: {e}")
            finally:
                cursor.close()
                connection.close()
    except ValueError:
        print("Invalid input. Please enter a valid transaction ID and amount.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def delete_transaction(user_id):
    """Delete a transaction."""
    try:
        transaction_id = int(input("Enter the transaction ID to delete: "))

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "DELETE FROM transactions WHERE transaction_id = %s AND user_id = %s"
                cursor.execute(query, (transaction_id, user_id))
                connection.commit()
                if cursor.rowcount > 0:
                    print("Transaction deleted successfully!")
                else:
                    print("No transaction found with the given ID.")
            except Error as e:
                print(f"Error deleting transaction: {e}")
            finally:
                cursor.close()
                connection.close()
    except ValueError:
        print("Invalid input. Please enter a valid transaction ID.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")