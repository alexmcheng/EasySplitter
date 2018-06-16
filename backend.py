# EasySplitter by Alex Cheng

# Using Flask framework and SQLAlchemy ORM for SQL querying.
import login
from flask import Flask, render_template, redirect, url_for, request

from wtforms import Form, StringField, IntegerField, TextAreaField, validators, FloatField, RadioField
from wtforms.validators import InputRequired

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

# Form object for bill input on add.html
class BillForm(Form):
    user_0_spending = FloatField('Alex Spending', [InputRequired()])
    user_1_spending = FloatField('Jenn Spending', [InputRequired()])
    restaurant = StringField('Restaurant', [InputRequired()])
    date = StringField('Date (YYYY-MM-DD)', [InputRequired()])
    notes = StringField('Notes', [InputRequired()])
    who_paid = RadioField('Who Paid?', choices=[(0,'Alex'), (0,'Jenn')])


# MySQL database login details, username, password, and address from login.py.
connection_string = 'mysql+pymysql://' + login.database_str

# Connect to database via engine creation.
engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

SQL_Session = sessionmaker(engine)
sql_sess = SQL_Session()



# Creating default Flask route.
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/addbill', methods = ['GET', 'POST'])
def addbill():
    form = BillForm(request.form)
    print("add")
    if request.method == 'POST':
        print("inside POST AND VALIDAT")
        detail = TransactionDetails()
        detail.restaurant = form.restaurant.data
        detail.date = form.date.data
        detail.notes = form.notes.data
        detail.who_paid = form.who_paid.data
        sql_sess.add(detail)
        sql_sess.flush()

        # Creating user 0 spending object
        trans0 = Transaction()
        trans0.spender_id = 0
        trans0.amt_spent = int(form.user_0_spending.data * 100)
        trans0.detail_id = detail.id

        # Creating user 1 spending object
        trans1 = Transaction()
        trans1.spender_id = 1
        trans1.amt_spent = int(form.user_1_spending.data * 100)
        trans1.detail_id = detail.id

        sql_sess.add(trans0)
        sql_sess.add(trans1)

        sql_sess.commit()
        sql_sess.close()
        print("hello world!")

        return redirect(url_for('home'))

    return render_template('add.html', form=form)



# Starts the Flask app
if __name__ == '__main__':
    app.run(debug=True)
