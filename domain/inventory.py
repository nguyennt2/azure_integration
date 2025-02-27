# domain/inventory.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class InventoryItem:
    item_id: str
    quantity: float
    description: Optional[str] = None

    def validate(self):
        if not self.item_id or self.quantity < 0:
            raise ValueError("Invalid inventory item: item_id must be non-empty and quantity non-negative")
