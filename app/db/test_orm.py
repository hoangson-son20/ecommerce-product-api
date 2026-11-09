from sqlalchemy import select

from app.models import Product
from app.db.session import SessionLocal



def main() -> None:
    with SessionLocal() as db:
        statement = (
            select(Product)
            .order_by(Product.id)
        )

        products = db.scalars(statement).all()

        for product in products:
            print(
                f"ID: {product.id} | "
                f"Name: {product.name} | "
                f"Price: {product.price} | "
                f"Category: {product.category.name} | "
                f"Seller: {product.seller.name}"
            )

        print(f"Total products: {len(products)}")


if __name__ == "__main__":
    main()