# TODO: Enhance usability of calc class methods (Full description below)


import time #Pomiar czasu funkcji
import sys  #Pomiar wielkości obiektu
import pandas as pd
import seaborn as sns

from source.data_reader import *

class calc:
    @staticmethod
    def timeMeasure(func):
        t_start = time.process_time()
        eval(func)
        t_end = time.process_time()
        return t_end - t_start

    @staticmethod
    def sizeMeasure(obj):
        return sys.getsizeof(eval(obj)) #[Bytes]
    

    """ timeMeasure and sizeMeasure functions pass parameters in the form of a string.
    Should instead work like delegates and pass ready functions as arguments. """
    # It should be corrected to something like this:

    """ 
    class calc:
    @staticmethod
    def timeMeasure(func):
        print("S")
        def wrapper(*args, **kwargs):
            t_start = time.process_time()
            print(str(func))
            t_end = time.process_time()
            return t_end - t_start
        return wrapper

    @staticmethod
    def sizeMeasure(obj):
        def wrapper(*args, **kwargs):
            return sys.getsizeof(obj(*args, **kwargs)) #[Bytes]
        return wrapper 
    """
