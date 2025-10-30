from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CountryName(Base):
    __tablename__ = 'country_names'

    country_id = Column(Integer, primary_key=True)
    name = Column(String)

class CountryPseudonym(Base):
    __tablename__ = 'country_pseudonims'  # да, опечатка в названии таблицы, но оставим как есть

    country_id = Column(Integer, primary_key=True)
    pseudonim = Column(String)

class Currency(Base):
    __tablename__ = 'currencies'

    currency_id = Column(Integer, primary_key=True)
    name = Column(String)
    mass = Column(Float)
    inflation_rate = Column(Float)

class Population(Base):
    __tablename__ = 'population'

    country_id = Column(Integer, primary_key=True)
    population_ss = Column(Float)
    population_ns = Column(Float)
    population_nns = Column(Float)
    population_nnns = Column(Float)
    growth_rate_ss = Column(Float)
    growth_rate_ns = Column(Float)
    growth_rate_nns = Column(Float)
    growth_rate_nnns = Column(Float)

class Economy(Base):
    __tablename__ = 'economy'

    country_id = Column(Integer, primary_key=True)
    gdb = Column(Float)  # предположительно — ВВП (GDP)
    income_percent = Column(Float)
    expenses_percent = Column(Float)

class Stat(Base):
    __tablename__ = 'stats'

    country_id = Column(Integer, primary_key=True)
    currency_id = Column(Integer)
    average_tax = Column(Float)
    literacy = Column(Float)