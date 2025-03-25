from database import create_connection
from mysql.connector import Error

def set_budget(user_id):
    """Set a monthly budget for a category."""
    try:
        category = input("Enter the category (e.g., Food, Rent, Entertainment): ").capitalize()
        monthly_limit = float(input("Enter the monthly budget limit: "))

        # Validate monthly limit
        if monthly_limit <= 0:
            print("Monthly budget limit must be greater than 0.")
            return

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    INSERT INTO budgets (user_id, category, monthly_limit)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE monthly_limit = %s
                """
                cursor.execute(query, (user_id, category, monthly_limit, monthly_limit))
                connection.commit()
                print(f"Budget set successfully for {category}!")
            except Error as e:
                print(f"Error setting budget: {e}")
            finally:
                cursor.close()
                connection.close()
    except ValueError:
        print("Invalid input. Please enter a valid monthly budget limit.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def view_budgets(user_id):
    """View all budgets for the logged-in user."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM budgets WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            budgets = cursor.fetchall()

            if budgets:
                print("\nYour Budgets:")
                for budget in budgets:
                    print(f"Category: {budget['category']}")
                    print(f"Monthly Limit: {budget['monthly_limit']}")
                    print("-" * 30)
            else:
                print("No budgets found.")
        except Error as e:
            print(f"Error fetching budgets: {e}")
        finally:
            cursor.close()
            connection.close()

def check_budget(user_id):
    """Check if the user has exceeded their budget for any category."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT b.category, b.monthly_limit, COALESCE(SUM(t.amount), 0) as total_spent
                FROM budgets b
                LEFT JOIN transactions t
                ON b.user_id = t.user_id AND b.category = t.category
                AND MONTH(t.date) = MONTH(CURRENT_DATE()) AND YEAR(t.date) = YEAR(CURRENT_DATE())
                WHERE b.user_id = %s
                GROUP BY b.category, b.monthly_limit
            """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            if results:
                print("\nBudget Status:")
                for row in results:
                    category = row['category']
                    monthly_limit = row['monthly_limit']
                    total_spent = row['total_spent']
                    remaining = monthly_limit - total_spent

                    print(f"Category: {category}")
                    print(f"Monthly Limit: {monthly_limit}")
                    print(f"Total Spent: {total_spent}")
                    print(f"Remaining: {remaining}")
                    if total_spent > monthly_limit:
                        print("Warning: You have exceeded your budget for this category!")
                    print("-" * 30)
            else:
                print("No budgets found.")
        except Error as e:
            print(f"Error checking budget: {e}")
        finally:
            cursor.close()
            connection.close()