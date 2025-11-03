from enum import Enum

class Category(Enum):
    POP = "pop"
    GDP = "gdp"
    INCOME = "income"
    EXPENSE = "expense"
    PPP = "ppp"

class PopSubcategory(Enum):
    TOTAL = "total_pop"
    SS = "pop_ss"
    NS = "pop_ns"
    NNS = "pop_nns"
    NNNS = "pop_nnns"

class Qualifier(Enum):
    PERCENT = "percent"
    UNIT = "unit"

class Order(Enum):
    ASC = "asc"
    DESC = "desc"