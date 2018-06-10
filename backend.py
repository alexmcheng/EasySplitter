import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# define our table columns
class Transaction(Base):
    __tablename__ = "transaction_test2"

    id = Column('id', Integer, primary_key=True,autoincrement=True)
    date = Column('date', Date)
    user_0_spending = Column('user_0_spending', Integer)
    user_1_spending = Column('user_1_spending', Integer)
    restaurant = Column('restaurant', String(30))
    notes = Column('notes', String(60))
    who_paid = Column('who_paid',Integer)


# MySQL database login details, username, password, addresss
with open('password.config', 'r') as myfile:
    database_login = myfile.read()

connection_string: str = 'mysql+pymysql://' + database_login

engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(engine)
session = Session()
trans = Transaction()
trans.id = 0
trans.restaurant = "Whole Foods"

session.add(trans)
session.commit()

session.close()


print("Hello World!")
