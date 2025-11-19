from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base

from config import OWNER_ID

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

def init_db():
    from models.application_model import ApplicationModel
    from models.category_model import CategoryModel
    from models.admin_model import AdminModel
    Base.metadata.create_all(engine)

def add_owner_to_db():
    from models.admin_model import AdminModel
    owner = session.query(AdminModel).filter_by(user_id=OWNER_ID).first()
    if not owner:
        owner = AdminModel(user_id=OWNER_ID)
        session.add(owner)
        session.commit()

def create_application(Application: Base):
    from models.application_model import ApplicationModel
    App = ApplicationModel(
        user_id=Application.user_id,
        name=Application.name,
        category=Application.category,
        phone=Application.phone,
        comment=Application.comment,
    )
    session.add(App)
    session.commit()
    return App.id

def get_applications_by_user(user_id):
    from models.application_model import ApplicationModel
    applications = session.query(ApplicationModel).filter_by(user_id=user_id).all()
    return applications

def get_all_applications_pending():
    from models.application_model import ApplicationModel
    applications = session.query(ApplicationModel).filter_by(status='pending').all()
    return applications


def delete_application(application_id):
    from models.application_model import ApplicationModel
    application = session.query(ApplicationModel).get(application_id)
    if application:
        session.delete(application)
        session.commit()
        return True
    return False





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



def create_admin(user_id: int):
    from models.admin_model import AdminModel
    admin = AdminModel(user_id=user_id)
    session.add(admin)
    session.commit()

def is_admin(user_id: int) -> bool:
    from models.admin_model import AdminModel
    admin = session.query(AdminModel).filter_by(user_id=user_id).first()
    return admin is not None

def delete_admin(user_id: int) -> bool:
    from models.admin_model import AdminModel
    admin = session.query(AdminModel).filter_by(user_id=user_id).first()
    session.delete(admin)
    session.commit()
