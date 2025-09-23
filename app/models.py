from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.sql.expression import null
from .databse import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True , nullable=False )
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now() 
    )