import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot.message_handlers import *

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

            if message_arr[0] == 'стата':
                self._handle_event_country_stata(
                    user_id,
                    ' '.join(message_arr[1:])
                )
    
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
    
    def get_country_id(self, country_name):
        for row in self.country_names:
            if row[2].lower() == country_name:
                return int(row[1])
        
        return None