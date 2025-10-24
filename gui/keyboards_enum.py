from enum import Enum
from abc import ABC

class BaseKeyboard(ABC):
    """Base class with common keyboard functionality"""
    
    def is_keyboard_button(self, button):
        return button in self.get_buttons()
    
    @classmethod
    def get_buttons(cls):
        return [member.value for member in cls]
    
    @classmethod
    def get_button_names(cls):
        return [member.name for member in cls]
    
    @classmethod
    def validate_button(cls, button):
        if button not in cls.get_buttons():
            raise ValueError(f"Invalid button '{button}'. Valid options: {cls.get_buttons()}")
        return cls(button)

class Keyboards(Enum):
    class START(BaseKeyboard, Enum):
        START = "start"

    class MAIN_MENU(BaseKeyboard, Enum):
        TOP = "top"
        ANTITOP = "antitop"
        STATA = "stata"
        SLICE = "slice"
        CONVERTER = "converter"

    class MAIN_CATEGORIES(BaseKeyboard, Enum):
        POP = "pop"
        GDP = "gdp"
        INCOME = "income"
        EXPENSE = "expense"
        PPP = "ppp"

    class POP_CATEGORIES(BaseKeyboard, Enum):
        TOTAL_POP = "total pop"
        POP_SS = "pop ss"
        POP_NS = "pop ns"
        POP_NNS = "pop nns"
        POP_NNNS = "pop nnns"

    class PERCENT_OR_UNIT_QUALIFIER(BaseKeyboard, Enum):
        PERCENT = "percent"
        UNIT = "unit"