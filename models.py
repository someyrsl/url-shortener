from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    original_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())