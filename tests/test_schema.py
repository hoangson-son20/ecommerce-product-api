
import pytest
from pydantic import ValidationError

from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.seller import SellerCreate, SellerUpdate


# ============================================================
# CATEGORY SCHEMA
# ============================================================

# -------------------------
# Category Create
# -------------------------

def test_category_create_valid():
    category = CategoryCreate(
        name=" Electronics ",
        description=" Electronic devices ",
    )

    assert category.name == "Electronics"
    assert category.description == "Electronic devices"


def test_category_create_without_description():
    category = CategoryCreate(name="Electronics")

    assert category.name == "Electronics"
    assert category.description is None


def test_category_create_reject_empty_name():
    with pytest.raises(ValidationError):
        CategoryCreate(name="")


def test_category_create_reject_whitespace_name():
    with pytest.raises(ValidationError):
        CategoryCreate(name="   ")


# -------------------------
# Category Update
# -------------------------

def test_category_update_partial():
    category = CategoryUpdate(name="New Electronics")

    assert category.name == "New Electronics"
    assert category.model_dump(exclude_unset=True) == {
        "name": "New Electronics"
    }


def test_category_update_strip_whitespace():
    category = CategoryUpdate(
        name="  New Electronics  ",
        description="  Updated description  ",
    )

    assert category.name == "New Electronics"
    assert category.description == "Updated description"


def test_category_update_description_can_be_null():
    category = CategoryUpdate(description=None)

    assert category.model_dump(exclude_unset=True) == {
        "description": None
    }


def test_category_update_reject_null_name():
    with pytest.raises(ValidationError):
        CategoryUpdate(name=None)


def test_category_update_reject_empty_patch():
    with pytest.raises(ValidationError):
        CategoryUpdate()


# ============================================================
# SELLER SCHEMA
# ============================================================

# -------------------------
# Seller Create
# -------------------------

def test_seller_create_valid():
    seller = SellerCreate(
        name=" Tech Store ",
        email="tech@example.com",
    )

    assert seller.name == "Tech Store"
    assert seller.email == "tech@example.com"


# -------------------------
# Seller Update
# -------------------------

def test_seller_update_partial():
    seller = SellerUpdate(name="New Tech Store")

    assert seller.name == "New Tech Store"
    assert seller.model_dump(exclude_unset=True) == {
        "name": "New Tech Store"
    }


# ============================================================
# PRODUCT SCHEMA
# ============================================================

# -------------------------
# Product Create
# -------------------------

def test_product_create_valid():
    product = ProductCreate(
        name="Wireless Mouse",
        price="25.50",
        stock_quantity=100,
        category_id=1,
        seller_id=1,
    )

    assert product.name == "Wireless Mouse"
    assert str(product.price) == "25.50"
    assert product.stock_quantity == 100
    assert product.category_id == 1
    assert product.seller_id == 1
    assert product.is_active is True


def test_product_create_strip_whitespace():
    product = ProductCreate(
        name="  Wireless Mouse  ",
        description="  Computer accessories  ",
        price="25.50",
        stock_quantity=100,
        category_id=1,
        seller_id=1,
    )

    assert product.name == "Wireless Mouse"
    assert product.description == "Computer accessories"


def test_product_create_reject_whitespace_name():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="   ",
            price="25.50",
            stock_quantity=100,
            category_id=1,
            seller_id=1,
        )


def test_product_create_reject_negative_price():
    with pytest.raises(ValidationError):
        ProductCreate(
            name="Wireless Mouse",
            price="-10",
            stock_quantity=100,
            category_id=1,
            seller_id=1,
        )


# -------------------------
# Product Update
# -------------------------

def test_product_update_partial():
    product = ProductUpdate(price="29.99")

    assert product.model_dump(exclude_unset=True) == {
        "price": product.price
    }


def test_product_update_strip_whitespace():
    product = ProductUpdate(
        name="  Gaming Mouse  ",
        description="  Updated description  ",
    )

    assert product.name == "Gaming Mouse"
    assert product.description == "Updated description"


def test_product_update_description_can_be_null():
    product = ProductUpdate(description=None)

    assert product.model_dump(exclude_unset=True) == {
        "description": None
    }


def test_product_update_reject_empty_patch():
    with pytest.raises(ValidationError):
        ProductUpdate()


def test_product_update_reject_null_price():
    with pytest.raises(ValidationError):
        ProductUpdate(price=None)
