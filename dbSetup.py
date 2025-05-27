import mysql.connector
from mysql.connector import Error
import pandas as pd
from pathlib import Path

class DatabaseSetup:
    def __init__(self, user, password, host, database):
        """
        Initializes the database setup with connection details.
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
            conn = mysql.connector.connect(
                user=self.config["user"],
                password=self.config["password"],
                host=self.config["host"]
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            print(f"✅ Database '{self.database}' is ready.")
        except Error as e:
            print(f"❌ Error creating database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            conn = mysql.connector.connect(**self.config)
            print("✅ Connected to MySQL database.")
            return conn
        except Error as e:
            print(f"❌ Connection error: {e}")
            return None

    def table_exists(self, cursor, table_name):
        """Checks if a table already exists."""
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.tables "
            "WHERE table_schema = %s AND table_name = %s",
            (self.database, table_name)
        )
        return cursor.fetchone()[0] > 0

    def create_tables(self):
        """Creates all required tables in the database."""
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
                    FOREIGN KEY (audio_id)
                      REFERENCES audio_details(audio_id)
                      ON DELETE CASCADE
                )
            """,
            "sponsor_occurrence": """
                CREATE TABLE sponsor_occurrence (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    audio_id INT,
                    chunk_id INT,
                    sponsor_id INT,
                    sponsor_frequency INT,
                    FOREIGN KEY (audio_id)
                      REFERENCES audio_details(audio_id)
                      ON DELETE CASCADE,
                    FOREIGN KEY (chunk_id)
                      REFERENCES chunk_details(chunk_id)
                      ON DELETE CASCADE,
                    FOREIGN KEY (sponsor_id)
                      REFERENCES sponsor(sponsor_id)
                      ON DELETE CASCADE
                )
            """
        }

        conn = self.connect()
        if not conn:
            return
        cursor = conn.cursor()
        for name, ddl in TABLES.items():
            if self.table_exists(cursor, name):
                print(f"⚠️ Table '{name}' already exists.")
            else:
                cursor.execute(ddl)
                print(f"✅ Table '{name}' created.")
        conn.commit()
        cursor.close()
        conn.close()

    def populate_from_csv(self, csv_path: str) -> None:
        """
        1) Ensures DB & tables exist,
        2) Reads CSV at csv_path,
        3) Inserts into audio_details & chunk_details.
        """
        # 1️⃣ Schema
        self.create_database()
        self.create_tables()

        # 2️⃣ Connect
        conn = self.connect()
        if not conn:
            return
        cursor = conn.cursor()

        # 3️⃣ Load CSV and insert
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            # insert into audio_details
            cursor.execute(
                "INSERT INTO audio_details (audio_name, audi_length) VALUES (%s, %s)",
                (row["audio_name"], row["audio_length"])
            )
            audio_id = cursor.lastrowid

            # insert corresponding chunks
            stem = Path(row["full_path"]).stem
            for chunk_file in sorted(Path("Chunks", stem).glob("chunk_*.mp3")):
                cursor.execute(
                    "INSERT INTO chunk_details (chunk_file_name, audio_id) "
                    "VALUES (%s, %s)",
                    (str(chunk_file), audio_id)
                )

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database populated from CSV")

if __name__ == "__main__":
    # Quick local test
    db = DatabaseSetup(user="root", password="12345",
                       host="localhost", database="sponsor_info")
    db.create_database()
    db.create_tables()
