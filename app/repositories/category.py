from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.models.category import Category

class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_name(self, category_name: str) -> Category | None:
        stmt = select(Category).where(func.lower(Category.name) == func.lower(category_name))
        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_all(self, search: str | None, page: int, page_size: int, sort_order: str,) -> tuple[list[Category], int]:

        # Xây dụng các điều kiện lọc. None | 1 điều kiện | nhiều điều kiện
        conditions = []
        search = search.strip() if search else None
        if search:
            conditions.append(Category.name.ilike(f"%{search}%"))


        # Đếm tổng số lượng items sau khi lọc
        count_stmt = select(func.count()).select_from(Category).where(*conditions)

        total_items = self.db.scalar(count_stmt)


        # Xác định điều kiện sắp xếp
        if sort_order == "asc":
            order_by = [Category.name.asc(), Category.id.asc()]
        else:
            order_by = [Category.name.desc(), Category.id.asc()]

        # tính toán offset
        offset = (page - 1) * page_size

        stmt = select(Category).where(*conditions).order_by(*order_by).limit(page_size).offset(offset)

        categories = self.db.scalars(stmt).all()

        return categories, total_items


    def create(self, category_data: dict) -> Category:
        category = Category(**category_data)

        self.db.add(category)
        self.db.flush()

        return category

    def update(self, category: Category, category_data: dict) -> Category:

        if not category_data:
            return category

        allowed_fields = {"name", "description"}

        for key, value in category_data.items():
            if key in allowed_fields:
                setattr(category, key, value)

        category.updated_at = datetime.now(timezone.utc)

        self.db.flush()
        return category

    def delete(self, category: Category) -> None:

        self.db.delete(category)
        self.db.flush()