import re
from pathlib import Path
import numpy as np
import pandas as pd
import logging
import os

logging.basicConfig(level = logging.INFO , format = '%(asctime)s - %(levelname)s - %(message)s')


class GetSponsors:

    def __init__(self):
        pass



    def get_sponsor(self , super_list , file_name):
    # Keywords to identify sponsor mentions

        print(f"############## THIS IS THE FILE NAME {file_name}")
        i = 0
        lists = []
        lists_one = []
        while i < len(super_list):

            pattern_1 =  r'([Ss]ponsor(?:ed)? by|[Pp]owered by|[Bb]rought to you by)'


            match_1 = re.search(pattern_1, super_list[i][1])

            if match_1:
                lists.append(super_list[i][0])
                lists_one.append(super_list[i][1])

            else:
                pattern_1 =  r'([Ss]ponsor(?:ed)? by|[Pp]owered by|[Bb]rought to you by)'
                match_3 = re.search(pattern_1 , super_list[i][1])
                if match_3:
                    lists.append(super_list[i][0])
                    lists_one.append(super_list[i][1])

                    lists.append(super_list[i+1][0])
                    lists_one.append(super_list[i+1][1])



            i+=1

        data = {
            "Timestamps" : lists,
            "Sponsors_Shows" : lists_one
        }

        try:

            csv_path = Path("CSV")
            csv_path.mkdir(exist_ok=True)
            df = pd.DataFrame(data)
            # logging.info(file_name)

            file_name_copy= str(file_name)

            name = str(file_name).split('.')[0]
            ext = str(file_name).split('.')[1]

            file_name = file_name_copy.replace(ext , 'csv')

            logging.info(f"This is file name {file_name}")
            
            #file_name = os.path.join(csv_path,file_name)

            logging.info(f"This is file name {file_name}")

            df.to_csv(csv_path / file_name , index=False)
            logging.info("File saved sucessfully")
        except Exception as error:
            logging.error(f"LINE 61: ########################### {str(error)}")

        

        
