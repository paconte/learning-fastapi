from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from app.database.db import PRODUCT_DB
from app.models.products import Product
from app.models.reviews import Review, ReviewIn
from app.security.authenticator import authenticate

review_router = APIRouter()


async def _get_product(product_id: int) -> Product:
    product = await PRODUCT_DB.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


# Product Reviews
@review_router.get(
    "/products/{product_id}/reviews", response_model=List[Review]
)
async def get_product_reviews(product_id: int) -> List[Review]:
    # Retrieve all reviews for a specific product
    product = await _get_product(product_id)
    return product.reviews


@review_router.post("/products/{product_id}/reviews")
async def create_product_review(
    product_id: int, body: ReviewIn, user: EmailStr = Depends(authenticate)
) -> dict:
    # Create a new review for a specific product
    product = await _get_product(product_id)
    review = Review(**body.dict(), user=user)
    product.reviews.append(review)
    review = await PRODUCT_DB.update(product.id, product)
    return {"message": "Review created successfully"}
