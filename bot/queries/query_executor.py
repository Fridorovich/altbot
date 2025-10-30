
from .queries import *

class QueryExecutor:
    def __init__(self, db_controller):
        self.db_controller = db_controller
    
    def try_execute(self, query):
        if isinstance(query, TopQuery):
            # return _execute_top(query)
            return
        elif isinstance(query, StataQuery):
            return self._execute_stata(query)

    # def _execute_top(self, query):
    #     i

    def _execute_stata(self, query):
        country_id = None

        for pseudonim_part in query.country_name.deserialize():

            country_id = self.db_controller.get_latest_db().find_country(pseudonim_part)

        if not country_id: return
        
        return self.db_controller.get_latest_db().get_country_data(country_id)
