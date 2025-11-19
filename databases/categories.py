from databases.init import *

def create_category(name: str):
    from models.category_model import CategoryModel
    category = CategoryModel(name=name)
    session.add(category)
    session.commit()
    return True

def get_all_categories():
    from models.category_model import CategoryModel
    categories = session.query(CategoryModel).all()
    return categories

def delete_category(category_id: str):
    from models.category_model import CategoryModel
    category = session.query(CategoryModel).filter_by(id=category_id).first()
    if category:
        session.delete(category)
        session.commit()
        return True
    return False

