# infrastructure/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from starlette_prometheus import metrics, PrometheusMiddleware
from adapters.controllers import InventoryController
from adapters.d365_client import D365Repository
from adapters.external_client import ExternalRepository
from use_cases.sync_inventory import SyncInventoryUseCase
from domain.inventory import InventoryItem
import logging

logging.basicConfig(level=logging.INFO)

# Pydantic model for API input
class InventoryItemModel(BaseModel):
    item_id: str
    quantity: float
    description: str | None = None

    def to_domain(self):
        return InventoryItem(
            item_id=self.item_id,
            quantity=self.quantity,
            description=self.description
        )

# Configuration
D365_BASE_URL = "https://<your-d365-org>.crm.dynamics.com/api/data/v9.2/"
D365_TOKEN_URL = "https://login.microsoftonline.com/<tenant_id>/oauth2/v2.0/token"
D365_AUTH = {
    "client_id": "<your-client-id>",
    "client_secret": "<your-client-secret>",
    "grant_type": "client_credentials",
    "scope": f"{D365_BASE_URL}.default"
}
EXTERNAL_API_URL = "http://external-system.example.com/api/inventory"

# Dependency injection
d365_repo = D365Repository(D365_BASE_URL, D365_TOKEN_URL, D365_AUTH)
external_repo = ExternalRepository(EXTERNAL_API_URL)
sync_use_case = SyncInventoryUseCase(d365_repo, external_repo)
controller = InventoryController(sync_use_case)

# FastAPI app
app = FastAPI(title="D365 Integration API")
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

@app.post("/inventory/sync")
async def sync_inventory(item: InventoryItemModel):
    return await controller.sync_inventory(item.to_domain())

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
