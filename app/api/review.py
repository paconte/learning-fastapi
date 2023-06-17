from typing import Any, Dict

from fastapi import APIRouter

from app.database import Database

review_router = APIRouter()
review_collection: Dict[int, Any] = dict()
review_db = Database(review_collection)


# Product Reviews
@review_router.get("/products/{product_id}/reviews")
async def get_product_reviews(product_id: int):
    # Retrieve all reviews for a specific product
    pass


@review_router.post("/products/{product_id}/reviews")
async def create_product_review(product_id: int):
    # Create a new review for a specific product
    pass


@review_router.get("/products/{product_id}/reviews/{review_id}")
async def get_product_review(product_id: int, review_id: int):
    # Retrieve a specific review for a specific product
    pass


@review_router.put("/products/{product_id}/reviews/{review_id}")
async def update_product_review(product_id: int, review_id: int):
    # Update a specific review for a specific product
    pass


@review_router.delete("/products/{product_id}/reviews/{review_id}")
async def delete_product_review(product_id: int, review_id: int):
    # Delete a specific review for a specific product
    pass
