import os 
import sys 
import pickle
from src.exceptions import CustomException
from src.logger import logging
from sklearn.metrics import accuracy_score

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
    
def evaluate_model(X_train,y_train,X_test,y_test,models:dict):
    '''
        Desc: This function responsible for evaluate our performance of models and than return dict
            of performance as report
    '''
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            model.fit(X_train,y_train)
            # predicting X_train
            y_train_pred = model.predict(X_train)
            # predicting X_test
            y_test_pred = model.predict(X_test)
            train_model_score = accuracy_score(y_train,y_train_pred)
            test_model_score = accuracy_score(y_test,y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e,sys)