from enum import Enum, auto
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# class KeyboardStates(Enum):
#     START = auto()
#     MAIN_MENU = auto()
#     MAIN_CATEGORIES = auto()
#     POP_CATEGORIES = auto()
#     PERCENT_OR_UNIT_QUALIFIER = auto()
#     N_COUNTRY_CHOICE = auto()
#     DEAD_END = auto()

# class Keyboards(Enum):
#     TOP = "top"
#     ANTITOP = "antitop"
#     STATA = "stata"
#     SLICE = "slice"
#     CONVERTER = "converter"
#     POP = "pop"
#     GDP = "gdp"
#     INCOME = "income"
#     EXPENSE = "expense"
#     PPP = "ppp"
#     PERCENT = "percent"
#     UNIT = "unit"
#     TOTAL_POP = "total pop"
#     POP_SS = "pop ss"
#     POP_NS = "pop ns"
#     POP_NNS = "pop nns"
#     POP_NNNS = "pop nnns"
#     BACK = "back"
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
    
    # class AMOUNTS_TO_CHOOSE(BaseKeyboard, Enum):
    #     FIVE = "5"
    #     TEN = "10"
    #     TWENTY = "20"
    #     THIRTY = "30"
    #     FIFTY = "50"
    #     SEVENTY = "70"
 
event_type = {"type": "button_click", "kind": "static"}

def setup_start_keyboard():
    start = VkKeyboard(inline=False)
    start.add_button('Старт', color=VkKeyboardColor.PRIMARY)
    
    return start

def setup_main_menu_keyboard():
    main_menu = VkKeyboard(inline=False)
    main_menu.add_callback_button('Топ', color=VkKeyboardColor.POSITIVE, payload={"button": Keyboards.MAIN_MENU.TOP} | event_type)
    main_menu.add_callback_button('Антитоп', color=VkKeyboardColor.NEGATIVE, payload={"button": Keyboards.MAIN_MENU.ANTITOP} | event_type)
    main_menu.add_line()
    main_menu.add_callback_button('Стата', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards.MAIN_MENU.STATA} | event_type)
    main_menu.add_callback_button('Срез', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards.MAIN_MENU.SLICE} | event_type)
    main_menu.add_line()
    main_menu.add_callback_button('Перевод', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards.MAIN_MENU.CONVERTER} | event_type)

    return main_menu

def setup_main_categories_keyboard():
    categories = VkKeyboard(inline=True)
    categories.add_callback_button('Население', payload={"button": Keyboards.MAIN_CATEGORIES.POP} | event_type)
    categories.add_callback_button('ВВП', payload={"button": Keyboards.MAIN_CATEGORIES.GDP} | event_type)
    categories.add_line()
    categories.add_callback_button('Доходы', payload={"button": Keyboards.MAIN_CATEGORIES.INCOME} | event_type)
    categories.add_callback_button('Расходы', payload={"button": Keyboards.MAIN_CATEGORIES.EXPENSE} | event_type)
    categories.add_line()
    categories.add_callback_button('ППС', payload={"button": Keyboards.MAIN_CATEGORIES.PPP} | event_type)

    return categories

def setup_pop_categories_keyboard():
    pop_categories = VkKeyboard(inline=True)
    pop_categories.add_callback_button('Полное население', payload={"button": Keyboards.POP_CATEGORIES.TOTAL_POP} | event_type)
    pop_categories.add_line()
    pop_categories.add_callback_button('Население в СС', payload={"button": Keyboards.POP_CATEGORIES.SS} | event_type)
    pop_categories.add_callback_button('Население в НС', payload={"button": Keyboards.POP_CATEGORIES.NS} | event_type)
    pop_categories.add_line()
    pop_categories.add_callback_button('Население в ННС', payload={"button": Keyboards.POP_CATEGORIES.NNS} | event_type)
    pop_categories.add_callback_button('Население в НННС', payload={"button": Keyboards.POP_CATEGORIES.NNNS} | event_type)

