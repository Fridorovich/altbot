from dataclasses import dataclass

@dataclass
class TopMetadata:
    category: str
    unit: str
    table: str
    column: str
    order_type: str
    limit: int

    @staticmethod
    def create_pop(category, order_type, limit):
        return TopMetadata(
            category=category, 
            unit=" человек", 
            table="population", 
            column="IFNULL(population_ss, 0) + IFNULL(population_ns, 0) + IFNULL(population_nns, 0) + IFNULL(population_nnns, 0)",
            limit=limit,
            order_type=order_type)
    @staticmethod
    def create_gdp(category, order_type, limit):
        return TopMetadata(
            category=category, 
            unit=" МЛРД ВК", 
            table="economy", 
            column="gdb",
            limit=limit,
            order_type=order_type)
    @staticmethod
    def create_income(category, order_type, limit):
        return TopMetadata(
            category=category, 
            unit="%", 
            table="economy", 
            column="income_percent",
            limit=limit,
            order_type=order_type) 
    @staticmethod
    def create_expenses(category, order_type, limit):
        return TopMetadata(
            category=category, 
            unit="%", 
            table="economy", 
            column="expenses_percent",
            limit=limit,
            order_type=order_type)    
    @staticmethod
    def create_gdp_ppp(category, order_type, limit):
        return TopMetadata(
            category=category, 
            unit=" кун", 
            table="economy", 
            column="gdb",
            limit=limit,
            order_type=order_type)