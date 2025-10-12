import vk_api
import Levenshtein
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot.message_handlers import *
from utils.dataclasses import TopMetadata

class VKBot:
    def __init__(self, token, group_id, db_manager):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.db_manager = db_manager
        self.country_pseudonims = self.db_manager.select_country_pseudonims()
        self.country_names = None
        self.country_count = None
        self.currencies = self.db_manager.get_currencies()

    def load_country_names(self):
        if (self.country_names is not None): return

        self.country_names = self.db_manager.select_country_names()


    def get_country_count(self):
        if (self.country_count is not None): return self.country_count

        self.load_country_names()

        self.country_count = len(self.country_names)

        return self.country_count

    def listen(self):
        print("Бот запущен и слушает события...")
        for event in self.longpoll.listen():
            self._handle_event(event)

    def _handle_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.object.message['from_id']
            message_text = event.object.message['text']
            message_arr = message_text.lower().split()

            print(f"from: {user_id}, message: {message_arr}")

            if len(message_arr) == 0: return

            if message_arr[0] == 'начать':
                send_guide(self.vk, user_id)
            elif len(message_arr) > 1 and message_arr[0] == 'стата':
                self._handle_event_country_stata(
                    user_id,
                    ' '.join(message_arr[1:])
                )
            elif len(message_arr) > 3 and message_arr[0].startswith('перев'):
                self._handle_event_currency_convertion(
                    user_id,
                    message_arr[1:]
                )
            elif len(message_arr) > 1 and message_arr[0] == 'топ':
                if message_arr[1].isdecimal() and len(message_arr) > 2:
                    self._handle_event_top(
                        user_id, 
                        ' '.join(message_arr[2:]), 
                        "DESC",
                        int(message_arr[1])
                    )
                else:
                    self._handle_event_top(user_id, message_arr[1], "DESC")
            elif len(message_arr) > 1 and message_arr[0] == 'антитоп':
                if message_arr[1].isdecimal() and len(message_arr) > 2:
                    self._handle_event_top(
                        user_id, 
                        ' '.join(message_arr[2:]), 
                        "ASC",
                        int(message_arr[1])
                    )
                else:
                    self._handle_event_top(user_id, message_arr[1], "ASC")
                
                
    def _handle_event_currency_convertion(self, user_id, message_arr):
        delim_idx = 0
        currency_lhs = None
        currency_rhs = None

        try:
            delim_idx = message_arr.index('в')
            currency_lhs = ' '.join(message_arr[:delim_idx])
            currency_rhs = ' '.join(message_arr[delim_idx + 1:])
        except:
            send_bad_curreny_convertion_format_error(self.vk, user_id)
            return
        
        currency_idx_lhs = None
        currency_idx_rhs = None

        for currency in self.currencies:
            if currency_lhs in currency[1].lower():
                currency_idx_lhs = currency[0] - 1
                break

        for currency in self.currencies:
            if currency_rhs in currency[1].lower():
                currency_idx_rhs = currency[0] - 1
                break

        if currency_idx_lhs is None:
            send_message(self.vk, user_id, f"Не смог распознать валюту: {currency_lhs}")
            return
        if currency_idx_rhs is None:
            send_message(self.vk, user_id, f"Не смог распознать валюту: {currency_rhs}")
            return

        lhs_to_rhs = self.currencies[currency_idx_lhs][2] / self.currencies[currency_idx_rhs][2]
        rhs_to_lhs = self.currencies[currency_idx_rhs][2] / self.currencies[currency_idx_lhs][2]

        message = f"Курс {self.currencies[currency_idx_lhs][1]} - {self.currencies[currency_idx_rhs][1]}\n"
        message += "1 {} = {} {}\n".format(
            self.currencies[currency_idx_lhs][1],
            round(lhs_to_rhs, 2) if lhs_to_rhs >= 1 else round(lhs_to_rhs, 4),
            self.currencies[currency_idx_rhs][1])
        message += "1 {} = {} {}\n".format(
            self.currencies[currency_idx_rhs][1],
            round(rhs_to_lhs, 2) if rhs_to_lhs >= 1 else round(rhs_to_lhs, 4),
            self.currencies[currency_idx_lhs][1])

        send_message(
            self.vk,
            user_id,
            message)


    
    def _handle_event_country_stata(self, user_id, country_name):
        country_id = self.get_country_id(country_name)

        if (country_id is None):
            send_bad_country_error(self.vk, user_id, country_name)
            return
        
        send_country_stata(
            self.vk, 
            self.db_manager, 
            user_id, 
            country_id)

        return 
    
    def _handle_event_top(self, user_id, category, order_type, limit = 10):
        if limit <= 0:
            send_message(self.vk, user_id, 'а слабо нормальные числа вводить?')
            return

        if category.startswith('населени'):
            self._handle_subevent_top(
                user_id, 
                TopMetadata.create_pop(category, order_type, limit))
        elif category.startswith('ввп'):
            self._handle_subevent_top(
                user_id, 
                TopMetadata.create_gdp(category, order_type, limit))
        elif category.startswith('доход'):
            # self._handle_subevent_top(
            self._handle_gdp_diff_top(
                user_id, 
                TopMetadata.create_income(category, order_type, limit))
        elif category.startswith('расход'):
            # self._handle_subevent_top(
            self._handle_gdp_diff_top(
                user_id, 
                TopMetadata.create_expenses(category, order_type, limit))
        elif 'ппс' in category:
            self._handle_gdp_ppp_top(
                user_id,
                TopMetadata.create_gdp_ppp(category, order_type, limit))
    
    def get_country_id(self, country_name):
        for row in self.country_pseudonims:
            if row[2].lower() == country_name:
                return int(row[1])
        
        return None
    
    def _handle_subevent_top(self, user_id, top_metadata):
        top = self.db_manager.get_top_countries(top_metadata)

        message = f"{"Топ" if top_metadata.order_type == "DESC" else "Антитоп"} {top_metadata.limit} государств в категории {top_metadata.category}\n"
        i = 1 if top_metadata.order_type == "DESC" else self.get_country_count()

        for row in top:
            message += f"{i}. {row[0]}: {row[1]:,}{top_metadata.unit}\n"
            i += 1 if top_metadata.order_type == "DESC" else -1

        send_message(
            self.vk, 
            user_id, 
            message)
      
    def _handle_gdp_ppp_top(self, user_id, top_metadata):
        top = self.db_manager.get_gdp_ppp_top(top_metadata)

        message = f"{"Топ" if top_metadata.order_type == "DESC" else "Антитоп"} {top_metadata.limit} государств в категории {top_metadata.category}\n"
        i = 1 if top_metadata.order_type == "DESC" else self.get_country_count()

        for row in top:
            message += f"{i}. {row[0]}: {'очень много' if row[1] is None else round(row[1], 2)}{top_metadata.unit}\n"
            i += 1 if top_metadata.order_type == "DESC" else -1

        send_message(
            self.vk, 
            user_id, 
            message)
        
    def _handle_gdp_diff_top(self, user_id, top_metadata):
        percent_top = self.db_manager.get_top_countries(top_metadata)
        unit_top = self.db_manager.get_top_countries(
            TopMetadata.create_gdp(
                category=top_metadata.category, 
                order_type=top_metadata.order_type, 
                limit=top_metadata.limit))
        
        message = f"{"Топ" if top_metadata.order_type == "DESC" else "Антитоп"} {top_metadata.limit} государств в категории {top_metadata.category}\n"
        i = 1 if top_metadata.order_type == "DESC" else self.get_country_count()

        top = list(zip(percent_top, unit_top))

        for row in top:
            message += "{i}. {name}: {percent}% от ВВП или же {quantity:,} МЛРД ВК\n".format(
                i=i,
                name=row[0][0],
                percent='очень много' if row[0][1] is None else round(row[0][1], 2),
                quantity=round(row[1][1] * row[0][1] / 100, 4)
            )
            i += 1 if top_metadata.order_type == "DESC" else -1

        send_message(
            self.vk, 
            user_id, 
            message)