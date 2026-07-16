from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:admin123@localhost/yashindb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

try:
    conn = engine.connect()
    print("Database connected!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

from sqlalchemy import Column ,Integer ,String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)
print('Table Ready!')
