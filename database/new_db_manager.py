from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from functools import lru_cache
from typing import List, Tuple, Any, Optional
from .models import Base, CountryName, CountryPseudonym, Currency, Population, Economy, Stat
from utils.dataclasses import TopMetadata

class DBManager:
    def __init__(self, db_name: str):
        self.engine = create_engine(f'sqlite:///{db_name}', echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @lru_cache(maxsize=1)
    def get_country_pseudonims(self) -> List[Tuple]:
        """Кэшируем псевдонимы стран - статичные данные"""
        with self.get_session() as session:
            return [(row.country_id, row.pseudonim.lower()) for row in session.query(CountryPseudonym).all()]

    @lru_cache(maxsize=1)
    def get_country_names(self) -> List[Tuple]:
        """Кэшируем названия стран - статичные данные"""
        with self.get_session() as session:
            return [(row.country_id, row.name.lower()) for row in session.query(CountryName).all()]

    @lru_cache(maxsize=1)
    def get_currencies(self) -> List[Tuple]:
        """Кэшируем валюты - статичные данные"""
        with self.get_session() as session:
            return [
                (row.currency_id, row.name, row.mass, row.inflation_rate)
                for row in session.query(Currency).all()
            ]

    def get_country_data(self, country_id: int) -> Optional[Tuple]:
        with self.get_session() as session:
            result = (
                session.query(
                    CountryName.name,
                    Currency.name.label('currency'),
                    Currency.mass.label('currency_mass'),
                    Economy.gdb,
                    Population.population_ss,
                    Population.population_ns,
                    Population.population_nns,
                    Population.population_nnns,
                    Population.growth_rate_ss,
                    Population.growth_rate_ns,
                    Population.growth_rate_nns,
                    Population.growth_rate_nnns,
                    Economy.income_percent,
                    Economy.expenses_percent,
                    Stat.average_tax,
                    Currency.inflation_rate,
                    Stat.literacy
                )
                .join(CountryName, CountryName.country_id == Stat.country_id)
                .join(Currency, Currency.currency_id == Stat.currency_id)
                .join(Population, Population.country_id == Stat.country_id)
                .join(Economy, Economy.country_id == Stat.country_id)
                .filter(CountryName.country_id == country_id)
                .first()
            )

            print(result)
            return result

    def get_world_totals(self) -> Tuple:
        with self.get_session() as session:
            result = session.query(
                func.sum(Economy.gdb).label('world_gdp'),
                func.sum(Population.population_ss).label('world_pop_ss'),
                func.sum(Population.population_ns).label('world_pop_ns'),
                func.sum(Population.population_nns).label('world_pop_nns'),
                func.sum(Population.population_nnns).label('world_pop_nnns')
            ).join(Population, Population.country_id == Economy.country_id).first()
            return result

    def get_top_countries(self, metadata: TopMetadata):
        with self.get_session() as session:
            table_map = {
                'economy': Economy,
                'population': Population,
                'stats': Stat,
                'currencies': Currency,
            }
            table_class = table_map.get(metadata.table)
            if not table_class:
                raise ValueError(f"Unknown table: {metadata.table}")

            column_attr = getattr(table_class, metadata.column, None)
            if not column_attr:
                raise AttributeError(f"Table {metadata.table} has no column '{metadata.column}'")

            query = (
                session.query(CountryName.name, column_attr.label('value'))
                .join(table_class, CountryName.country_id == table_class.country_id)
                .order_by(column_attr.desc() if metadata.order_type == 'DESC' else column_attr.asc())
                .limit(metadata.limit)
            )
            return query.all()

    def get_gdp_ppp_top(self, metadata: TopMetadata):
        with self.get_session() as session:
            total_pop = (
                func.coalesce(Population.population_ss, 0) +
                func.coalesce(Population.population_ns, 0) +
                func.coalesce(Population.population_nns, 0) +
                func.coalesce(Population.population_nnns, 0)
            )

            gdp_ppp = (Economy.gdb / total_pop) * 1_000_000_000

            query = (
                session.query(CountryName.name, gdp_ppp.label('gdp_ppp'))
                .join(Economy, CountryName.country_id == Economy.country_id)
                .join(Population, CountryName.country_id == Population.country_id)
                .order_by(gdp_ppp.desc() if metadata.order_type == 'DESC' else gdp_ppp.asc())
                .limit(metadata.limit)
            )
            return query.all()
        
    def find_country(self, user_input: str):
        for country_id, pseudonim in self.get_country_pseudonims():
            if user_input in pseudonim:
                return country_id
            
        return None