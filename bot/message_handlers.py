import glob
import os

from vk_api import VkUpload

from infographic.CountryInfographic import CountryInfographic
from utils.formatters import format_stata

from config import STATA_FORMAT


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

    must_created = False
    if not os.path.exists(output_file_path):
        print(f"Файл инфографики не найден: {output_file_path}")
        must_created = True

    try:
        if must_created:
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

def send_message(vk, user_id, message, keyboard = None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        keyboard=keyboard,
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

class SimpleMessageHandler:
    def __init__(self, vk):
        self.vk = vk

    def send_message(self, user_id, message, keyboard = None):
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            keyboard=keyboard,
            random_id=0
        )

    def send_country_stata(self, user_id, db_answer, get_world_totals):
        (
            country_name,          # 0 - название страны
            currency_name,         # 1 - название валюты
            currency_mass,         # 2 - масса валюты (г золота)
            gdb,                   # 3 - ВВП в млрд
            pop_ss, pop_ns, pop_nns, pop_nnns,  # 4-7 - население по группам
            growth_ss, growth_ns, growth_nns, growth_nnns,  # 8-11 - прирост по группам
            income_percent,        # 12 - доходы %
            expenses_percent,      # 13 - расходы %
            average_tax,           # 14 - средний налог
            inflation_rate,        # 15 - инфляция
            literacy               # 16 - грамотность
        ) = db_answer
        
        # Вычисляем общее население
        total_population = (pop_ss or 0) + (pop_ns or 0) + (pop_nns or 0) + (pop_nnns or 0)
        
        # Получаем мировые итоги для расчета процентов
        world_totals = get_world_totals()
        world_gdp = world_totals.world_gdp or 1  # избегаем деления на ноль
        world_pop = (world_totals.world_pop_ss or 0) + (world_totals.world_pop_ns or 0) + \
                    (world_totals.world_pop_nns or 0) + (world_totals.world_pop_nnns or 0)
        
        # Процент ВВП от мирового
        gdp_percent = (gdb / world_gdp * 100) if world_gdp else 0
        
        # Процент населения от мирового
        pop_percent = (total_population / world_pop * 100) if world_pop else 0
        
        # Форматируем население (добавляем единицы измерения)
        def format_population(pop, world_total, tag):
            return f"{pop:,} ({tag}, {format_number(pop / world_total * 100, 2)}% от населения {tag}), "
        
        # Форматируем прирост населения
        def format_growth(growth, tag):
            if growth is None:
                return "0"
            return f"{growth:+.1f}%({tag}) "
        
        # Форматируем числовые значения
        def format_number(value, decimals=1):
            if value is None:
                return "0"
            return f"{value:.{decimals}f}"
        
        stata_msg = STATA_FORMAT.format(
            country_name,                                  # 0 - название страны
            currency_name,                                 # 1 - название валюты
            format_number(currency_mass, 2),              # 2 - масса валюты
            format_number(gdb, 3),                        # 3 - ВВП в млрд
            format_number(gdp_percent, 2),                # 4 - % ВВП от мирового
            # format_population(pop_ss or 0) if pop_ss else "",               # 5 - население SS
            # format_population(pop_ns or 0) if pop_ns else "",  # 6 - население NS
            # format_population(pop_nns or 0) if pop_nns else "", # 7 - население NNS
            # format_population(pop_nnns or 0) if pop_nnns else "", # 8 - население NNNS
            "" if pop_ss is None else format_population(pop_ss, world_totals.world_pop_ss, 'СС'),
            "" if pop_ns is None else format_population(pop_ns, world_totals.world_pop_ns, 'НС'),
            "" if pop_nns is None else format_population(pop_nns, world_totals.world_pop_nns, 'ННС'),
            "" if pop_nnns is None else format_population(pop_nnns, world_totals.world_pop_nnns, 'НННС'),
            format_number(pop_percent, 2),                # 9 - % населения от мирового
            # format_growth(growth_ss),                     # 10 - прирост SS
            # f", {format_growth(growth_ns)}" if growth_ns else "", # 11 - прирост NS
            # f", {format_growth(growth_nns)}" if growth_nns else "", # 12 - прирост NNS
            # f", {format_growth(growth_nnns)}" if growth_nnns else "", # 13 - прирост NNNS
            "" if growth_ss is None else format_growth(growth_ss, "СС"),
            "" if growth_ns is None else format_growth(growth_ns, "НС"),
            "" if growth_nns is None else format_growth(growth_nns, "ННС"),
            "" if growth_nnns is None else format_growth(growth_nnns, "НННС"),
            format_number(income_percent, 1),             # 14 - доходы %
            format_number(expenses_percent, 1),           # 15 - расходы %
            format_number(average_tax, 1),                # 16 - средний налог
            format_number(inflation_rate, 1),             # 17 - инфляция
            format_number(literacy, 1),                   # 18 - грамотность
            format_number(income_percent - expenses_percent, 1)  # 19 - темпы роста ВВП (недоступно в текущих данных)
        )

        self.vk.messages.send(
            user_id=user_id,
            message=stata_msg,
            random_id=0
        )