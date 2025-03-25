import csv
import json
from decimal import Decimal
from datetime import date
from database import create_connection
from mysql.connector import Error

def custom_serializer(obj):
    """
    Convert Decimal and datetime.date objects to JSON-serializable types.
    """
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    elif isinstance(obj, date):
        return obj.isoformat()  # Convert datetime.date to ISO format string
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def backup_data(user_id, format="csv"):
    """Backup user data to a file."""
    try:
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                # Fetch transactions
                cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
                transactions = cursor.fetchall()

                # Fetch budgets
                cursor.execute("SELECT * FROM budgets WHERE user_id = %s", (user_id,))
                budgets = cursor.fetchall()

                if not transactions and not budgets:
                    print("No data found to backup.")
                    return

                # Backup to CSV
                if format == "csv":
                    with open(f"user_{user_id}_backup.csv", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Table", "Data"])
                        for transaction in transactions:
                            writer.writerow(["transactions", json.dumps(transaction, default=custom_serializer)])
                        for budget in budgets:
                            writer.writerow(["budgets", json.dumps(budget, default=custom_serializer)])
                    print(f"Data backed up to user_{user_id}_backup.csv")

                # Backup to JSON
                elif format == "json":
                    data = {
                        "transactions": transactions,
                        "budgets": budgets
                    }
                    with open(f"user_{user_id}_backup.json", "w") as file:
                        json.dump(data, file, indent=4, default=custom_serializer)
                    print(f"Data backed up to user_{user_id}_backup.json")

                else:
                    print("Invalid backup format. Please choose 'csv' or 'json'.")

            except Error as e:
                print(f"Error fetching data for backup: {e}")
            finally:
                cursor.close()
                connection.close()
    except Exception as e:
        print(f"An unexpected error occurred during backup: {e}")

def restore_data(user_id, filename):
    """Restore user data from a backup file."""
    try:
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                if filename.endswith(".csv"):
                    # Restore from CSV
                    with open(filename, "r") as file:
                        reader = csv.reader(file)
                        next(reader)  # Skip header
                        for row in reader:
                            table = row[0]
                            data = json.loads(row[1])

                            if table == "transactions":
                                query = """
                                    INSERT INTO transactions (user_id, type, category, amount, date, description)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(query, (
                                    user_id, data["type"], data["category"], data["amount"], data["date"], data["description"]
                                ))
                            elif table == "budgets":
                                query = """
                                    INSERT INTO budgets (user_id, category, monthly_limit)
                                    VALUES (%s, %s, %s)
                                """
                                cursor.execute(query, (
                                    user_id, data["category"], data["monthly_limit"]
                                ))

                    connection.commit()
                    print(f"Data restored from {filename}")

                elif filename.endswith(".json"):
                    # Restore from JSON
                    with open(filename, "r") as file:
                        data = json.load(file)
                        for transaction in data["transactions"]:
                            query = """
                                INSERT INTO transactions (user_id, type, category, amount, date, description)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """
                            cursor.execute(query, (
                                user_id, transaction["type"], transaction["category"], transaction["amount"], transaction["date"], transaction["description"]
                            ))
                        for budget in data["budgets"]:
                            query = """
                                INSERT INTO budgets (user_id, category, monthly_limit)
                                VALUES (%s, %s, %s)
                            """
                            cursor.execute(query, (
                                user_id, budget["category"], budget["monthly_limit"]
                            ))

                    connection.commit()
                    print(f"Data restored from {filename}")

                else:
                    print("Invalid file format. Please use a CSV or JSON file.")

            except Error as e:
                print(f"Error restoring data: {e}")
            finally:
                cursor.close()
                connection.close()
    except Exception as e:
        print(f"An unexpected error occurred during restore: {e}")