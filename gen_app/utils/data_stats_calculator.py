import time 
import sys, os
import tracemalloc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class calc:
    # UNIVERSAL METHOD
    @staticmethod
    def timeMeasure(func):
        def wrapper(*args, **kwargs):
            t_start = time.process_time()
            result = func(*args, **kwargs)
            t_end = time.process_time()
            print(f"{func}: (Czas: {t_end - t_start} [s])")
            return result
        return wrapper

    # SINGLE OBJECT METHODS
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
    def sizeMeasure(obj):
        def wrapper(*args, **kwargs):
            result = obj(*args, **kwargs)
            print(f"{obj}: (Pojemność: {sys.getsizeof(result)} [bajtów])")
            return result
        return wrapper
    
    # MULTI OBJECT METHODS
    @staticmethod
    def traceFullMeasure(func):
        def wrapper(*args, **kwargs):
            t_start = time.process_time()
            tracemalloc.start()
            result = func(*args, **kwargs)
            curr_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            t_end = time.process_time()

            return result, t_end - t_start, curr_mem, peak_mem
        return wrapper

    @staticmethod
    def traceSizeMeasure(func):
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return result, current, peak
        return wrapper
