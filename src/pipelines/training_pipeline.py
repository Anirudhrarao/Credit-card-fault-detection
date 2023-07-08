from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data,store_file_path = obj.initiate_data_ingestion()
    dt = DataTransformation(store_file_path=store_file_path)
    train_arr,test_arr,_ = dt.initiate_data_transformation(train_path=train_data,test_path=test_data)
    model_trainer_obj = ModelTrainer()
    model_trainer_obj.initiate_model_trainer(train_arr=train_arr,test_arr=test_arr)