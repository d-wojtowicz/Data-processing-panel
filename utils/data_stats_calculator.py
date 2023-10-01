import time #Pomiar czasu funkcji
import sys  #Pomiar wielkości obiektu
import pandas as pd
import seaborn as sns

from source.data_reader import *

class calc:
    @staticmethod
    def fullMeasure(func):
        def wrapper(*args, **kwargs):
            t_start = time.process_time()
            result = func(*args, **kwargs)
            t_end = time.process_time()
            print(f"{func}: (Czas: {t_end - t_start} [s]; Pojemność: {sys.getsizeof(result)} [bajtów])")
            return result
        return wrapper
    
    @staticmethod
    def timeMeasure(func):
        def wrapper(*args, **kwargs):
            t_start = time.process_time()
            result = func(*args, **kwargs)
            t_end = time.process_time()
            print(f"{func}: (Czas: {t_end - t_start} [s])")
            return result
        return wrapper

    @staticmethod
    def sizeMeasure(obj):
        def wrapper(*args, **kwargs):
            result = obj(*args, **kwargs)
            print(f"{obj}: (Pojemność: {sys.getsizeof(result)} [bajtów])")
            return result
        return wrapper