def setup_percent_or_unit_qualifier_keyboard():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button('В процентах', payload={"button": Keyboards.PERCENT_OR_UNIT_QUALIFIER.PERCENT} | event_type)
    keyboard.add_line()
    keyboard.add_callback_button('В млрд ВК', payload={"button": Keyboards.PERCENT_OR_UNIT_QUALIFIER.UNIT} | event_type)

    return keyboard

def setup_static_keyboards():
    keyboards = {}
    
    keyboards[Keyboards.START] = setup_start_keyboard()
    keyboards[Keyboards.MAIN_MENU] = setup_main_menu_keyboard()
    keyboards[Keyboards.MAIN_CATEGORIES] = setup_main_categories_keyboard()
    keyboards[Keyboards.POP_CATEGORIES] = setup_pop_categories_keyboard()
    keyboards[Keyboards.PERCENT_OR_UNIT_QUALIFIER] = setup_percent_or_unit_qualifier_keyboard()
    # keyboards[Keyboards.AMOUNTS_TO_CHOOSE] = setup_amounts_to_choose_keyboard()

    return keyboards

def generate_n_country_choice(countries: dict[int, str], page, page_limit = 8):
    n_country_choice = VkKeyboard(inline=True)

    for id in range(page_limit * page + 1, page_limit * (page + 1) + 1):
        n_country_choice.add_callback_button(
            countries[id], 
            payload={
                "button": f"{id};{countries[id]}", 
                "type": "button_click", 
                "kind": "dynamic", 
                "details": None
            }
        )
        n_country_choice.add_line()
        
    n_country_choice.add_callback_button(
        "<<", 
        payload={
            "button": f"{id};{countries[id]}", 
            "type": "button_click", 
            "kind": "dynamic", 
            "details": "<<"
        }
    )

    n_country_choice.add_callback_button(
        "<", 
        payload={
            "button": f"{id};{countries[id]}", 
            "type": "button_click", 
            "kind": "dynamic", 
            "details": "<"
        }
    )

    '''Вот примерно на этом шаге я понял, что всё это ебучая хуйня'''
    

class ClientKeyboardsPool:
    static_keyboards = setup_static_keyboards()

    def _try_parse_event_payload(self, payload):
        import json

        # если payload по какой-то причине уже словарь
        if isinstance(payload, dict):
            return payload

        # Если JSON-стринга
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                # Вот такие пироги
                return {"type": "not_button"}
        
    def _parse_static_keyboard_layout(self, button_type):
        if Keyboards.START.is_keyboard_button(button_type):

            return self.static_keyboards[Keyboards.MAIN_MENU]
        
        elif Keyboards.MAIN_MENU.is_keyboard_button(button_type):

            if button_type in [Keyboards.MAIN_MENU.TOP, Keyboards.MAIN_MENU.ANTITOP]:
                return self.static_keyboards[Keyboards.MAIN_CATEGORIES]
            elif button_type is Keyboards.MAIN_MENU.STATA:
                return lambda countries: generate_n_country_choice(countries, 0)
        elif Keyboards.MAIN_CATEGORIES.is_keyboard_button(button_type):
            return
        elif Keyboards.POP_CATEGORIES.is_keyboard_button(button_type):
            return
        elif Keyboards.PERCENT_OR_UNIT_QUALIFIER.is_keyboard_button(button_type):
            return
        else: raise Exception("Не смог распарсить статическую клаву, не тот ээээ лэйаут???")

    '''Парсит нажатие кнопки и возвращает следующий лэйаут (теоретически)'''
    def parse_button_click_event(self, payload: str):
        dict = self._try_parse_event_payload(payload)

        if dict["type"] != event_type["type"]:
            return

        button = dict["button"]
        kind = dict["kind"]

        if kind == "static":
            return self._parse_static_keyboard_layout(button)
        elif kind == "dynamic":
            return self._parse_dynamic_keyboard_layout(button, dict["details"])
        else: raise Exception("Это точно кнопка, но она ни static, ни dynamic")
