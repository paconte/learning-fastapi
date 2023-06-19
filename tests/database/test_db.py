import pytest

from app.database import db
from app.models.products import Product, ProductIn

product_a = ProductIn(
    name="Test Product",
    category="Test Category",
    score="9",
)
product_b = ProductIn(
    name="Test Product 2",
    category="Test Category 2",
    score="50",
)
products = [product_a, product_b]


@pytest.mark.asyncio
async def test_save():
    for product in products:
        new_product = await db.PRODUCT_DB.save(product)
        assert isinstance(new_product, Product)
        assert new_product.id == products.index(product)
        assert new_product.name == product.name
        assert new_product.category == product.category
        assert new_product.score == product.score


@pytest.mark.asyncio
async def test_get():
    # get product
    for id, product in enumerate(products):
        new_product = await db.PRODUCT_DB.get(products.index(product))
        assert isinstance(new_product, Product)
        assert new_product.id == id
        assert new_product.name == product.name
        assert new_product.category == product.category
        assert new_product.score == product.score

    # get product with invalid ID
    product = await db.PRODUCT_DB.get(len(products))
    assert product is None


@pytest.mark.asyncio
async def test_get_all():
    # get all products
    products = await db.PRODUCT_DB.get_all()
    assert isinstance(products, list)
    assert len(products) == 2
    for id, product in enumerate(products):
        assert isinstance(product, Product)
        assert product.id == id
        assert product.name == products[product.id].name
        assert product.category == products[product.id].category
        assert product.score == products[product.id].score
        assert product.reviews == products[product.id].reviews


@pytest.mark.asyncio
async def test_update():
    # update product
    updated_product = await db.PRODUCT_DB.update(
        0,
        ProductIn(
            name="Updated Product",
            category="Updated Category",
            score=19,
            reviews=[],
        ),
    )
    assert isinstance(updated_product, Product)
    assert updated_product.id == 0
    assert updated_product.name == "Updated Product"
    assert updated_product.category == "Updated Category"
    assert updated_product.score == "19"
    assert updated_product.reviews == []

    # update product with invalid ID
    with pytest.raises(ValueError) as exc_info:
        updated_product = await db.PRODUCT_DB.update(
            0,
            Product(
                id=1,
                name="Updated Product",
                category="Updated Category",
                score=19,
                reviews=[],
            ),
        )
    assert str(exc_info.value) == "ID in data does not match key ID"


@pytest.mark.asyncio
async def test_delete():
    # delete products
    products = await db.PRODUCT_DB.get_all()
    for product in products:
        deleted_product = await db.PRODUCT_DB.delete(product.id)
        assert isinstance(deleted_product, Product)
        assert deleted_product.id == product.id
        assert deleted_product.name == product.name
        assert deleted_product.category == product.category
        assert deleted_product.score == product.score
        assert deleted_product.reviews == product.reviews

    # delete product with invalid ID
    deleted_product = await db.PRODUCT_DB.delete(0)
    assert deleted_product is None
