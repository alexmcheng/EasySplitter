from flask import Flask

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

Base = declarative_base()

# define our table columns
class Transaction(Base):
    __tablename__ = 'user_spending'

    id = Column('transaction_id', Integer, primary_key=True,autoincrement=True)
    spender_id = Column('spender_id', Integer) # either 0 or 1
    amt_spent = Column('amt_spent', Integer)
    detail_id = Column('detail_id', Integer, ForeignKey('transaction_details.detail_id'))


class TransactionDetails(Base):
    __tablename__ = 'transaction_details'

    id = Column('detail_id', Integer, primary_key=True, autoincrement=True)
    date = Column('date', Date)
    restaurant = Column('restaurant', String(30))
    notes = Column('notes', String(60))
    who_paid = Column('who_paid', Integer)

# MySQL database login details, username, password, addresss
with open('password.config', 'r') as myfile:
    database_login = myfile.read()

connection_string: str = 'mysql+pymysql://' + database_login

engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(engine)
session = Session()

detail = TransactionDetails()
detail.restaurant = 'Seto'
detail.date = '2018-06-11'
detail.notes = 'delicious'
detail.who_paid = 0
session.add(detail)

trans0 = Transaction()
trans0.spender_id = 0
trans0.amt_spent = 1800
trans0.detail_id = detail.id

trans1 = Transaction()
trans1.spender_id = 1
trans1.amt_spent = 900
trans1.detail_id = detail.id


session.add(trans0)
session.add(trans1)

session.commit()

session.close()

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
