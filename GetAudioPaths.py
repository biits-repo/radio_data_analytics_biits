import os
import sys
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd
import concurrent.futures
from Chunking import chunk_audio_only  # New parallel chunking function
from WhisperAgent import WhisperAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GetCsv:
    def __init__(self, csv_path: str, root_folder: str):
        self.csv_path = Path(csv_path)
        self.root_folder = Path(root_folder)
        self._validate_paths()

    def _validate_paths(self) -> None:
        if not self.root_folder.exists() or not self.root_folder.is_dir():
            raise FileNotFoundError(f"Root folder '{self.root_folder}' does not exist or is not a directory.")
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

    def get_audio_path(self) -> bool:
        try:
            audio_name_list: List[str] = []
            audio_path_list: List[str] = []
            for item in os.listdir(self.root_folder):
                item_path = self.root_folder / item
                if item_path.is_file():
                    audio_name_list.append(item)
                    audio_path_list.append(str(item_path))
                elif item_path.is_dir():
                    for file in os.listdir(item_path):
                        file_path = item_path / file
                        if file_path.is_file():
                            audio_name_list.append(file)
                            audio_path_list.append(str(file_path))
            if not audio_path_list:
                logging.error("No audio files found in the provided root folder.")
                return False
            data: Dict[str, List[str]] = {"audio_name": audio_name_list, "full_path": audio_path_list}
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, index=False)
            logging.info(f"CSV creation completed successfully: {self.csv_path}")
            return True
        except Exception as e:
            logging.error(f"Error generating audio paths CSV: {e}")
            return False

# Top-level function for parallel processing (instead of lambda)
def process_file(file: str) -> (str, list):
    # Call the chunking function with a fixed segment time
    chunks = chunk_audio_only(file, segment_time=200)
    return file, chunks

def main():
    if len(sys.argv) < 3:
        logging.error("Usage: python GetAudioPaths.py <csv_output_path> <root_folder>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    root_folder = sys.argv[2]
    
    try:
        # Step 1: Generate CSV of audio file paths
        gc = GetCsv(csv_path, root_folder)
        if not gc.get_audio_path():
            sys.exit(1)
        
        df = pd.read_csv(csv_path)
        audio_files = df["full_path"].tolist()
        
        # Step 2: Parallel chunking for each audio file using a top-level function
        logging.info("Starting parallel chunking...")
        file_to_chunks = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Use the top-level process_file function for parallel mapping
            chunks_list = list(executor.map(process_file, audio_files))
        for file_path, chunks in chunks_list:
            file_to_chunks[file_path] = chunks
        
        # Step 3: Sequential transcription per file
        agent = WhisperAgent()
        all_segments = []
        for audio_file, chunks in file_to_chunks.items():
            logging.info(f"Transcribing file: {audio_file}")
            time_offset = 0
            for chunk in chunks:
                logging.info(f"Transcribing chunk: {chunk} with offset {time_offset:.2f}s")
                segments, last_end_time = agent.transcribe_chunk(chunk, time_offset)
                all_segments.extend(segments)
                time_offset = last_end_time
        
        # Step 4: Save aggregated transcription segments to CSV
        output_csv = "final_transcription_details.csv"
        final_df = pd.DataFrame(all_segments)
        Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_csv, index=False)
        logging.info(f"Final transcription details saved to {output_csv}")
    except Exception as e:
        logging.error(f"Script execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
