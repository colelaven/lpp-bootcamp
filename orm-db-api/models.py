from sqlalchemy import Column, create_engine, DateTime, Integer, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Bug(Base):
    __tablename__ = "bugs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    isClosed = Column(Boolean)
    createdAt = Column(DateTime, server_default=func.now())
    def toDict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'isClosed' : self.isClosed,
            'createdAt' : self.createdAt
        }
    def __repr__(self):
        return f"Bug(id={self.id!r}, name={self.name!r}, isClosed={self.isClosed!r}, createdAt={self.createdAt!r})"

# run to init db
# engine = create_engine("sqlite:///./bugs.db")
# Base.metadata.create_all(engine)
