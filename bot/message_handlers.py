from utils.formatters import format_stata


def send_bad_country_error(vk, user_id, country):
    vk.messages.send(
        user_id=user_id,
        message=f"Нету такой страны {country} ты че КОК?",
        random_id=0)


def send_country_stata(vk, db_manager, user_id, country_id):
    main_data = db_manager.get_country_data(country_id)
    world_totals = db_manager.get_world_totals()

    vk.messages.send(
        user_id=user_id,
        message=format_stata(world_totals, main_data),
        random_id=0)

def send_bad_curreny_convertion_format_error(vk, user_id):
    vk.messages.send(
        user_id=user_id,
        message=f"Должен быть такой формат команды: \"перевод валюта1 в валюта2\"",
        random_id=0)
    
def send_throw_error(vk, user_id):
    vk.messages.send(
        user_id=user_id,
        message="Ты сломал бота. Доволен?\nНапиши разрабу",
        random_id=0)
    
def send_message(vk, user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0
    )

def send_guide(vk, user_id):
    GUIDE = '''
        Вот что я могу:
        "Стата Поностиум" (вставьте любое интересующее государство)

        "Топ X Категория":
        -- "население"
        -- "ввп"
        -- "доходы"
        -- "расходы"
        
        "антитоп X Категория" (Думаю тут всё очев)
    '''
    vk.messages.send(
        user_id=user_id,
        message=GUIDE,
        random_id=0
    )