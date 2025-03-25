import mysql.connector
from mysql.connector import Error

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'finance_app'
}

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                )
            """)

            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type ENUM('Income', 'Expense') NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    date DATE NOT NULL,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            # Create budgets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    budget_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    monthly_limit DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            connection.commit()
            print("Database initialized successfully!")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()