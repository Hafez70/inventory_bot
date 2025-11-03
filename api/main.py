"""
FastAPI Backend for Warehouse Management System
Provides REST API for web applications to access warehouse data.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from database import database as db

# Initialize FastAPI app
app = FastAPI(
    title="Warehouse Management API",
    description="REST API for warehouse inventory management",
    version="1.0.0"
)

# Enable CORS for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class ItemUpdate(BaseModel):
    available_count: float

class StatsResponse(BaseModel):
    total_items: int
    total_categories: int
    total_brands: int
    low_stock_items: int

# ============================================================================
# Root & Health Check
# ============================================================================

@app.get("/")
def read_root():
    """API root endpoint."""
    return {
        "message": "Warehouse Management API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "items": "/api/items",
            "categories": "/api/categories",
            "brands": "/api/brands",
            "low_stock": "/api/low-stock",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.get_connection().close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# ============================================================================
# Statistics
# ============================================================================

@app.get("/api/stats", response_model=StatsResponse)
def get_stats():
    """Get warehouse statistics."""
    try:
        items = db.get_all_items()
        categories = db.get_all_categories()
        brands = db.get_all_brands()
        low_stock = db.get_low_stock_items()
        
        return {
            "total_items": len(items),
            "total_categories": len(categories),
            "total_brands": len(brands),
            "low_stock_items": len(low_stock)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Items
# ============================================================================

@app.get("/api/items")
def get_items(
    limit: Optional[int] = Query(100, ge=1, le=1000),
    offset: Optional[int] = Query(0, ge=0)
):
    """Get all items with pagination."""
    try:
        all_items = db.get_all_items()
        total = len(all_items)
        items = all_items[offset:offset+limit]
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": [
                {
                    "id": item[0],
                    "code": item[1],
                    "custom_code": item[2],
                    "name": item[3],
                    "description": item[4],
                    "category": item[5],
                    "subcategory": item[6],
                    "brand": item[7],
                    "measure_type": item[8],
                    "available_count": item[9],
                    "video_url": item[10],
                    "created_at": item[11],
                    "updated_at": item[12]
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/items/search")
def search_items(q: str = Query(..., min_length=1)):
    """Search items by name, custom_code, or description."""
    try:
        items = db.search_items(q)
        
        return {
            "query": q,
            "total": len(items),
            "items": [
                {
                    "id": item[0],
                    "code": item[1],
                    "custom_code": item[2],
                    "name": item[3],
                    "description": item[4],
                    "category": item[5],
                    "subcategory": item[6],
                    "brand": item[7],
                    "measure_type": item[8],
                    "available_count": item[9],
                    "video_url": item[10],
                    "created_at": item[11],
                    "updated_at": item[12]
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    """Get item by ID with full details."""
    try:
        item = db.get_item_by_id(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        images = db.get_item_images(item_id)
        
        return {
            "id": item[0],
            "code": item[1],
            "custom_code": item[2],
            "name": item[3],
            "description": item[4],
            "category_id": item[5],
            "category": item[6],
            "subcategory_id": item[7],
            "subcategory": item[8],
            "brand_id": item[9],
            "brand": item[10],
            "measure_type_id": item[11],
            "measure_type": item[12],
            "available_count": item[13],
            "video_url": item[14],
            "created_at": item[15],
            "updated_at": item[16],
            "images": [
                {
                    "id": img[0],
                    "path": img[1],
                    "created_at": img[2]
                }
                for img in images
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/items/{item_id}/stock")
def update_item_stock(item_id: int, update: ItemUpdate):
    """Update item stock/available count."""
    try:
        item = db.get_item_by_id(item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Update only the available_count
        success = db.update_item(
            item_id=item_id,
            name=item[3],
            custom_code=item[2],
            category_id=item[5],
            subcategory_id=item[7],
            brand_id=item[9],
            measure_type_id=item[11],
            description=item[4],
            available_count=update.available_count,
            video_url=item[14]
        )
        
        if success:
            return {"message": "Stock updated successfully", "available_count": update.available_count}
        else:
            raise HTTPException(status_code=500, detail="Failed to update stock")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Low Stock Items
# ============================================================================

@app.get("/api/low-stock")
def get_low_stock_items():
    """Get items below low stock threshold."""
    try:
        items = db.get_low_stock_items()
        
        return {
            "total": len(items),
            "items": [
                {
                    "id": item[0],
                    "code": item[1],
                    "custom_code": item[2],
                    "name": item[3],
                    "description": item[4],
                    "category": item[5],
                    "subcategory": item[6],
                    "brand": item[7],
                    "measure_type": item[8],
                    "available_count": item[9],
                    "low_stock_threshold": item[10],
                    "created_at": item[11],
                    "updated_at": item[12]
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Categories
# ============================================================================

@app.get("/api/categories")
def get_categories():
    """Get all categories."""
    try:
        categories = db.get_all_categories()
        
        return {
            "total": len(categories),
            "categories": [
                {
                    "id": cat[0],
                    "code": cat[1],
                    "name": cat[2],
                    "created_at": cat[3]
                }
                for cat in categories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories/{category_id}/subcategories")
def get_subcategories(category_id: int):
    """Get subcategories for a specific category."""
    try:
        subcategories = db.get_subcategories_by_category(category_id)
        
        return {
            "category_id": category_id,
            "total": len(subcategories),
            "subcategories": [
                {
                    "id": sub[0],
                    "code": sub[1],
                    "name": sub[2],
                    "created_at": sub[3]
                }
                for sub in subcategories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Brands
# ============================================================================

@app.get("/api/brands")
def get_brands():
    """Get all brands."""
    try:
        brands = db.get_all_brands()
        
        return {
            "total": len(brands),
            "brands": [
                {
                    "id": brand[0],
                    "code": brand[1],
                    "name": brand[2],
                    "created_at": brand[3]
                }
                for brand in brands
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brands/{brand_id}/items")
def get_brand_items(brand_id: int):
    """Get all items for a specific brand."""
    try:
        items = db.get_items_by_brand(brand_id)
        
        return {
            "brand_id": brand_id,
            "total": len(items),
            "items": [
                {
                    "id": item[0],
                    "code": item[1],
                    "custom_code": item[2],
                    "name": item[3],
                    "available_count": item[9],
                    "measure_type": item[8]
                }
                for item in items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Measure Types
# ============================================================================

@app.get("/api/measure-types")
def get_measure_types():
    """Get all measure types."""
    try:
        measure_types = db.get_all_measure_types()
        
        return {
            "total": len(measure_types),
            "measure_types": [
                {
                    "id": mt[0],
                    "code": mt[1],
                    "name": mt[2],
                    "low_stock_threshold": mt[3],
                    "created_at": mt[4]
                }
                for mt in measure_types
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

