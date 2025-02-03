import subprocess
from pathlib import Path
import pandas as pd
from WhisperAgent import WhisperAgent
from Sponsors import GetSponsors
import logging


logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(levelname)s - %(message)s')



class Chunker:


    def __init__(self , csv_path:str):

        self.model = WhisperAgent()

        self.chunk_dir = Path("Chunks")

        self.chunk_dir.mkdir(exist_ok=True)

        self.csv_path = csv_path
        
        self.chunk_path = self.chunk_dir / 'chunk_%d.mp3'


    def read_csv(self):

        df = pd.read_csv(self.csv_path)

        path_list = df['full_path'].to_list()
        
        for path in path_list:

            file_name = str(path).split("\\")[-1]
            is_completed = self.chunk_audio(path)

            if is_completed:

                transcription_list = self.model.transcribe(self.chunk_dir)

                print(f"THIS IS TRANSCRIPTION LIST {transcription_list}")


                try:
                    sponsors = GetSponsors()

                    
                    #logging.info("Getting sponsor names ...")

                    sponsors.get_sponsor(transcription_list , file_name)
                except Exception as e:
                    print(f"THIS IS THE ERROR {str(e)}")
        
                    



    def chunk_audio(self , audio_file):

        command = [
            'ffmpeg',
            '-i', audio_file,
            '-f', 'segment',
            '-segment_time', str(600),
            '-c:a', 'libmp3lame',
            '-b:a', '192k',
            self.chunk_path
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Audio file '{audio_file}' has been chunked successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while chunking the audio file: {e}")
            return False


