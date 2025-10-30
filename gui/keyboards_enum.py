from enum import Enum

class KeyboardEnum(Enum):
    """Base Enum class with keyboard functionality"""
    
    @classmethod
    def is_keyboard_button(cls, button):
        return button in cls.get_buttons()
    
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
        for member in cls:
            if member.value == button:
                return member
        raise ValueError(f"Button '{button}' not found")
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

# Keyboard enum classes
class START(KeyboardEnum):
    START = "start"

class MAIN_MENU(KeyboardEnum):
    TOP = "top"
    ANTITOP = "antitop" 
    STATA = "stata"
    SLICE = "slice"
    CONVERTER = "converter"

class MAIN_CATEGORIES(KeyboardEnum):
    POP = "pop"
    GDP = "gdp"
    INCOME = "income"
    EXPENSE = "expense"
    PPP = "ppp"

class POP_CATEGORIES(KeyboardEnum):
    TOTAL_POP = "total pop"
    POP_SS = "pop ss"
    POP_NS = "pop ns"
    POP_NNS = "pop nns"
    POP_NNNS = "pop nnns"

class PERCENT_OR_UNIT_QUALIFIER(KeyboardEnum):
    PERCENT = "percent"
    UNIT = "unit"

class BACK(KeyboardEnum):
    BACK = "back"

# Simple container - no need for complex class
Keyboards = {
    'START': START,
    'MAIN_MENU': MAIN_MENU,
    'MAIN_CATEGORIES': MAIN_CATEGORIES,
    'POP_CATEGORIES': POP_CATEGORIES,
    'PERCENT_OR_UNIT_QUALIFIER': PERCENT_OR_UNIT_QUALIFIER,
    'BACK': BACK
}