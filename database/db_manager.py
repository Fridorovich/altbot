import sqlite3

from utils.dataclasses import TopMetadata

class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def select_country_names(self):
        self.cursor.execute('SELECT * FROM country_pseudonims;')
        return self.cursor.fetchall()

    def get_country_data(self, country_id):
        self.cursor.execute('''
        SELECT 
            cn.name AS name,
            cur.name AS currency,
            cur.mass AS currency_mass,
            e.gdb AS gdp,
            pop.population_ss,
            pop.population_ns,
            pop.population_nns,
            pop.population_nnns,
            pop.growth_rate_ss,
            pop.growth_rate_ns,
            pop.growth_rate_nns,
            pop.growth_rate_nnns,
            e.income_percent,
            e.expenses_percent,
            s.average_tax,
            cur.inflation_rate,
            s.literacy
        FROM stats s
        JOIN country_names cn ON cn.country_id = s.country_id
        JOIN currencies cur ON cur.currency_id = s.currency_id
        JOIN population pop ON pop.country_id = s.country_id
        JOIN economy e ON e.country_id = s.country_id
        WHERE cn.country_id = ?
        ''', (country_id,))
        return self.cursor.fetchone()

    def get_world_totals(self):
        self.cursor.execute('''
        SELECT 
            SUM(e.gdb) as world_gdp,
            SUM(pop.population_ss) as world_pop_ss,
            SUM(pop.population_ns) as world_pop_ns,
            SUM(pop.population_nns) as world_pop_nns,
            SUM(pop.population_nnns) as world_pop_nnns
        FROM economy e
        JOIN population pop ON pop.country_id = e.country_id
        ''')
        return self.cursor.fetchone()
    
    def get_top_countries(self, metadata):
        query = '''
        SELECT country_names.name AS name, ({}) AS value FROM {}
        JOIN country_names ON country_names.country_id = {}.country_id
        ORDER BY value {}
        LIMIT ?;
        '''.format(metadata.column, metadata.table, metadata.table, metadata.order_type,)

        self.cursor.execute(query, (metadata.limit,))

        return self.cursor.fetchall()
    
    def get_gdp_ppp_top(self, metadata):
        query = '''
            SELECT country_names.name AS name, 
            (economy.gdb / (IFNULL(population_ss, 0) + IFNULL(population_ns, 0) + IFNULL(population_nns, 0) + IFNULL(population_nnns, 0)) * 1000000000) AS gdp_ppp
            FROM country_names
            JOIN economy ON country_names.country_id = economy.country_id
            JOIN population ON country_names.country_id = population.country_id
            ORDER BY gdp_ppp {}
            LIMIT ?
        '''.format(metadata.order_type)

        self.cursor.execute(query, (metadata.limit,))

        return self.cursor.fetchall()