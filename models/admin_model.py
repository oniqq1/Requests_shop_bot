from database import Base
from sqlalchemy import Column,  String , Integer

class AdminModel(Base):
    __tablename__ = 'admin_profile'

    id = Column(Integer, primary_key=True , autoincrement=True)
    user_id = Column(String, primary_key=False, unique=True, nullable=False)
    at_work = Column(String, nullable=False, default='no')