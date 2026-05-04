from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models.Base_Model import Base

engine = create_engine('sqlite:///POO\Guilda.db')
Session = sessionmaker(bind=engine)

def CriarTabelas():
    Base.metadata.create_all(engine)
