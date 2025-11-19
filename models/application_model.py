from databaseOLD import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime , timezone

class ApplicationModel(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False , default=datetime.now(timezone.utc))