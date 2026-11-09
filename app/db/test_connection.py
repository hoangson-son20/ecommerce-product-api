
from sqlalchemy import text

from app.db.session import SessionLocal, engine


def main() -> None:
    # Test 1: Check database connection
    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        print(f"Connected to database: {database_name}")

    # Test 2: Read data through SQLAlchemy
    with SessionLocal() as db:
        result = db.execute(
            text("""
                SELECT
                    p.id,
                    p.name AS product_name,
                    p.price,
                    c.name AS category_name,
                    s.name AS seller_name
                FROM public.products AS p
                JOIN public.categories AS c
                    ON p.category_id = c.id
                JOIN public.sellers AS s
                    ON p.seller_id = s.id
                ORDER BY p.id
            """)
        )

        rows = result.mappings().all()

        for row in rows:
            print(
                f"Product: {row['product_name']} | "
                f"Price: {row['price']} | "
                f"Category: {row['category_name']} | "
                f"Seller: {row['seller_name']}"
            )

        print(f"Total products retrieved: {len(rows)}")


if __name__ == "__main__":
    main()
