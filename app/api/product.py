from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.database.db import PRODUCT_DB
from app.models.products import Product, ProductIn
from app.security.authenticator import authenticate

product_router = APIRouter()


# Products
@product_router.get(
    "/products", response_model=List[Product], summary="Get all products"
)
async def get_products() -> List[Product]:
    """
    Retrieve a list of all products.

    Returns:
        List[Product]: The list of products.
    """
    return await PRODUCT_DB.get_all()


@product_router.get(
    "/products/{id}",
    response_model=Product,
    summary="Get a specific product by ID",
)
async def get_product(id: int) -> Product:
    """
    Retrieve a specific product by its ID.

    Args:
        id (int): The ID of the product.

    Returns:
        Product: The product information.

    Raises:
        HTTPException: If the product with the supplied ID does not exist.
    """
    product = await PRODUCT_DB.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with supplied ID does not exist",
        )
    return product


@product_router.post(
    "/products",
    dependencies=[Depends(authenticate)],
    summary="Create a new product",
)
async def create_product(
    body: ProductIn,
) -> dict:
    """
    Create a new product.

    Args:
        body (ProductIn): The product information.

    Returns:
        dict: A message indicating the successful creation of the product.

    Dependencies:
        - Depends(authenticate): Requires authentication.
    """
    await PRODUCT_DB.save(body)
    return {"message": "Product created successfully"}


@product_router.delete(
    "/products/{id}",
    dependencies=[Depends(authenticate)],
    summary="Delete a product by ID",
)
async def delete_product(id: int) -> dict:
    """
    Delete a specific product by its ID.

    Args:
        id (int): The ID of the product.

    Returns:
        dict: A message indicating the successful deletion of the product.

    Dependencies:
        - Depends(authenticate): Requires authentication.

    Raises:
        HTTPException: If the product with the supplied ID does not exist.
    """
    product = await PRODUCT_DB.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    await PRODUCT_DB.delete(id)

    return {"message": "Product deleted successfully."}
