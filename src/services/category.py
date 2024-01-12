# Core imports
from core.db import session, Transactional, standalone_session
from sqlalchemy import select, and_, any_
from sqlalchemy.orm import selectinload, joinedload
from core.helpers.redis import redis
# App imports
from models import Category, Attribute, AttributeValue, CategoryAttribute
from errors import CategoryNotFound

# Python imports
from collections import defaultdict
from typing import List


class CategoryServices:
    def __init__(self) -> None:
        ...

    async def get_category_attributes(self, category_id: int) -> Category:
        query = (
            select(Category)
            .options(joinedload(Category.attributes).joinedload(Attribute.values))
            .where(Category.id == category_id)
        )
        category: Category = (await session.execute(query)).scalars().first()
        if not Category:
            raise CategoryNotFound
        
        return category

    async def get_category_tree(self) -> List[Category]:
        all_categories = (
            await session.execute(
                select(Category)
            )
        ).unique().scalars().all()
    
        root_categories = []
        for category in all_categories:
            if not category.parent_id:
                root_categories.append(category.serialize())

        def __category_tree_builder(parent_category):
            """ Return a category with subs """
            parent_category['sub_categories'] = []
            for category in all_categories:
                if category.parent_id == parent_category['id']:
                    sub = __category_tree_builder(category.serialize())
                    parent_category['sub_categories'].append(sub)

            return parent_category

        for root_category in root_categories:
            root_category = __category_tree_builder(root_category)

        return root_categories
