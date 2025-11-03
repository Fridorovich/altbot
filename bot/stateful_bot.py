import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot.message_handlers import *
from infographic.CountryInfographic import CountryInfographic
from utils.dataclasses import TopMetadata
from config import STANDARD_MESSAGE
from bot.queries.state_machine import *
from bot.queries.query_executor import *

class VKBot:
    def __init__(self, token, group_id, db_controller):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.query_executor = QueryExecutor(db_controller)
        self.message_handler = SimpleMessageHandler(self.vk)
        self.user_states = {}

    def listen(self):
        print("Бот запущен и слушает события...")
        for event in self.longpoll.listen():
            self._handle_event(event)

    def _handle_event(self, event):
        user_id = None
        parsed_payload = None

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.object.message['from_id']
            parsed_payload = event.object.message['text'].lower()

            if 'начать' in parsed_payload:
                self.message_handler.send_message(
                    user_id,
                    "Чекай кнопки",
                    ClientKeyboardsPool.create_main_menu_keyboard().get_keyboard()
                )

        elif event.type == VkBotEventType.MESSAGE_EVENT and event.object.get('payload'):
            print("А это кнопка")
            user_id = event.object.user_id
            payload = event.object.payload
            serialized_payload = payload # хзхзхзхзз
            try:
                parsed_payload = serialized_payload['button']
            except:
                print("Не распарсил кнопку")
                return

        if user_id not in self.user_states:
            self.user_states[user_id] = UserQueryStateMachine()

        transition_result = self.user_states[user_id].transition(parsed_payload)
        if transition_result.status == QueryResultStatus.FINISHED:
            send_message(self.vk, user_id, "Запрос оформлен")
            self.user_states[user_id].reset()

            query_exec_result = self.query_executor.try_execute(transition_result.query)

            if query_exec_result is None: 
                self.message_handler.send_message(user_id, "Страна хуй")
                return

            if isinstance(transition_result.query, StataQuery):
                self.message_handler.send_country_stata(
                    user_id, 
                    query_exec_result, 
                    self.query_executor.db_controller.get_latest_db().get_world_totals)

        elif transition_result.status == QueryResultStatus.IN_PROGRESS:
            send_message(
                self.vk, 
                user_id, 
                transition_result.response, 
                transition_result.keyboard.get_keyboard() if transition_result.keyboard is not None else None)

    def get_country_id(self, country_name):
        for row in self.country_pseudonims:
            if row[2].lower() == country_name:
                return int(row[1])
        
        return None