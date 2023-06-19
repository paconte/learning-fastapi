import asyncio
from threading import Lock
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.db import PRODUCT_DB, REVIEW_DB
from app.models.reviews import Review, ReviewIn
from app.security.authenticator import authenticate

review_router = APIRouter()


# Product Reviews
@review_router.get(
    "/products/{product_id}/reviews", response_model=List[Review]
)
async def get_product_reviews(product_id: int) -> List[Review]:
    # Retrieve all reviews for a specific product
    lock = Lock()
    with lock:
        product = await PRODUCT_DB.get(product_id)
        queries = []
        for review_id in product.review_ids:
            queries.append(REVIEW_DB.get(review_id))
        result = await asyncio.gather(*queries)
        print(result)
        return result


@review_router.get("/products/{product_id}/reviews/{review_id}")
async def get_product_review(product_id: int, review_id: int):
    # Retrieve a specific review for a specific product
    lock = Lock()
    with lock:
        review = await REVIEW_DB.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        product = await PRODUCT_DB.get(product_id)
        if review.id not in product.review_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product not found",
            )
        return review


@review_router.post(
    "/products/{product_id}/reviews", dependencies=[Depends(authenticate)]
)
async def create_product_review(product_id: int, body: ReviewIn):
    # Create a new review for a specific product
    lock = Lock()
    with lock:
        product = await PRODUCT_DB.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        review = await REVIEW_DB.save(body)
        product.review_ids.append(review.id)
        await PRODUCT_DB.update(product_id, product)
        return {"message": "Review created successfully"}


@review_router.put("/products/{product_id}/reviews/{review_id}")
async def update_product_review(
    product_id: int, review_id: int, body: ReviewIn
) -> Review:
    # Update a specific review for a specific product
    lock = Lock()
    with lock:
        review = await REVIEW_DB.get(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        product = await PRODUCT_DB.get(product_id)
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
        return await REVIEW_DB.update(review_id, body)


@review_router.delete(
    "/products/{product_id}/reviews/{review_id}",
    dependencies=[Depends(authenticate)],
)
async def delete_product_review(product_id: int, review_id: int):
    # Delete a specific review for a specific product
    lock = Lock()
    with lock:
        product = await PRODUCT_DB.get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        review = await REVIEW_DB.get(review_id)
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
        await REVIEW_DB.delete(review_id)
        product.review_ids.remove(review.id)
        return {"message": "Review deleted successfully"}
