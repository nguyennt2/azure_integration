# adapters/controllers.py
from fastapi import HTTPException
from domain.inventory import InventoryItem
from use_cases.sync_inventory import SyncInventoryUseCase
import logging

logger = logging.getLogger(__name__)

class InventoryController:
    def __init__(self, sync_use_case: SyncInventoryUseCase):
        self.sync_use_case = sync_use_case

    async def sync_inventory(self, item: InventoryItem):
        try:
            logger.info(f"Processing sync for item: {item.item_id}")
            result = self.sync_use_case.execute(item)
            logger.info(f"Successfully synced item: {item.item_id}")
            return result
        except Exception as e:
            logger.error(f"Error syncing item {item.item_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
