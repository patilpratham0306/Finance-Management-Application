import mysql.connector  # Import the mysql.connector module
from mysql.connector import Error  # Import Error for exception handling
from database import create_connection
from utils import hash_password


def register_user():
    """Register a new user."""
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    password_hash = hash_password(password)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(query, (username, password_hash))
            connection.commit()
            print("User registered successfully!")
        except mysql.connector.IntegrityError:
            print("Username already exists. Please choose a different username.")
        except Error as e:
            print(f"Error registering user: {e}")
        finally:
            cursor.close()
            connection.close()

def login_user():
    """Authenticate a user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    password_hash = hash_password(password)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT user_id, password_hash FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result and result[1] == password_hash:
                print("Login successful!")
                return result[0]  # Return user_id for future use
            else:
                print("Invalid username or password.")
                return None
        except Error as e:
            print(f"Error during login: {e}")
        finally:
            cursor.close()
            connection.close()