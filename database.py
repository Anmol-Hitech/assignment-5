from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL=DATABASE_URL
engine=create_engine(DATABASE_URL)
Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()