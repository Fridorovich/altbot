import glob
import os

from vk_api import VkUpload

from infographic.CountryInfographic import CountryInfographic
from utils.formatters import format_stata


def send_bad_country_error(vk, user_id, country):
    vk.messages.send(
        user_id=user_id,
        message=f"Нету такой страны {country} ты че КОК? Либо пиши ее название одним словом слитно!",
        random_id=0)


def send_country_stata(vk, db_manager, user_id, country_id, vk_session):
    main_data = db_manager.get_country_data(country_id)
    world_totals = db_manager.get_world_totals()

    country_name = main_data[0]

    data_file_path = 'infographic/Статистика_1951.txt'
    flags_folder_path = 'flags'
    output_file_path = f'infographic/infos/{country_name}_infographic.png'

    os.makedirs('infographic/infos', exist_ok=True)
    os.makedirs('flags', exist_ok=True)

    if not os.path.exists(data_file_path):
        print(f"Файл статистики не найден: {data_file_path}")

    try:
        infographic = CountryInfographic(data_file_path, flags_folder_path, country_name)
        infographic.print_parsed_data()
        if not infographic.create_infographic(output_file_path):
            vk.messages.send(
                user_id=user_id,
                message=format_stata(world_totals, main_data),
                random_id=0)

        upload = VkUpload(vk_session)
        photo = upload.photo_messages(output_file_path)

        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        vk.messages.send(
            user_id=user_id,
            message=format_stata(world_totals, main_data),
            attachment=attachment,
            random_id=0)

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Ошибка при создании инфографики: {e}")


def check_file_with_pattern(pattern):
    """
    Проверяет существование файлов по шаблону (с поддержкой *)

    Args:
        pattern (str): шаблон пути (например, '*/infographic/*.png')

    Returns:
        bool: True если найден хотя бы один файл, False если нет
    """
    return len(glob.glob(pattern)) > 0


def check_infographic_file(country_name, base_path='*/infographic/infos/'):
    """
    Проверяет существование файла инфографики для страны

    Args:
        country_name (str): название страны
        base_path (str): базовый путь к папке с инфографиками

    Returns:
        bool: True если файл существует, False если нет
    """
    pattern = base_path + country_name + '_infographic.png'
    return check_file_with_pattern(pattern)


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
