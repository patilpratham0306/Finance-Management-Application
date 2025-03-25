from database import create_connection
from datetime import datetime

def generate_monthly_report(user_id):
    """Generate a monthly financial report."""
    try:
        month = input("Enter the month (MM): ")
        year = input("Enter the year (YYYY): ")

        # Validate month and year
        datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid month or year. Please use the format MM for month and YYYY for year.")
        return

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT type, SUM(amount) as total
                FROM transactions
                WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
                GROUP BY type
            """
            cursor.execute(query, (user_id, month, year))
            results = cursor.fetchall()

            if results:
                total_income = 0
                total_expenses = 0

                print(f"\nMonthly Financial Report for {month}/{year}:")
                for row in results:
                    if row[0] == "Income":
                        total_income = row[1]
                        print(f"Total Income: {total_income}")
                    elif row[0] == "Expense":
                        total_expenses = row[1]
                        print(f"Total Expenses: {total_expenses}")

                savings = total_income - total_expenses
                print(f"Savings: {savings}")
            else:
                print("No transactions found for the specified month and year.")
        except Error as e:
            print(f"Error generating monthly report: {e}")
        finally:
            cursor.close()
            connection.close()

def generate_yearly_report(user_id):
    """Generate a yearly financial report."""
    try:
        year = input("Enter the year (YYYY): ")

        # Validate year
        datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid year. Please use the format YYYY.")
        return

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT type, SUM(amount) as total
                FROM transactions
                WHERE user_id = %s AND YEAR(date) = %s
                GROUP BY type
            """
            cursor.execute(query, (user_id, year))
            results = cursor.fetchall()

            if results:
                total_income = 0
                total_expenses = 0

                print(f"\nYearly Financial Report for {year}:")
                for row in results:
                    if row[0] == "Income":
                        total_income = row[1]
                        print(f"Total Income: {total_income}")
                    elif row[0] == "Expense":
                        total_expenses = row[1]
                        print(f"Total Expenses: {total_expenses}")

                savings = total_income - total_expenses
                print(f"Savings: {savings}")
            else:
                print("No transactions found for the specified year.")
        except Error as e:
            print(f"Error generating yearly report: {e}")
        finally:
            cursor.close()
            connection.close()