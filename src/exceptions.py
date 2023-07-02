import os
import sys 
from src.logger import logging

def error_message_details(error,error_detail:sys):
    '''
        Desc: This function will responsible for interact with python interpreter and catch your exception
        from os and python interpreter
    '''
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error ocurred in python script [{}] line number [{}] error message [{}]".format(
        file_name,
        exc_tb.tb_lineno,
        str(error)
    )

    return error_message


class CustomException(Exception):
    '''
        Desc: This is CustomException class which is inherited from parent class Exception
            basically here we called our init function of parent class and passed error 
            message in Exception class
    '''
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message,error_detail)

    def __str__(self) -> str:
        return self.error_message
    

if __name__ == '__main__':
    try:
        2/0
    except Exception as e:
        logging.info('Testing exceptions.py')
        raise CustomException(e,sys)