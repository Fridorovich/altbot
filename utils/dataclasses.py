from dataclasses import dataclass

@dataclass
class TopMetadata:
    category: str
    unit: str
    table: str
    column: str
    order_type: str
    limit: int