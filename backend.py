# EasySplitter by Alex Cheng

# Using Flask framework and SQLAlchemy ORM for SQL querying.
import login
from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


app = Flask(__name__)
Base = declarative_base()

# Defining table columns.
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

# MySQL database login details, username, password, and address from login.py.
connection_string = 'mysql+pymysql://' + login.database_str

# Connect to database via engine creation.
engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(engine)
session = Session()

# Creating detail object
detail = TransactionDetails()
detail.restaurant = 'Joy Wok'
detail.date = '2018-06-12'
detail.notes = 'delicious'
detail.who_paid = 0
session.add(detail)
session.flush()

# Creating user 0 spending object
trans0 = Transaction()
trans0.spender_id = 0
trans0.amt_spent = 1000
trans0.detail_id = detail.id

# Creating user 1 spending object
trans1 = Transaction()
trans1.spender_id = 1
trans1.amt_spent = 1000
trans1.detail_id = detail.id

session.add(trans0)
session.add(trans1)

session.commit()
session.close()

# Creating default Flask route
@app.route('/')
def index():
    return "Home Page"

# Starts the Flask app
if __name__ == '__main__':
    app.run()
