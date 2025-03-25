import subprocess
from pathlib import Path
import logging
from pydub.utils import mediainfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def chunk_audio_only(audio_file: str, segment_time: int = 200) -> list:
    """
    Chunks a single audio file into segments of given segment_time (in seconds).
    It creates a unique subdirectory for each audio file (based on its stem) under the base "Chunks" folder.
    
    Returns a sorted list of chunk file paths.
    """
    base_chunk_dir = Path("Chunks")
    base_chunk_dir.mkdir(exist_ok=True)
    
    file_stem = Path(audio_file).stem
    chunk_dir = base_chunk_dir / f"{file_stem}_chunks"
    chunk_dir.mkdir(exist_ok=True)
    
    chunk_path = chunk_dir / 'chunk_%d.mp3'
    
    # (Optional) Check duration using mediainfo
    try:
        info = mediainfo(audio_file)
        duration = float(info["duration"])
        logging.info(f"File {audio_file} duration: {duration:.2f}s")
    except Exception as e:
        logging.warning(f"Could not determine duration for {audio_file}: {e}")
    
    command = [
        'ffmpeg',
        '-i', audio_file,
        '-f', 'segment',
        '-segment_time', str(segment_time),
        '-c:a', 'libmp3lame',
        '-b:a', '192k',
        str(chunk_path)
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Audio file '{audio_file}' chunked successfully in {chunk_dir}.")
        chunks = sorted([str(p) for p in chunk_dir.iterdir() if p.is_file()])
        logging.info(f"Chunks for {audio_file}: {chunks}")
        return chunks
    except subprocess.CalledProcessError as e:
        logging.error(f"Error chunking audio file {audio_file}: {e.stderr.decode()}")
        return []
