from pathlib import Path
import os
import whisper
import concurrent.futures
from datetime import datetime
from multiprocessing import Process , Queue
from rdascripts import Database
from concurrent.futures import ProcessPoolExecutor
import time
import requests
import torch

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

class TranscribeAudio:

    def __init__(self):
        pass

    def transcribe_wrapper(self,path):

        super_list = []

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model = whisper.load_model("base")

        if device == "cuda":
            model = model.half()
        
        for p in path:
              # Load inside the thread

            audio_name = p.split("\\")[1]
            #audio_name = audio_name.split("_")[0]
            audio_name = audio_name + ".mp3"

            chunk_name = p.split("\\")[2]

            db_obj = Database()
            audio_id = db_obj.get_audio_id(audio_name)


            result = model.transcribe(p)


            segments = result["segments"]


            chunk_creation_date = datetime.now().date()
            chunk_creation_date_time = datetime.now()

            chunk_time_stamps = ""
            chunk_text = ""
            previous_end_time = 0  # ← You had this missing in the original

            for segment in segments:
                start_time = segment['start'] + previous_end_time
                end_time = segment['end'] + previous_end_time
                chunk_time_stamps += f" {start_time} - {end_time} $!"
                chunk_text += f"{segment['text']} $!"

            
            chunk_details = {
                'chunk_file_name': f"{audio_name} / {chunk_name}",
                'chunk_text': chunk_text,
                #'timestamps': chunk_time_stamps,
                'audio_id': audio_id,
                #'chunk_creation_date': chunk_creation_date,
                #'chunk_creation_date_time': chunk_creation_date_time
            }



            save_transcription = SaveTranscription()

            save_transcription.save_transcription(chunk_details)

            # url = "https://expenseapp.creowiz.com/api/get_audio_data/"

            # resp = requests.post(url , data = chunk_details)

            # print(resp.status_code)

            super_list.append(chunk_details)





class SaveTranscription:

    def __init__(self):
        pass

    def save_transcription(self , chunk_details):
        
        try:
            url = "https://expenseapp.creowiz.com/api/get_audio_data/"

            resp = requests.post(url , data = chunk_details)

            print(resp.status_code)

        except Exception as error:
            return str(error)


class GetAudioPath:

    def __init__(self):
        pass


    def get_audio_chunks_path(self)-> list[list]: 

        chunks = Path("Chunks")

        chunk_list = []

        for i in os.listdir(chunks):

            chunk_full_path = []
            full_path = os.path.join(chunks, i)

            for files in os.walk(full_path):

                for i in files[2]:

                    chunk_full_path.append(os.path.join(full_path , i))

                chunk_list.append(chunk_full_path)

        return chunk_list

# chunk_list = get_audio_chunks_path()



# print(chunk_list)


# def transcribe():
#     start = time.perf_counter()
#     for i in chunk_list:
#         for j in i:
#             transcribe_wrapper(j)
#     end = time.perf_counter()

#     print(f"Total time elapsed {end - start : .4f}")
    
# transcribe()

# def main():

#     start = time.perf_counter()
#     for i in chunk_list:
#         with ProcessPoolExecutor() as executor:
#             executor.map(transcribe_wrapper, i)
#     end = time.perf_counter()

#     print(f"Total time taken {end - start:.4f}" )
# if __name__ == '__main__':
#     main()
    
class StartProcessing:

    def __init__ (self):
        pass

    def main(self):
        audio_obj = GetAudioPath()
        chunk_list = audio_obj.get_audio_chunks_path()


        transcriber_obj = TranscribeAudio()

        start = time.perf_counter()

        for i in range(0, len(chunk_list), 2):
            p1 = Process(target=transcriber_obj.transcribe_wrapper, args=(chunk_list[i],))
            #print(p1._identity)
            
            p2 = None
            if i + 1 < len(chunk_list):
                p2 = Process(target=transcriber_obj.transcribe_wrapper, args=(chunk_list[i + 1],))

            p1.start()
            if p2: p2.start()

            p1.join()
            if p2: p2.join()
        end = time.perf_counter()

        print(f"Total time elapsed {end - start : .4f}")

        return "Completed"



        # if __name__ == "__main__":
        #     self.main()
    

    

        #     for path in chunk_full_path:
        #         try:

        #             p1 = Process(model.transcribe , path)

        #             result = model.transcribe(path)
        #             chunk_result.append(result["segments"])
        #         except Exception as error:
        #             print(str(error))
        # print(chunk_result)

    # """ Create two process and assign the first audio file to process one
    #     And the second audio file to the second process . 
    
    # """


        #results = []
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     future_to_path = {executor.submit(model.transcribe, path): path for path in chunk_full_path}
        #     for future in concurrent.futures.as_completed(future_to_path):
        #         path = future_to_path[future]
        #         result = future.result()
        #         results.append((path , result))
        # print(results)
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
