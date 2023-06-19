from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.db import PRODUCT_DB
from app.models.products import Product, ProductIn
from app.security.authenticator import authenticate

product_router = APIRouter()


# Products
@product_router.get("/products", response_model=List[Product])
async def get_products() -> List[Product]:
    # Retrieve a list of all products
    return await PRODUCT_DB.get_all()


@product_router.get("/products/{id}", response_model=Product)
async def get_product(id: int) -> Product:
    # Retrieve a specific product by its ID
    product = await PRODUCT_DB.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with supplied ID does not exist",
        )
    return product


@product_router.post("/products", dependencies=[Depends(authenticate)])
async def create_product(
    body: ProductIn,
) -> dict:
    # Create a new product
    await PRODUCT_DB.save(body)
    return {"message": "Product created successfully"}


@product_router.put("/products/{id}", response_model=Product)
async def update_product(id: int, body: ProductIn) -> Product:
    # Update a specific product by its ID
    updated_product = await PRODUCT_DB.update(id, body)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with supplied ID does not exist",
        )
    return updated_product


@product_router.delete("/products/{id}", dependencies=[Depends(authenticate)])
async def delete_product(id: int) -> dict:
    # Delete a specific product by its ID
    product = await PRODUCT_DB.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    await PRODUCT_DB.delete(id)

    return {"message": "Product deleted successfully."}
