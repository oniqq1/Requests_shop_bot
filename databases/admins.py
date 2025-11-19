from databases.init import *


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
