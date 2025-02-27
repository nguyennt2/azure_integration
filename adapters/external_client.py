# adapters/external_client.py
from domain.inventory import InventoryItem

class ExternalRepository:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def update(self, item: InventoryItem):
        print(f"Updated external system: {item.item_id}, qty: {item.quantity}")
