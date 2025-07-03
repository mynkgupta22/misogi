from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from ..models.user import User
from .auth import get_current_user
from ..main import PRODUCTS
from ..utils.auth import get_users, save_users

router = APIRouter()

@router.get("/", response_model=List[Dict])
async def get_products(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
):
    """Get products with optional filtering"""
    products = PRODUCTS["products"]
    
    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    if subcategory:
        products = [p for p in products if p["subcategory"].lower() == subcategory.lower()]
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]
    if min_rating is not None:
        products = [p for p in products if p["rating"] >= min_rating]
    
    return products

@router.get("/categories")
async def get_categories():
    """Get unique categories and their subcategories"""
    categories = {}
    for product in PRODUCTS["products"]:
        if product["category"] not in categories:
            categories[product["category"]] = set()
        categories[product["category"]].add(product["subcategory"])
    
    # Convert sets to lists for JSON serialization
    return {k: list(v) for k, v in categories.items()}

@router.post("/interaction/{product_id}")
async def track_interaction(
    product_id: str,
    interaction_type: str,
    current_user: User = Depends(get_current_user)
):
    """Track user interaction with a product"""
    if interaction_type not in ["viewed", "liked", "purchased"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid interaction type"
        )
    
    # Verify product exists
    if not any(p["id"] == product_id for p in PRODUCTS["products"]):
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    # Update user interactions
    users_data = get_users()
    user_data = users_data["users"][current_user.id]
    
    if product_id not in user_data["interactions"][interaction_type]:
        user_data["interactions"][interaction_type].append(product_id)
        save_users(users_data)
    
    return {"status": "success"} 