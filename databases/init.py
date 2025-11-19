from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base

from config import OWNER_ID

engine = create_engine('sqlite:///databases.db')
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