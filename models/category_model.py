from databaseOLD import Base
from sqlalchemy import Column,  String , Integer

class CategoryModel(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True , autoincrement=True)
    name = Column(String, primary_key=False, unique=True, nullable=False)