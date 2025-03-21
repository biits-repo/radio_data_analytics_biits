#Scheduler Code
import schedule
import time
from GetAudioPaths import main
import logging

logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)


schedule.every().day.at("18:21").do(main,"C:\\Users\\mohammad.adeeb\\OpenAIProject\\audio_path.csv","C:\\Folders")







while True:
    schedule.run_pending()
    # schedule.run_all()
    # schedule.clear()
