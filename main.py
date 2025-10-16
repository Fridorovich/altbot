from bot.bot import VKBot
from database.db_manager import DBManager
from config import TOKEN, GROUP_ID, DB_NAME
from infographic.CountryInfographic import CountryInfographic


def main():
    db_manager = DBManager(DB_NAME)
    db_manager.connect()

    bot = VKBot(TOKEN, GROUP_ID, db_manager)
    bot.load_country_names()
    bot.listen()

    db_manager.close()


if __name__ == '__main__':
    main()