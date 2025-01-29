# Radio_Data_Analytics_BIITS

> This projects uses whipser model for the audio transcription where we have to pass the audio file since audio file could be large so we are chunking first and then passing the audio chunks.
> And from that audio chunks we are getting the output as transcribed txt.
> From that response we are extracting the sponsor names , show names with there corresponding timestamps and saving as a CSV file


## Features
- Supports multiple audio formats (MP3, WAV, etc.).
- High-accuracy transcription using Whisper("large").
- Saving transcription in text file sponsor names and show names in CSV format with there corresponding timestamps.

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ai-ml-biits/radio_data_analytics_biits.git
   cd your-repo

2. **Create your virtual enviroment**
   ```bash
       python -m venv your_env_name
       your_user_dir:.\env\Scripts\activate
       (your_env_name): Like this will come after activating virtual enviroment
   
3. **Install all dependencies from requirements.txt**
    ```bash
        pip install -r requirements.txt

4. **Install ffmpeg**
   '''bash 
      > On macOS: brew install ffmpeg
      > On Linux: sudo apt install ffmpeg
      > On Windows: Download from FFmpeg's website and add it to your PATH. (https://www.gyan.dev/ffmpeg/builds/) [ffmpeg-git-full.7z] Download this file from the website
      
      
5. ***After this all you can run python script**
   ```bash
      python WhisperAgent.py


**NOTE**: **Recomended python version - 3.11.0**




  
