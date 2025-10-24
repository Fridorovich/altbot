from typing import List
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from gui.keyboards_enum import Keyboards
 
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

    return keyboards

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

    def create_n_country_choice_keyboard(self, countries: dict[int, List[str, bool]], page, page_limit = 8):
        n_country_choice = VkKeyboard(inline=True)

        for id in range(page_limit * page + 1, page_limit * (page + 1) + 1):
            n_country_choice.add_callback_button(
                countries[id][0], 
                payload={
                    "button": "country", 
                    "type": "button_click", 
                    "kind": "dynamic", 
                    "already_selected": "False" if countries[id][1] else "True",
                    "id": f"{id}"
                }
            )
            n_country_choice.add_line()

        slider_payload = lambda str: (str, {"button": "page_change", "type": "button_click", "kind": "dynamic", "details": str})
            
        for s in ["<<", "<", ">", ">>"]:
            label, payload = slider_payload(s)
            n_country_choice.add_callback_button(label, payload=payload)
        
    def create_start_keyboard(self):
        return self.static_keyboards[Keyboards.START]
    def create_main_menu_keyboard(self):
        return self.static_keyboards[Keyboards.MAIN_MENU]
    def create_main_categories_keyboard(self):
        return self.static_keyboards[Keyboards.MAIN_CATEGORIES]
    def create_pop_categories_keyboard(self):
        return self.static_keyboards[Keyboards.POP_CATEGORIES]
    def create_percent_or_unit_keyboard(self):
        return self.static_keyboards[Keyboards.PERCENT_OR_UNIT_QUALIFIER]
