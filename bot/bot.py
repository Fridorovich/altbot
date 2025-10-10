import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot.message_handlers import *
from utils.dataclasses import TopMetadata

class VKBot:
    def __init__(self, token, group_id, db_manager):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.db_manager = db_manager
        self.country_names = None

    def load_country_names(self):
        if (self.country_names is not None): return

        self.country_names = self.db_manager.select_country_names()

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
            ifn = "IFNULL({}, 0)"
            self._handle_subevent_top(
                user_id, 
                TopMetadata(
                    category=category, 
                    unit=" человек", 
                    table="population", 
                    column="IFNULL(population_ss, 0) + IFNULL(population_ns, 0) + IFNULL(population_nns, 0) + IFNULL(population_nnns, 0)",
                    limit=limit,
                    order_type=order_type))
        elif category.startswith('ввп'):
            self._handle_subevent_top(
                user_id, 
                TopMetadata(
                    category=category, 
                    unit=" МЛРД ВК", 
                    table="economy", 
                    column="gdb",
                    limit=limit,
                    order_type=order_type))
        elif category.startswith('доход'):
            self._handle_subevent_top(
                user_id, 
                TopMetadata(
                    category=category, 
                    unit="%", 
                    table="economy", 
                    column="income_percent",
                    limit=limit,
                    order_type=order_type))
        elif category.startswith('расход'):
            self._handle_subevent_top(
                user_id, 
                TopMetadata(
                    category=category, 
                    unit="%", 
                    table="economy", 
                    column="expenses_percent",
                    limit=limit,
                    order_type=order_type))
        elif 'ппс' in category:
            self._handle_gdp_ppp_top(
                user_id,
                TopMetadata(
                    category=category, 
                    unit=" кун", 
                    table="economy", 
                    column="gdb",
                    limit=limit,
                    order_type=order_type))
    
    def get_country_id(self, country_name):
        for row in self.country_names:
            if row[2].lower() == country_name:
                return int(row[1])
        
        return None
    
    def _handle_subevent_top(self, user_id, top_metadata):
        top = self.db_manager.get_top_countries(top_metadata)

        message = f"{"Топ" if top_metadata.order_type == "DESC" else "Антитоп"} {top_metadata.limit} государств в категории {top_metadata.category}\n"
        i = 1

        for row in top:
            message += f"{i}. {row[0]}: {row[1]:,}{top_metadata.unit}\n"
            i += 1

        send_message(
            self.vk, 
            user_id, 
            message)
      
    def _handle_gdp_ppp_top(self, user_id, top_metadata):
        top = self.db_manager.get_gdp_ppp_top(top_metadata)

        message = f"{"Топ" if top_metadata.order_type == "DESC" else "Антитоп"} {top_metadata.limit} государств в категории {top_metadata.category}\n"
        i = 1

        for row in top:
            message += f"{i}. {row[0]}: {'очень много' if row[1] is None else round(row[1], 2)}{top_metadata.unit}\n"
            i += 1

        send_message(
            self.vk, 
            user_id, 
            message)