import mysql.connector

# Database connection details
config = {
    "user": "root",  
    "password": "Mysql@123",  
    "host": "localhost",  
    "database": "sponsor_info",  
    "raise_on_warnings": True
}


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def _create_user_table(self,data):

        self.data = data
        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = 'users'
            """, (config["database"],))
            table_exists = self.cursor.fetchone()[0]
            
            if not table_exists:
                
                get_create_user_table = """
                    SELECT * FROM sponsor_info.sql_queries
                """
                self.cursor.execute(get_create_user_table)
                create_table_query = self.cursor.fetchall()[0][1]
                self.cursor.execute(create_table_query)
                self.connection.commit()
                print("Table 'users' created successfully.")

                fetch_sql_queries = """
                    SELECT * FROM sponsor_info.sql_queries
                    """
                self.cursor.execute(fetch_sql_queries)

                insert_query = self.cursor.fetchall()[1][1]
                print(f"THIS IS INSERT TABLE QUERY --------- {insert_query}")
                self.cursor.execute(insert_query, self.data)
                self.connection.commit()

            else:
                print("Table 'users' already exists.")
                print("Inserting records")

                fetch_sql_queries = """
                    SELECT * FROM sponsor_info.sql_queries
                    """
                self.cursor.execute(fetch_sql_queries)

                insert_query = self.cursor.fetchall()[1][1]
                print(f"THIS IS INSERT TABLE QUERY --------- {insert_query}")
                self.cursor.execute(insert_query, self.data)
                self.connection.commit()

                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

    def store_sponsor_details(self, data):
        try:
            self.data = data
            self._create_user_table(data)
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

    def close_db_connection(self):
        """
        Closing the cursor and database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")
