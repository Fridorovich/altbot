import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot.message_handlers import get_country_stata


class VKBot:
    def __init__(self, token, group_id, db_manager):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.db_manager = db_manager
        self.country_names = None

    def load_country_names(self):
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

            if message_arr[0] == 'стата' and len(message_arr) > 1:
                get_country_stata(
                    self.vk,
                    self.db_manager,
                    user_id,
                    ' '.join(message_arr[1:]),
                    self.country_names
                )