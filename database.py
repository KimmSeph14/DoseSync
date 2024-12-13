import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dosesync"
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
        else:
            print("Failed to connect to the database")
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

def create_database_and_tables():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create the dosesync database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS dosesync")

            # Use the dosesync database
            cursor.execute("USE dosesync")

            # Create the users table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """)

            # Insert default data if the table is empty
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            if user_count == 0:
                cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")

            connection.commit()
            cursor.close()
            connection.close()

            print("Database and table are set up.")
        else:
            print("Failed to connect to MySQL server.")

    except Error as e:
        print(f"Error while setting up database: {e}")

def main():
    create_database_and_tables()

if __name__ == "__main__":
    main()
