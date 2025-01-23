import whisper
from pathlib import Path
import subprocess
import os


class TranscribingAgent:

    def __init__(self  , audio):
        
        self.model = whisper.load_model('large')
        self.audio_file = audio


        self.audio_dir = Path("Chunks")

        self.audio_dir.mkdir(exist_ok=True)
        

    def chunk_audio(self):

        chunk_path = self.audio_dir / 'chunk_%d.mp3'
        
        command = [
            'ffmpeg',
            '-i' , self.audio_file,
            '-f' , 'segment',
            '-segment_time' , str(600),
            '-c' , 'copy' ,
            '-c:a' , 'libmp3lame',
            '-b:a' , '128k',
            '-reset_timestamps' , '1',
            chunk_path
        ]

        try:
            chunk_path = subprocess.run(command , check = True , stderr = subprocess.PIPE)
            return True

        except subprocess.CalledProcessError as e:
            print(f"Eroor occurred while running ffmpeg: {e.stderr.decode()}")
            return False
        

    def transcribe_audio(self):

        chunker = self.chunk_audio()
        full_transcription = ""
        if chunker:

            audio_dir = Path("Chunks")

            for i in audio_dir.glob('chunk_*.mp3'):

                result = self.model.transcribe(str(i) )

                full_transcription+=result['text']

            print(full_transcription)
            
            for i in self.audio_dir.glob("chunk_*.mp3"):
                os.unlink(i)
        else:
            print("Error occurred while making chunks")


input_dir = Path("InputAudios")
audio_file_path = input_dir / "C:\\Users\\mohammad.adeeb\\Downloads\\InternetDownloads\\audio2.mp3"
model = TranscribingAgent(audio_file_path)
model.transcribe_audio()
