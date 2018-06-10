import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transaction_test2"

    id = Column('id', Integer, primary_key=True,autoincrement=True)
    date = Column('date', Date)
    user_0_spending = Column('user_0_spending', Integer)
    user_1_spending = Column('user_1_spending', Integer)
    restaurant = Column('restaurant', String(30))
    notes = Column('notes', String(60))
    who_paid = Column('who_paid',Integer)



connection_string: str = "mysql+pymysql://acheng:Sqlpass1!@cubesolver.ci4spsc48dhk.us-west-1.rds.amazonaws.com:3306/EasySplitter"

engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

# Session = sessionmaker(engine)
# session = Session()
# trans = Transaction()
# trans.id = 0
# trans.restaurant = "Whole Foods"
#
# session.add(trans)
# session.commit()
#
# session.close()


print("Hello World!")
