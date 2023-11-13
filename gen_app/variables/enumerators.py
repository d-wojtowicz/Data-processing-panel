from enum import Enum

class read_by(Enum):
    NORMAL = "Normal"
    COLUMNS = "Columns"
    ROWS = "Rows"
    TUPLES = "Tuples"
    CHUNKS = "Chunks"
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def seaborn_sklearn_gen_list(cls):
        return ["Rows", "Tuples", "Chunks"]
    
class read_from(Enum):
    TOP = "Top"
    BOTTOM = "Bottom"
    RANDOM = "Random"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))    
    
class reader_tester(Enum):
    SEABORN = "Seaborn"
    SKLEARN = "Sklearn"
    GENERATED = "Generated"
    INDIVIDUAL = "Individual"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
