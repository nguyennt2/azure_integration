# use_cases/sync_inventory.py
from domain.inventory import InventoryItem
from prometheus_client import Histogram

SYNC_LATENCY = Histogram("inventory_sync_latency_seconds", "Latency of inventory sync operations")

class SyncInventoryUseCase:
    def __init__(self, d365_repository, external_repository):
        self.d365_repository = d365_repository
        self.external_repository = external_repository

    def execute(self, item: InventoryItem) -> dict:
        item.validate()
        with SYNC_LATENCY.time():
            d365_result = self.d365_repository.create_or_update(item)
            self.external_repository.update(item)
        return {"message": "Inventory synced", "d365_record": d365_result}
