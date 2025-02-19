import mysql.connector
from mysql.connector import Error

class DatabaseSetup:
    def __init__(self, user, password, host, database):
        """
        Initializes the database setup with connection details.

        Args:
            user (str): MySQL username
            password (str): MySQL password
            host (str): MySQL server host
            database (str): Name of the database
        """
        self.config = {
            "user": user,
            "password": password,
            "host": host,
            "database": database
        }
        self.database = database

    def create_database(self):
        """Creates the database if it does not exist."""
        try:
            connection = mysql.connector.connect(
                user=self.config["user"], 
                password=self.config["password"], 
                host=self.config["host"]
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"✅ Database '{self.database}' is ready.")
        except Error as e:
            print(f"❌ Error creating database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            connection = mysql.connector.connect(**self.config)
            print("✅ Connected to MySQL database.")
            return connection
        except Error as e:
            print(f"❌ Connection error: {e}")
            return None

    def table_exists(self, cursor, table_name):
        """Checks if a table already exists."""
        cursor.execute(f"""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s
        """, (self.database, table_name))
        return cursor.fetchone()[0] > 0

    def create_tables(self):
        """Creates the required tables in the database."""
        TABLES = {
            "users": """
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "sponsor": """
                CREATE TABLE sponsor (
                    sponsor_id INT AUTO_INCREMENT PRIMARY KEY,
                    sponsor_name TEXT
                )
            """,
            "audio_details": """
                CREATE TABLE audio_details (
                    audio_id INT AUTO_INCREMENT PRIMARY KEY,
                    audio_name TEXT NOT NULL,
                    audi_length TEXT NOT NULL
                )
            """,
            "chunk_details": """
                CREATE TABLE chunk_details (
                    chunk_id INT AUTO_INCREMENT PRIMARY KEY,
                    chunk_file_name TEXT,
                    chunk_text TEXT,
                    timestamps TEXT,
                    audio_id INT,
                    chunk_creation_date DATE,
                    chunk_creation_date_time DATETIME,
                    FOREIGN KEY (audio_id) REFERENCES audio_details(audio_id) ON DELETE CASCADE
                )
            """,
            "sponsor_occurrence": """
                CREATE TABLE sponsor_occurrence (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    audio_id INT,
                    chunk_id INT,
                    sponsor_id INT,
                    sponsor_frequency INT,
                    FOREIGN KEY (audio_id) REFERENCES audio_details(audio_id) ON DELETE CASCADE,
                    FOREIGN KEY (chunk_id) REFERENCES chunk_details(chunk_id) ON DELETE CASCADE,
                    FOREIGN KEY (sponsor_id) REFERENCES sponsor(sponsor_id) ON DELETE CASCADE
                )
            """
        }

        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor()
                for table_name, table_query in TABLES.items():
                    if self.table_exists(cursor, table_name):
                        print(f"⚠️ Table '{table_name}' already exists.")
                    else:
                        cursor.execute(table_query)
                        print(f"✅ Table '{table_name}' has been created.")
                connection.commit()
            except Error as e:
                print(f"❌ Error creating tables: {e}")
            finally:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    
    db_setup = DatabaseSetup(user="root", password="12345", host="localhost", database="sponsor_info")
    
    
    db_setup.create_database()
    
    
    db_setup.create_tables()
