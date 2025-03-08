# Azure integration

Integrate Dynamic 365 and RestAPI to update

# Tech Stack

- FastAPI
- Dynamic 365 Azure
- Clean Architect
- REST API
- Prometheus

## Installation Dependency

`pip install -r requirements.txt`

## Data flow

External system → REST API (Middleware to monitor) → D365 for updates;

### Prometheus

Middleware to monitor REST API

#### Set up

- Download : `brew install prometheus`

- Configuration : `prometheus.yml`

- Start run : `./prometheus --config.file=prometheus.yml`

### Start and Test App

`python main.py`

Docs: `http://localhost:8000/docs`

`curl -X POST "http://localhost:8000/inventory/sync" -H "Content-Type: application/json" -d '{"item_id": "ITEM001", "quantity": 100.5, "description": "Test Item"}'`
