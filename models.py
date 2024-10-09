from sqlalchemy import Column, Integer, String
from database import Base

class Hash(Base):
  __tablename__ = "hash"

  id = Column(Integer, primary_key=True, index=True)
  hash = Column(String, nullable=False)
  key = Column(String, unique=True, index=True, nullable=False)
