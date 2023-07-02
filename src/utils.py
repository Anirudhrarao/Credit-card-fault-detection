import os 
import sys 
import pickle
from src.exceptions import CustomException
from src.logger import logging

def save_object(file_path,obj):
    '''
        Desc: This function responsible for saving our pickle file
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
            
    except Exception as e:
        raise CustomException(e,sys)