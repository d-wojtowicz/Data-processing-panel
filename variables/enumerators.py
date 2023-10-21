from enum import Enum

class read_by(Enum):
    COLUMNS = "columns"
    ROWS = "rows"
    TUPLES = "tuples"
    NORMAL = "normal"
    CHUNKS = "chunks"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class read_from(Enum):
    TOP = "head"
    BOTTOM = "tail"
    RANDOM = "sample"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))    
    
class reader_tester(Enum):
    SEABORN = "seaborn"
    SKLEARN = "sklearn"
    INDIVIDUAL = "individual"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
