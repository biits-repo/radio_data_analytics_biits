import os
import sys
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GetCsv:
    def __init__(self, csv_path: str, root_folder: str):
        """
        Initializing the GetCsv class.

        Args:
            csv_path (str): Path to save the CSV file.
            root_folder (str): Root folder containing audio files.
        """
        self.csv_path = Path(csv_path)
        self.root_folder = Path(root_folder)

        # Validate paths
        self._validate_paths()

    def _validate_paths(self) -> None:
        """
        Validating that the provided paths exist and are accessible.
        """
        if not self.root_folder.exists() or not self.root_folder.is_dir():
            raise FileNotFoundError(f"Root folder '{self.root_folder}' does not exist or is not a directory.")

        # Ensure the CSV directory exists
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

    def get_audio_path(self) -> None:
        """
        Traverse the root folder, collect audio file paths, and save them to a CSV file.
        """
        try:
            audio_name_list: List[str] = []
            audio_path_list: List[str] = []

            # Traversing the root folder
            for folder in os.listdir(self.root_folder):
                folder_path = self.root_folder / folder

                if folder_path.is_dir():
                    for file_name in os.listdir(folder_path):
                        file_path = folder_path / file_name

                        if file_path.is_file():
                            audio_name_list.append(file_name)
                            audio_path_list.append(str(file_path))

            # Preparing data for CSV
            data: Dict[str, List[str]] = {
                "audio_name": audio_name_list,
                "full_path": audio_path_list,
            }

            # Here saving data to CSV
            if self.save_as_csv(data):
                logging.info("CSV creation completed successfully.")
            else:
                logging.error("CSV creation failed.")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def save_as_csv(self, data: Dict[str, List[str]]) -> bool:
        """
        Saving the provided data to a CSV file.

        Args:
            data (Dict[str, List[str]]): Data to save.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, index=False)
            return True
        except Exception as e:
            logging.error(f"Error saving CSV file: {e}")
            return False


def main():
    """
    Main function to execute the script.
    """
    # Checking if the required arguments are provided a=other wise raising error
    if len(sys.argv) < 3:
        logging.error("Example: python script.py <csv_path> <root_folder>")
        sys.exit(1)

    csv_path = sys.argv[1]
    root_folder = sys.argv[2]

    try:
        # Here Creating an instance of GetCsv and processing the audio paths
        obj = GetCsv(csv_path, root_folder)
        obj.get_audio_path()
    except Exception as e:
        logging.error(f"Script execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
