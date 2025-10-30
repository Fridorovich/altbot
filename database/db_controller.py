import os

from .new_db_manager import DBManager

class DBController:
    def __init__(self, db_directory):
        self.db_directory = db_directory
        self.stat_dbs = {}
        self.latest_db = None
        self._load_databases()
    
    def _load_databases(self):
        """Загружает все БД и определяет актуальную"""
        years = []
        
        for item in os.listdir(self.db_directory):
            full_path = os.path.join(self.db_directory, item)
            if os.path.isfile(full_path) and item.endswith('.db'):
                # Извлекаем год из названия файла
                try:
                    year = int(item.replace('.db', '').split('-')[-1])
                    self.stat_dbs[year] = DBManager(full_path)
                    years.append(year)
                except ValueError:
                    continue
        
        if years:
            latest_year = max(years)
            self.latest_db = self.stat_dbs[latest_year]
    
    def get_latest_db(self):
        return self.latest_db