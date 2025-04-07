from pathlib import Path
import os
import whisper
import concurrent.futures
from datetime import datetime

chunk_dir = Path("Chunks")

chunk_dir.mkdir(exist_ok=True)

model = whisper.load_model('large')



# for i in os.listdir(chunk_dir):
#     full_path = os.path.join(chunk_dir, i)
#     if os.path.isdir(full_path):
#         print(full_path)
#         for j in os.listdir(full_path):
#             print(j)


# for root , dir , files in os.walk(chunk_dir):
#     if dir:
#         for i in dir:
#             for j in os.listdir(os.path.join(root , i)):
#                 print(j)
#         break
#     else:
#         print("No directory found")

chunks = Path("Chunks")

super_list = []
previous_end_time = 0

for i in os.listdir(chunks):

    chunk_full_path = []
    chunk_details = {}
    chunk_time_stamps = ""
    chunk_text = ""

    full_path = os.path.join(chunks, i)

    for files in os.walk(full_path):

        for i in files[2]:

            chunk_full_path.append(os.path.join(full_path , i))
        
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(model.transcribe, path): path for path in chunk_full_path}
            for future in concurrent.futures.as_completed(future_to_path):
                path = future_to_path[future]
                result = future.result()
                results.append((path , result))
        print(results)
                # try:
                    #print(future.result()['text'])
                    # segments = future.result()['segments']

                    # chunk_creation_date = datetime.now().date()
                    # chunk_creation_date_time = datetime.now()

                    # for segment in segments:
                        # Adjust the start and end time based on the previous chunk's end time
                        # start_time = segment['start'] + previous_end_time
                        # end_time = segment['end'] + previous_end_time

                        # Update the timestamps string to reflect adjusted times
                        # chunk_time_stamps += f" {start_time} - {end_time} $!"

                        #print(chunk_time_stamps)

                        # Append the segment text to the chunk's text
                        # chunk_text += f"{segment['text']} $!"

                    # print(chunk_text)
                    
                        #print(" "*5)

                    # Save chunk details
                    #chunk_details['chunk_file_name'] = f"{file_name} / {i}"
                    ##chunk_details['chunk_text'] = chunk_text
                    ##chunk_details['timestamps'] = chunk_time_stamps
                    #chunk_details['audio_id'] = audio_id
                    ##chunk_details['chunk_creation_date'] = chunk_creation_date
                    ##chunk_details['chunk_creation_date_time'] = chunk_creation_date_time

                    # Add to the super list
                    ##super_list.append(chunk_details)

                    # Update the previous_end_time for the next chunk
                    ##previous_end_time = segments[-1]['end']
                

                # except Exception as exc:
                #     print(f"Audio file {path} generated an exception: {exc}")

    # print(super_list)
