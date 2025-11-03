from typing import List
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from gui.keyboards_enum import Keyboards
 
event_type = {"type": "button_click", "kind": "static"}

# def setup_start_keyboard():
#     start = VkKeyboard(inline=False)
#     start.add_button('Старт', color=VkKeyboardColor.PRIMARY)
    
#     return start

def setup_main_menu_keyboard():
    main_menu = VkKeyboard(inline=False)
    main_menu.add_callback_button('Топ', color=VkKeyboardColor.POSITIVE, payload={"button": Keyboards['MAIN_MENU'].TOP.value} | event_type)
    main_menu.add_callback_button('Антитоп', color=VkKeyboardColor.NEGATIVE, payload={"button": Keyboards['MAIN_MENU'].ANTITOP.value} | event_type)
    main_menu.add_line()
    main_menu.add_callback_button('Стата', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards['MAIN_MENU'].STATA.value} | event_type)
    main_menu.add_callback_button('Срез', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards['MAIN_MENU'].SLICE.value} | event_type)
    main_menu.add_line()
    main_menu.add_callback_button('Перевод', color=VkKeyboardColor.SECONDARY, payload={"button": Keyboards['MAIN_MENU'].CONVERTER.value} | event_type)

    return main_menu

def setup_main_categories_keyboard():
    categories = VkKeyboard(inline=True)
    categories.add_callback_button('Население', payload={"button": Keyboards['MAIN_CATEGORIES'].POP.value} | event_type)
    categories.add_callback_button('ВВП', payload={"button": Keyboards['MAIN_CATEGORIES'].GDP.value} | event_type)
    categories.add_line()
    categories.add_callback_button('Доходы', payload={"button": Keyboards['MAIN_CATEGORIES'].INCOME.value} | event_type)
    categories.add_callback_button('Расходы', payload={"button": Keyboards['MAIN_CATEGORIES'].EXPENSE.value} | event_type)
    categories.add_line()
    categories.add_callback_button('ППС', payload={"button": Keyboards['MAIN_CATEGORIES'].PPP.value} | event_type)

    return categories

def setup_pop_categories_keyboard():
    pop_categories = VkKeyboard(inline=True)
    pop_categories.add_callback_button('Полное население', payload={"button": Keyboards['POP_CATEGORIES'].TOTAL_POP.value} | event_type)
    pop_categories.add_line()
    pop_categories.add_callback_button('Население в СС', payload={"button": Keyboards['POP_CATEGORIES'].POP_SS.value} | event_type)
    pop_categories.add_callback_button('Население в НС', payload={"button": Keyboards['POP_CATEGORIES'].POP_NS.value} | event_type)
    pop_categories.add_line()
    pop_categories.add_callback_button('Население в ННС', payload={"button": Keyboards['POP_CATEGORIES'].POP_NNS.value} | event_type)
    pop_categories.add_callback_button('Население в НННС', payload={"button": Keyboards['POP_CATEGORIES'].POP_NNNS.value} | event_type)
    
    return pop_categories

def setup_percent_or_unit_qualifier_keyboard():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button('В процентах', payload={"button": Keyboards['PERCENT_OR_UNIT_QUALIFIER'].PERCENT.value} | event_type)
    keyboard.add_line()
    keyboard.add_callback_button('В млрд ВК', payload={"button": Keyboards['PERCENT_OR_UNIT_QUALIFIER'].UNIT.value} | event_type)

    return keyboard

def setup_back_keyboard():
    back = VkKeyboard(inline=True)
    back.add_callback_button("Назад", payload={"button": Keyboards.BACK.BACK.value} | event_type)
    
    return back

def setup_static_keyboards():
    keyboards = {}
    
    # keyboards[Keyboards.START] = setup_start_keyboard()
    keyboards[Keyboards['MAIN_MENU']] = setup_main_menu_keyboard()
    keyboards[Keyboards['MAIN_CATEGORIES']] = setup_main_categories_keyboard()
    keyboards[Keyboards['POP_CATEGORIES']] = setup_pop_categories_keyboard()
    keyboards[Keyboards['PERCENT_OR_UNIT_QUALIFIER']] = setup_percent_or_unit_qualifier_keyboard()
    # keyboards[Keyboards.BACK] = setup_back_keyboard()

    return keyboards

class ClientKeyboardsPool:
    static_keyboards = setup_static_keyboards()

    # def create_n_country_choice_keyboard(self, countries: dict[int, List[str, bool]], page, page_limit=8):
    #     n_country_choice = VkKeyboard(inline=True)

    #     for id in range(page_limit * page + 1, page_limit * (page + 1) + 1):
    #         n_country_choice.add_callback_button(
    #             countries[id][0], 
    #             payload={
    #                 "button": "country", 
    #                 "type": "button_click", 
    #                 "kind": "dynamic", 
    #                 "already_selected": "False" if countries[id][1] else "True",
    #                 "id": f"{id}"
    #             }
    #         )
    #         n_country_choice.add_line()

    #     slider_payload = lambda s: (s, {"button": "page_change", "type": "button_click", "kind": "dynamic", "details": s})
            
    #     for s in ["<<", "<", ">", ">>"]:
    #         label, payload = slider_payload(s)
    #         n_country_choice.add_callback_button(label, payload=payload)
        
    #     return n_country_choice

    @staticmethod
    def create_start_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards.START]
    
    @staticmethod
    def create_main_menu_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards['MAIN_MENU']]
    
    @staticmethod
    def create_main_categories_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards['MAIN_CATEGORIES']]
    
    @staticmethod
    def create_pop_categories_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards['POP_CATEGORIES']]
    
    @staticmethod
    def create_percent_or_unit_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards['PERCENT_OR_UNIT_QUALIFIER']]
    
    @staticmethod
    def create_back_keyboard():
        return ClientKeyboardsPool.static_keyboards[Keyboards.BACK]