import mysql.connector
import pandas as pd
import numpy as np
import spacy
import re
from pathlib import Path
import os
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
        self.nlp = spacy.load('en_core_web_lg')

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



    # Here storing all the audio path in database
    def store_audio_data(self,audio_data):

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            query = "SELECT * FROM sponsor_info.sql_queries"
            self.cursor.execute(query)
            query = self.cursor.fetchall()[3][1]

            for i in audio_data:
                self.cursor.execute(query, i)
                self.connection.commit()

            self.close_db_connection()

            return True
        except Exception as e:
            print(f"Error dbacript stire_audio_details(): {e}")

    #Get Audio Id

    # def get_audio_id(self, file_name):

    #     try:
    #         self.connection = mysql.connector.connect(**config)
    #         self.cursor = self.connection.cursor()
    #         query = "SELECT audio_id FROM audio_details WHERE audio_name = %s"
    #         self.cursor.execute(query, (file_name,))
    #         audio_id = self.cursor.fetchone()[0]
    #         self.cursor.fetchall()
    #         self.close_db_connection()

    #         return audio_id
        
    #     except Exception as error:

    #         print(f"Error in rdascript.py file -> function: get_audio_id () -> {error}")
    


    def store_chunk_details(self,chunk_data:list):
        

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
            
            query = "SELECT * FROM sponsor_info.sql_queries"
            self.cursor.execute(query)
            insert_chunk_query = self.cursor.fetchall()[4][1]

            for i in chunk_data:

                self.cursor.execute(insert_chunk_query,i)
                self.connection.commit()

            self.close_db_connection()

            return True
        

        except Exception as error:
            print(f"Error in rdascript.py file -> function: store_chunk_details () -> {error}")
            return False
    
    def save_json(self,csv_data):
        
        print(f"THIS IS HE CSV DATA ############## {csv_data}")

        csv_path = Path("JSON")
        csv_path.mkdir(exist_ok=True)


        try:
            csv_name = "all_csv.csv"

            print(csv_path)
            print(csv_path)
            file_name = csv_data["audio_name"].split('/')[0].split('.')[0]
            file_name = file_name + '.json'

            csv_file_path = os.path.join(csv_path,file_name)
            df = pd.DataFrame(csv_data) 
            df.to_json(csv_file_path,index=False)
            

        except Exception as error:
            print(f"Error in rdascript.py file -> function: save_csv () -> {error}")


    def save_csv(self,csv_data):
        
        print(f"THIS IS HE CSV DATA ############## {csv_data}")

        csv_path = Path("CSV")
        csv_path.mkdir(exist_ok=True)


        try:
            csv_name = "all_csv.csv"

            print(csv_path)
            print(csv_path)
            file_name = csv_data["audio_name"].split('/')[0].split('.')[0]
            file_name = file_name + '.csv'

            csv_file_path = os.path.join(csv_path,file_name)
            df = pd.DataFrame(csv_data)
            df.to_csv(csv_file_path,index=False)
            

        except Exception as error:
            print(f"Error in rdascript.py file -> function: save_csv () -> {error}")

    def get_sponsor(self,chunk_details):

        try:
            file_name =   chunk_details[0][1].split("/")[0]
            sponsor_detail_dict = {}

            csv_data = {}

            super_list = []

            unique_sponsors = set()

            pattern = r'([Ss]ponsor(?:ed)? by|[Pp]owered by|[Bb]rought to you by)'

            self.audio_name = []
            self.chunk_text_data = []
            for i in chunk_details:

                sponsor_name_list = set()

                print(f"THIS IS CHUNK {i[2]}")

                match = re.search(pattern, i[2])
                
                
                sponsor_text_data = []
                if match:
                    
                    doc = self.nlp(i[2])

                    for ent in doc.ents:

                        if ent.label_ in ["ORG","PERSON"]:
                            
                            sponsor_name_list.add(ent.text)
                            unique_sponsors.add(ent.text)

                    sponsor_name_list = list(sponsor_name_list)
                    

                
                audio_file_name = i[1]
                self.audio_name.append(i[1])
                self.chunk_text_data.append(i[2])
            
                csv_data['audio_name'] = i[1]
                csv_data['chunk_text'] = i[2]
                csv_data['sponsor_name'] = sponsor_name_list
                    
            

                    
                sponsor_detail_dict[i[1]] = sponsor_name_list

            print(self.audio_name)

            print(self.chunk_text_data)

            self.save_csv(csv_data)
            self.save_json(csv_data)

            print(f"THIS IS UNIQUE SPONSOR{unique_sponsors}")

            print(f"THIS IS SPONSOR DICT {sponsor_detail_dict}")

            self.store_chunk_occurence(unique_sponsors,sponsor_detail_dict,file_name)

            return list(unique_sponsors)
        except Exception as error:
            print(f"Error in rdascript.py file -> function: get_sponsor () -> {error}")


    def sponsor_count(self,records:tuple,sponsor_detail_dict:dict)-> dict:
    
        sponsor_count_dict = {}
        
        try:
            for key in sponsor_detail_dict.keys():
                
                data = {}

                list_of_names = sponsor_detail_dict.get(key)

                for i in records:
                    
                    if i[1] in list_of_names:

                        data[i[0]] = data.get(i[0],0)+1

                sponsor_count_dict[key] = data
                
            
            return sponsor_count_dict
        except Exception as error:
            print(f"Error in rdascript.py file -> function: sponsor_count () -> {error}")


    def get_chunk_ids(self,audio_file_name:str)->list:

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            print(audio_file_name)
            query = "SELECT * FROM sponsor_info.chunk_details where chunk_file_name LIKE %s "

            self.cursor.execute(query,(f"{audio_file_name}%",))
            chunk_ids = [i[0] for i in self.cursor.fetchall()]

            self.cursor.close()  
            self.connection.close()

            return chunk_ids
        except Exception as error:
            print(f"Error in rdascript.py file -> function: get_chunk_ids () -> {error}")

    def store_chunk_occurence(self,unique_sponsor,sponsor_detail_dict,file_name):
        try:
            unique_sponsors = list(unique_sponsor)

            #place holder for passing to the sql query
            placeholder = ', '.join(['%s'] * len(unique_sponsors))


            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            query = f"SELECT * FROM sponsor_info.sponsor where sponsor_name IN ({placeholder})"

            self.cursor.execute(query,unique_sponsors)

            records = self.cursor.fetchall()
            self.close_db_connection()

            print(f"THIS IS RECORDS {records}")

            sponsor_counts = self.sponsor_count(records, sponsor_detail_dict)

            chunk_ids = self.get_chunk_ids(file_name)

            audio_id = None#self.get_audio_id(file_name)

            print(f"LINE NO 303 --------------------- {audio_id}")

            self.store_sponsor_details_occurence(sponsor_counts,chunk_ids,audio_id)

        except Exception as error:
            print(f"Error in rdascript.py file -> function: store_chunk_details () -> {error}")

    def get_chunk_ids(self,audio_file_name:str)->list:

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            print(audio_file_name)
            query = "SELECT * FROM sponsor_info.chunk_details where chunk_file_name LIKE %s "

            self.cursor.execute(query,(f"{audio_file_name}%",))
            chunk_ids = [i[0] for i in self.cursor.fetchall()]

            self.cursor.close()  
            self.connection.close()

            return chunk_ids
        except Exception as error:
            print(f"Error in rdascript.py file -> function: get_chunk_ids () -> {error}")
    

    def get_audio_id(self,file_name):

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            print(f"THIS IS FILE NAME   {file_name}")
            query = "SELECT audio_id FROM audio_details WHERE audio_name = %s"
            self.cursor.execute(query, (file_name,))
            audio_id = self.cursor.fetchall()[0][0]
            
            print(audio_id)

            return audio_id
        except Exception as error:
            print(f"Error in rdascript.py file -> function: get_audio_id () LINE 353-> {error}")

        finally:
            self.close_db_connection()

    def save_sponsors(self,audio_id):
        
        self.audio_id = audio_id

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            query = "SELECT * FROM sponsor_info.chunk_details where audio_id = %s"
            self.cursor.execute(query, (self.audio_id,))
            chunk_details = self.cursor.fetchall()
            
            print(f"THIS IS HE CHUNK DETAILS {chunk_details}")

            #Getting all unique spossors from chunk details

            unique_sponsors = self.get_sponsor(chunk_details)

            print(f"THIS IS UNIQUE SPONSOR {unique_sponsors}")

            if unique_sponsors:
                
                print("ALL UNIQUE SPONSORS")
                self.connection = mysql.connector.connect(**config)
                self.cursor = self.connection.cursor()
                query = "SELECT * FROM sponsor_info.sponsor"
                self.cursor.execute(query)
                existing_sponsor = [i[1] for i in self.cursor.fetchall()]

                print(f"THIS IS EXISTIMG SPONSOR {existing_sponsor}")

                try:
                    for i in unique_sponsors:

                        if i not in existing_sponsor:

                            query = "SELECT * FROM sponsor_info.sql_queries"
                            self.cursor.execute(query)
                            query = self.cursor.fetchall()[5][1]

                            data = {
                                    'sponsor_name': i
                                }
                            self.cursor.execute(query,data)
                            self.connection.commit()

                        else:
                            continue

                    return True
                except Exception as error:
                    print(f"THIS IS THE ERROR RDASCRIPT.PY save_sponsor() ->{str(error)}")

                # query = "SELECT * FROM sponsor_info.sponsor_info"
                # self.cursor.execute(query)
                # existing_sponsor = [i[1] for i in self.cursor.fetchall()]

                # placeholder = ', '.join(['%s'] * len(unique_sponsors))

                # query = f"SELECT * FROM sponsor_info.sponsor where sponsor_name IN ({placeholder})"

                # for i in unique_sponsors:
                #     if i not in existing_sponsor:
                #         self.cursor.execute(query,(i,))
                
                # records = self.cursor.fetchall()

            


        except Exception as error:
            print(f"Error in rdascript.py file -> function: save_sponsors () -> {error}")
        
    
    def store_sponsor_details_occurence(self,sponsor_counts:dict , chunk_ids:list , audio_id:int):

    # chunk_id , sponsor_id  , sponsor_count
        self.audio_id = audio_id

        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

        query = "SELECT audio_id FROM sponsor_info.chunk_details where chunk_id = %s"
        self.cursor.execute(query,(chunk_ids[0],))
        audio_id = self.cursor.fetchone()[0]

        print(f"THIS IS THE AUDIO ID INSIDE 429 SPONSOR OCCURENCE {audio_id}")
        try:
            list_details = []
            for i in chunk_ids:
                
                for key , value in sponsor_counts.items():
                    
                    for id , val in value.items():
                        data = {}
                        data['audio_id'] = audio_id
                        data['chunk_id'] = i
                        data['sponsor_id'] = id
                        data['sponsor_frequency'] = val

                        list_details.append(data)

            print(list_details)


            print("########################  ###################### ##################")

            print(f"THIS IS THE LIST {list_details}")

            self.inserting_chunk_occurence(list_details)

        except Exception as error:
            print(f"Error in rdascript.py file -> function: store_sponsor_details_occurence () {str(error)}")

        
    def inserting_chunk_occurence(self,list_details):

        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()

            query = "SELECT * FROM sponsor_info.sql_queries"
            self.cursor.execute(query)
            insert_query = self.cursor.fetchall()[6][1]

            for i in list_details:
                self.cursor.execute(insert_query , i)
                self.connection.commit()
            self.close_db_connection()

            print("SPONSOR OCCURENCE STORED SUCCEEFULLY")

        except Exception as error:
            print(f"Error in rdascript.py file -> function: inserting_chunk_occurence () {str(error)}")



    def close_db_connection(self):
        """
        Closing the cursor and database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")
