# from bot.stateful_bot import VKBot
from bot.stateful_bot import VKBot
# from database.new_db_manager import DBManager
from database.db_controller import DBController
from config import TOKEN, GROUP_ID, DB_PATH
from infographic.CountryInfographic import CountryInfographic


def main():
    db_controller = DBController(DB_PATH)

    bot = VKBot(TOKEN, GROUP_ID, db_controller)
    bot.listen()


if __name__ == '__main__':
    main()