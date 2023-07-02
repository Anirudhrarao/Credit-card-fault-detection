import os 
import sys 
from datetime import datetime
import logging 

# Creating log file with current timestamp name
LOG_FILE = f"{datetime.now().strftime('%m-%d-%y-%H-%M-%S')}.log"

# Creating logs folder
log_path = os.path.join(os.getcwd(),'logs',LOG_FILE)

os.makedirs(log_path,exist_ok=True)

# joining log folder with log file
LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info("Testing logger.py file")