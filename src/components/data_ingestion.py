import os
import sys 
import pandas as pd 
import numpy as np 
from pymongo import MongoClient
from zipfile import Path
from upload_data import uri

from src.exceptions import CustomException
from src.logger import logging

DATABASE_NAME = 'Creditcardfault'
COLLECTION_NAME = 'CreditData'

class DataIngestionConfig():
    def __init__(self,artifact_folder:str = os.path.join('artifacts')):
        self.artifact_folder = artifact_folder


class DataIngestion():
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def export_collection_from_db_as_dataframe(self,database_name,collection_name):
        '''
            Desc: This function will responsible for extracting collections from mongo db 
            as data frame
        '''
        try:
            logging.info('Data ingestion started')
            client = MongoClient(uri)
            logging.info('Connecting with mongo db atlas')
            collection = client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=['_id'],axis=1,inplace=True)
            logging.info('Data ingestion completed')
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_data_into_file_path(self)->pd.DataFrame:
        '''
            Desc: This method reads data from mongodb and saves it into artifacts.
        '''
        try:
            logging.info('Data exporting started')
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path,exist_ok=True)
            credit_data = self.export_collection_from_db_as_dataframe(
                DATABASE_NAME,
                COLLECTION_NAME
            )
            logging.info(f'Saving data into folder: {raw_file_path}')
            store_file_path = os.path.join(raw_file_path,'credit_card.csv')
            credit_data.to_csv(store_file_path,index=False)
            return store_file_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self)->Path:
        '''
            Desc: This method initiates the data ingestion components of training pipeline
        '''
        try:
            store_file_path = self.export_data_into_file_path()
            logging.info('Got the data from db and saved under artifact folder')
            return store_file_path 
        except Exception as e:
            raise CustomException(e,sys)
        


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()