# API Module

REST API backend for warehouse management system built with FastAPI.

## Files

- `main.py` - FastAPI application with all endpoints
- `__init__.py` - Module initialization
- `requirements.txt` - API-specific dependencies

## Running the API

### Local Development (Windows):
```cmd
start_api.bat
```

### Linux/cPanel:
```bash
./start_api.sh
```

Or manually:
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### General
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/stats` - Warehouse statistics

### Items
- `GET /api/items` - Get all items (with pagination)
- `GET /api/items/search?q={query}` - Search items
- `GET /api/items/{id}` - Get item details
- `PATCH /api/items/{id}/stock` - Update item stock

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}/subcategories` - Get subcategories

### Brands
- `GET /api/brands` - Get all brands
- `GET /api/brands/{id}/items` - Get brand items

### Measure Types
- `GET /api/measure-types` - Get all measurement units

### Low Stock
- `GET /api/low-stock` - Get low stock items

## Example Requests

### Get All Items
```bash
curl http://localhost:8000/api/items
```

### Search Items
```bash
curl "http://localhost:8000/api/items/search?q=laptop"
```

### Get Item Details
```bash
curl http://localhost:8000/api/items/1
```

### Update Item Stock
```bash
curl -X PATCH http://localhost:8000/api/items/1/stock \
  -H "Content-Type: application/json" \
  -d '{"available_count": 50}'
```

## Response Format

All responses are in JSON format:

```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "Product Name",
      "code": "ITM123456",
      "custom_code": "CUSTOM-001",
      "available_count": 25,
      "measure_type": "عدد",
      ...
    }
  ]
}
```

## CORS

CORS is enabled for all origins by default. Update in production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Your frontend domain
    ...
)
```

## Authentication

Currently, the API is open. To add authentication:
1. Add JWT token middleware
2. Add API key validation
3. Use FastAPI dependencies for auth

## Using with Web App

This API is designed to be consumed by:
- Angular applications
- React applications  
- Vue applications
- Any HTTP client

Example (JavaScript/Fetch):
```javascript
// Get all items
fetch('http://localhost:8000/api/items')
  .then(res => res.json())
  .then(data => console.log(data));

// Search items
fetch('http://localhost:8000/api/items/search?q=laptop')
  .then(res => res.json())
  .then(data => console.log(data));
```

## Dependencies

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

See `/api/requirements.txt` or project `/requirements.txt`.

## Deployment

### cPanel Setup Python App

1. Create new Python app in cPanel
2. Point to this directory
3. Set startup file to `main.py`
4. Set application entry point to `app`
5. Map to subdomain (e.g., `api.yourdomain.com`)

See `/DEPLOYMENT.md` for full guide.

