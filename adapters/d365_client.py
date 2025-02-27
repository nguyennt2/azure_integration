# adapters/d365_client.py
import requests
from domain.inventory import InventoryItem

class D365Repository:
    def __init__(self, base_url: str, token_url: str, auth_config: dict):
        self.base_url = base_url
        self.token_url = token_url
        self.auth_config = auth_config

    def _get_token(self) -> str:
        response = requests.post(self.token_url, data=self.auth_config)
        response.raise_for_status()
        return response.json()["access_token"]

    def create_or_update(self, item: InventoryItem) -> dict:
        token = self._get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0"
        }
        payload = {
            "itemid": item.item_id,
            "availphysical": item.quantity,
            "name": item.description or item.item_id
        }
        url = f"{self.base_url}inventtables"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
