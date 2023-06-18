import asyncio
from threading import Lock
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.product import product_db
from app.database import Database
from app.models.reviews import Review, ReviewIn

review_router = APIRouter()
review_db = Database(Review)


# Product Reviews
@review_router.get(
    "/products/{product_id}/reviews", response_model=List[Review]
)
async def get_product_reviews(product_id: int) -> List[Review]:
    # Retrieve all reviews for a specific product
    lock = Lock()
    with lock:
        product = await product_db.get(product_id)
        queries = []
        for review_id in product.review_ids:
            queries.append(review_db.get(review_id))
        result = await asyncio.gather(*queries)
        print(result)
        return result


@review_router.get("/products/{product_id}/reviews/{review_id}")
async def get_product_review(product_id: int, review_id: int):
    # Retrieve a specific review for a specific product
    lock = Lock()
    with lock:
        review = await review_db.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        product = await product_db.get(product_id)
        if review.id not in product.review_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product not found",
            )
        return review


@review_router.post("/products/{product_id}/reviews")
async def create_product_review(product_id: int, body: ReviewIn):
    # Create a new review for a specific product
    lock = Lock()
    with lock:
        product = await product_db.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        review = await review_db.save(body)
        product.review_ids.append(review.id)
        await product_db.update(product_id, product)
        return {"message": "Review created successfully"}


@review_router.put("/products/{product_id}/reviews/{review_id}")
async def update_product_review(
    product_id: int, review_id: int, body: ReviewIn
) -> Review:
    # Update a specific review for a specific product
    lock = Lock()
    with lock:
        review = await review_db.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        product = await product_db.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if review.id not in product.review_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Review with supplied ID exists, but is not "
                    "associated with the product with supplied ID"
                ),
            )
        return await review_db.update(review_id, body)


@review_router.delete("/products/{product_id}/reviews/{review_id}")
async def delete_product_review(product_id: int, review_id: int):
    # Delete a specific review for a specific product
    lock = Lock()
    with lock:
        product = await product_db.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        review = await review_db.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        if review.id not in product.review_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Review with supplied ID exists, but is not "
                    "associated with the product with supplied ID"
                ),
            )
        await review_db.delete(review_id)
        product.review_ids.remove(review.id)
        return {"message": "Review deleted successfully"}
