from typing import Dict, Callable, Any
from enum import Enum

from gui.client_keyboards import ClientKeyboardsPool
from gui.keyboards_enum import Keyboards
from .query_result_type import *
from .queries import *


class UserQueryStateMachine:
    def __init__(self):
        self.current_state = 'main_menu'
        self.query = None

        self.states: Dict[str, Callable[[str], str]] = {
            "main_menu": self._main_menu,
            "select_limit": self._select_limit,
            "select_category": self._top_select_category,
            "select_pop_sub": self._select_pop_sub,
            "select_country": self._select_country,
            # "converter": self._converter,
            "finish_state": self._finish_state,
        }

    def transition(self, payload):
        return self.states[self.current_state](payload)
    
    def reset(self):
        self.current_state = 'main_menu'
        self.query = None
    
    def _finish_state(self, payload):
        raise Exception("В финишное состояние попал сука")

    def _main_menu(self, payload):
        if payload not in Keyboards['MAIN_MENU'].get_buttons():
            return QueryResult(status=QueryResultStatus.IGNORED)
        
        kb = None
        msg = None

        if payload == Keyboards['MAIN_MENU'].TOP.value:
            self.current_state = 'select_limit'
            self.query = TopQuery(order=Order.DESC)
            msg = "Выберите количество государств\n"
        elif payload == Keyboards['MAIN_MENU'].ANTITOP.value:
            self.current_state = 'select_limit'
            self.query = TopQuery(order=Order.ASC)
            msg = "Выберите количество государств\n"
        elif payload == Keyboards['MAIN_MENU'].STATA.value:
            self.current_state = 'select_country'
            self.query = StataQuery()
            msg = "Выберите государство\n"
        # elif payload is Keyboards['MAIN_MENU'].CONVERTER:
        #     self.current_state = 'converter'
        #     self.query = ConvererQuery()

        return QueryResult(
            status=QueryResultStatus.IN_PROGRESS,
            keyboard=kb,
            response=msg)
    
    def _select_limit(self, payload):
        try:
            self.query.limit = NumberValue(payload)
        except:
            return QueryResult(status=QueryResultStatus.ERROR, error_message="Плохое число")
        finally:
            self.query.limit = None

        self.current_state = 'select_category'

        kb = ClientKeyboardsPool.create_main_categories_keyboard()
        msg = "Выберите категорию\n"

        return QueryResult(
            status=QueryResultStatus.IN_PROGRESS,
            keyboard=kb,
            response=msg)
    
    def _top_select_category(self, payload):
        if payload not in Keyboards['MAIN_CATEGORIES'].get_buttons():
            return QueryResult(status=QueryResultStatus.IGNORED)

        if payload == Keyboards['MAIN_CATEGORIES'].POP.value:
            self.current_state = "select_pop_sub"
            kb = ClientKeyboardsPool.create_pop_categories_keyboard()
            msg = "Выберите подкатегорию\n"
            return QueryResult(
                status=QueryResultStatus.IN_PROGRESS, 
                keyboard=kb,
                response=msg)
        
        self.current_state = "finish_state"
        return QueryResult(status=QueryResultStatus.FINISHED, query=self.query)
    
    def _select_pop_sub(self, payload):
        if payload not in Keyboards['POP_CATEGORIES'].get_buttons():
            return QueryResult(status=QueryResultStatus.IGNORED)
        self.query.subcategory = payload
        self.current_state = "finish_state"
        return QueryResult(status=QueryResultStatus.FINISHED, query=self.query)
    
    def _select_country(self, payload):
        try:
            self.query.country_name = CountryValue(payload)
        except:
            return QueryResult(status=QueryResultStatus.ERROR, error_message="Плохое название страны")
        
        self.current_state = "finish_state"
        return QueryResult(status=QueryResultStatus.FINISHED, query=self.query)