import subprocess
from pathlib import Path
import pandas as pd
# from WhisperAgent import WhisperAgent
from WhisperAgent import TranscribeAgent
from Sponsors import GetSponsors
import logging
import pandas as pd
from pydub.utils import mediainfo
from rdascripts import Database
logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(levelname)s - %(message)s')
import requests
import concurrent.futures



class Chunker:


    def __init__(self , csv_path:str):

        # self.model = WhisperAgent()



        # self.chunk_dir = Path("Chunks")

        # self.chunk_dir.mkdir(exist_ok=True)

        # self.csv_path = csv_path
        
        # self.chunk_path = str(self.chunk_dir / 'chunk_%d.mp3')

        #self.chunk_dir = Path("Chunks")
        #self.chunk_dir.mkdir(exist_ok=True)
        self.csv_path = csv_path
        #self.chunk_path = self.chunk_dir / 'chunk_%d.mp3'

        self.db_obj = Database()


    def read_csv(self):

        df = pd.read_csv(self.csv_path)

        path_list = df['full_path'].to_list()

        print(path_list)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(self.chunk_audio, path): path for path in path_list}
            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    future.result()
                except Exception as exc:
                    logging.error(f"Audio file {path} generated an exception: {exc}")

        
        for path in path_list:

            self.file_name = str(path).split("\\")[-1]
            is_completed = self.chunk_audio(path)

            
            self.audio_id = self.db_obj.get_audio_id(self.file_name)

            exit()
            if is_completed:
                
                
                self.model = TranscribeAgent()
                audio_chunk_list = self.model.transcribe(self.chunk_dir,self.file_name,self.audio_id)

                print(f"THIS IS TRANSCRIPTION LIST {audio_chunk_list}")

                inserted_chunk_data = self.db_obj.store_chunk_details(audio_chunk_list)

                if inserted_chunk_data:

                    print("DATA INSERTED SUCCESSFULLY IN CHUNK DETAILS TABLE")

                    saved_sponsors = self.db_obj.save_sponsors(self.audio_id)
                    if saved_sponsors:
                        print("Sponsor saved in sponsor table successfully")
                    else:
                        print("Failed to save sponsor in sponsor table")

                else:
                    print("DATA INSERTION FAILED IN CHUNK DETAILS TABLE")


                # try:
                #     sponsors = GetSponsors()

                    
                #     #logging.info("Getting sponsor names ...")

                #     sponsors.get_sponsor(transcription_list , file_name)
                # except Exception as e:
                #     print(f"THIS IS THE ERROR {str(e)}")
        
                    
    def get_audio_length(self , audio_path:str):

        self.audio_data = {}

        self.audio_info = mediainfo(audio_path)
        self.total_seconds = float(self.audio_info["duration"])

        self.hours = int(self.total_seconds // 3600)
        self.minutes = int((self.total_seconds % 3600) // 60)
        self.seconds = self.total_seconds % 60

        # Print the result
        self.audio_length = f"{self.hours}:{self.minutes}:{self.seconds:.0f}"

        self.audio_name = audio_path.split("\\")[-1]

        self.audio_data['audio_name'] = self.audio_name
        self.audio_data['audi_length'] = self.audio_length

        return self.audio_data    
    



    def store_audio_data(self):

        # self.csv_path = csv_path

        self.df = pd.read_csv(self.csv_path)

        self.path_list = self.df['full_path'].to_list()

        audio_data_list = []
        for i in self.path_list:
            audio_data_list.append(self.get_audio_length(i))
        
        try:
            
            data_inserted = self.db_obj.store_audio_data(audio_data_list)

            if data_inserted:
                 return True
            else:
                return False

        except Exception as error:
        
            print(f"THIS IS THE ERROR Chunking.py file: store_audio_data():  {str(error)}")



    def chunk_audio(self , audio_file):

        base_chunk_dir = Path("Chunks")
        base_chunk_dir.mkdir(exist_ok=True)
        
        file_stem = Path(audio_file).stem
        chunk_dir = base_chunk_dir / f"{file_stem}_chunks"
        chunk_dir.mkdir(exist_ok=True)
    
        chunk_path = chunk_dir / 'chunk_%d.mp3'

        command = [
            'ffmpeg',
            '-i', audio_file,
            '-f', 'segment',
            '-segment_time', str(200),
            '-c:a', 'libmp3lame',
            '-b:a', '192k',
            chunk_path
            #self.chunk_path
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Audio file '{audio_file}' has been chunked successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while chunking the audio file: {e}")
            return False

    
