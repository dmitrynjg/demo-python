from src.app.product.entity.product import Product
from src.app.product.entity.product_edit_history import ProductEditHistory, EditAction
from src.core.database import db
from src.lib.Paginator import Paginator
from ..user.entity.user import User
from src.lib.ServerException import ServerException
from sqlalchemy import desc, asc, not_
import re;

class ProductService:
    def get_all_products(self, page=1, limit=10, sort=[], filter={}):
        query = Product.query.where(Product.is_delete == False)
    
        if filter:
            field = getattr(Product, filter['field'])
            print(field)
            if filter['op'] == 'like':
                query = query.filter(field.like(f'%{filter["value"]}%'))
            elif filter['op'] == 'equal':
                query = query.filter(field == filter['value'])
            elif filter['op'] == 'not':
                query = query.filter(not_(field == filter['value']))
        
        if sort is not None and len(sort) == 2:
            if sort[0] == "desc":
                query = query.order_by(desc(getattr(Product, sort[1])))
            if sort[0] == "asc":
                query = query.order_by(asc(getattr(Product, sort[1])))
      
        paginator = Paginator(query, page, limit)
        paginator.apply_pagination()
        products_with_pagination = paginator.get_results()
        products_with_pagination.update(
            {
                "result": [
                    product.to_dict() for product in products_with_pagination["result"]
                ]
            }
        )
        return products_with_pagination

    def create_product(self, data, user_id):
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        product_edit_history = ProductEditHistory(
            product_id=product.id, user_id=user_id, action=EditAction.CREATE
        )
        db.session.add(product_edit_history)
        db.session.commit()
        return {"message": "Товар успешно создан", "product": product.to_dict()}

    def get_product(self, id):
        try:
            product = Product.query.where(
                Product.id == id, Product.is_delete == False
            ).one()
            if product:
                return product.to_dict()
        except:
            raise ServerException("Товар не найден")

    def update_product(self, id, data, user_id):
        product = Product.query.get(id)

        if product:
            if product.is_delete:
                raise Exception("Товар не найден")
            for key, value in data.items():
                setattr(product, key, value)
            product_edit_history = ProductEditHistory(
                product_id=product.id, user_id=user_id, action=EditAction.UPDATE
            )
            db.session.add(product_edit_history)
            db.session.commit()

            return {"message": "Товар успешно обновлен", "product": product.to_dict()}

        raise ServerException("Товар не найден")

    def delete_product(self, id, user_id):
        product = Product.query.get(id)

        if product:
            setattr(product, "is_delete", True)
            product_edit_history = ProductEditHistory(
                product_id=product.id, user_id=user_id, action=EditAction.DELETE
            )
            db.session.add(product_edit_history)
            db.session.commit()
            return {"message": "Товар успешно удален"}

        raise ServerException("Товар не найден")

    def get_history_edit(self, page, limit):
        paginator = Paginator(
            db.session.query(ProductEditHistory, Product.name, User.login)
            .join(Product)
            .join(User)
            .order_by(desc(ProductEditHistory.created_at)),
            page,
            limit,
        )
        paginator.apply_pagination()
        data = paginator.get_results()

        data.update(
            {
                "result": [
                    {
                        "id": edit[0].id,
                        "createdAt": edit[0].created_at.isoformat(),
                        "action": edit[0].action.value,
                        "productName": edit[1],
                        "userLogin": edit[2],
                    }
                    for edit in data["result"]
                ],
            }
        )
        return data
