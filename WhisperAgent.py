from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from groq import Groq
import whisper
from Sponsors import GetSponsors


load_dotenv()


class WhisperAgent:

    def __init__(self):

        # Open AI client initialization
        #self.api_key = os.getenv("GROQ_KEY")
        #self.client = Groq(api_key=self.api_key)

        self.model = whisper.load_model('large')
        # self.folder_path = audio_path
        
        

    def transcribe(self,chunk_dir):
        
        super_list = []

        try:
            for i in os.listdir(chunk_dir):
                chunk_path = os.path.join(chunk_dir,i)
                transcription = self.model.transcribe(chunk_path)
                segments = transcription['segments']

                
                for segment in segments:
                   super_list.append((f"{segment['start']} - {segment['end']}", segment['text']))
            

            
        except Exception as error:
            print(str(error))
        
        for i in os.listdir(chunk_dir):
            chunk_path = os.path.join(chunk_dir,i)
            os.unlink(chunk_path)
        
        print("Cleared all chunks..............")

        return super_list
                
