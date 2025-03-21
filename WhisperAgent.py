from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from groq import Groq
import whisper
from Sponsors import GetSponsors
from datetime import datetime




load_dotenv()


class WhisperAgent:

    def __init__(self):

        # Open AI client initialization
        #self.api_key = os.getenv("GROQ_KEY")
        #self.client = Groq(api_key=self.api_key)

        self.model = whisper.load_model('large')
    



    def transcribe(self,chunk_dir,file_name,audio_id):
        
        self.super_list = []

        self.audio_id = audio_id
        
        previous_end_time = 0  # Initialize to 0 to start the first chunk at 0

        try:
            for i in os.listdir(chunk_dir):
                self.chunk_details = {}
                self.chunk_time_stamps = ""
                self.chunk_text = ""

                chunk_path = os.path.join(chunk_dir, i)
                transcription = self.model.transcribe(chunk_path)
                segments = transcription['segments']

                self.chunk_creation_date = datetime.now().date()
                self.chunk_creation_date_time = datetime.now()

                for segment in segments:
                    # Adjust the start and end time based on the previous chunk's end time
                    start_time = segment['start'] + previous_end_time
                    end_time = segment['end'] + previous_end_time

                    # Update the timestamps string to reflect adjusted times
                    self.chunk_time_stamps += f" {start_time} - {end_time} $!"

                    # Append the segment text to the chunk's text
                    self.chunk_text += f"{segment['text']} $!"

                # Save chunk details
                self.chunk_details['chunk_file_name'] = f"{file_name} / {i}"
                self.chunk_details['chunk_text'] = self.chunk_text
                self.chunk_details['timestamps'] = self.chunk_time_stamps
                self.chunk_details['audio_id'] = self.audio_id
                self.chunk_details['chunk_creation_date'] = self.chunk_creation_date
                self.chunk_details['chunk_creation_date_time'] = self.chunk_creation_date_time

                # Add to the super list
                self.super_list.append(self.chunk_details)

                # Update the previous_end_time for the next chunk
                previous_end_time = segments[-1]['end']

        # try:
        #     for i in os.listdir(chunk_dir):

        #         self.chunk_details = {}
        #         self.chunk_time_stamps = ""
        #         self.chunk_text = ""

        #         chunk_path = os.path.join(chunk_dir,i)
        #         transcription = self.model.transcribe(chunk_path)
        #         segments = transcription['segments']

        #         self.chunk_creation_date = datetime.now().date()
        #         self.chunk_creation_date_time = datetime.now()

                
        #         for segment in segments:
                   
        #            self.chunk_text+= f"{segment['text']} $!"
        #            self.chunk_time_stamps+= f" {segment['start']} - {segment['end']} $!"
                
        #         self.chunk_details['chunk_file_name'] = f"{file_name} / {i}"
        #         self.chunk_details['chunk_text'] = self.chunk_text
        #         self.chunk_details['timestamps'] = self.chunk_time_stamps   
        #         self.chunk_details['audio_id'] = self.audio_id
        #         self.chunk_details['chunk_creation_date'] = self.chunk_creation_date
        #         self.chunk_details['chunk_creation_date_time'] = self.chunk_creation_date_time
            
        #         self.super_list.append(self.chunk_details)

            
            for i in self.super_list:
                print(i)
                print('\n'*5)

                   #super_list.append((f"{segment['start']} - {segment['end']}", segment['text']))
            

            
        except Exception as error:
            print(str(error))
        
        for i in os.listdir(chunk_dir):
            chunk_path = os.path.join(chunk_dir,i)
            os.unlink(chunk_path)
        
        print("Cleared all chunks..............")

        return self.super_list
                
