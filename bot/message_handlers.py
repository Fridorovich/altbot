from utils.formatters import format_stata


def send_bad_country_error(vk, user_id, country):
    vk.messages.send(
        user_id=user_id,
        message=f"Нету такой страны {country} ты че КОК?",
        random_id=0)


def get_country_stata(vk, db_manager, user_id, country, country_names):
    country_id = -1

    for row in country_names:
        if row[2].lower() == country:
            country_id = int(row[1])
            break

    if country_id == -1:
        send_bad_country_error(vk, user_id, country)
        return

    main_data = db_manager.get_country_data(country_id)
    world_totals = db_manager.get_world_totals()

    vk.messages.send(
        user_id=user_id,
        message=format_stata(world_totals, main_data),
        random_id=0)