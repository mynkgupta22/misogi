from fastapi import APIRouter, Depends
from typing import List, Dict
from ..utils.recommendations import RecommendationEngine
from ..models.user import User
from .auth import get_current_user
from ..main import PRODUCTS

router = APIRouter()

# Initialize recommendation engine
recommendation_engine = RecommendationEngine(PRODUCTS["products"])

@router.get("/similar/{product_id}", response_model=List[Dict])
async def get_similar_products(product_id: str, n: int = 5):
    """Get similar products based on product features"""
    return recommendation_engine.get_similar_products(product_id, n)

@router.get("/personalized", response_model=List[Dict])
async def get_personalized_recommendations(
    n: int = 5,
    current_user: User = Depends(get_current_user)
):
    """Get personalized recommendations based on user interactions"""
    return recommendation_engine.get_personalized_recommendations(
        current_user.interactions,
        n
    )

@router.get("/popular", response_model=List[Dict])
async def get_popular_products(n: int = 5):
    """Get most popular products based on ratings and review count"""
    return sorted(
        PRODUCTS["products"],
        key=lambda x: (x["rating"] * x["reviews_count"]),
        reverse=True
    )[:n] 