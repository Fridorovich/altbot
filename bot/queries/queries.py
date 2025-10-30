from dataclasses import dataclass
from typing import Optional

from .value_objects import *
from .query_enums import Order

@dataclass
class TopQuery:
    order: Order
    limit: Optional[NumberValue] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None

@dataclass
class StataQuery:
    country_name: Optional[CountryValue] = None

@dataclass
class ConvererQuery:
    currency_lhs: Optional[CurrencyValue] = None
    currency_rhs: Optional[CurrencyValue] = None