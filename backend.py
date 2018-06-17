# EasySplitter by Alex Cheng

# Using Flask framework and SQLAlchemy ORM for SQL querying.
import login
import sample_bill_data

from flask import Flask, render_template, redirect, url_for, request, flash

from wtforms import Form, StringField, IntegerField, TextAreaField, validators, FloatField, RadioField
from wtforms.validators import InputRequired

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


app = Flask(__name__)
Base = declarative_base()


# Defining table columns.
class BillSpending(Base):
    __tablename__ = 'spending'

    id = Column('spending', Integer, primary_key=True,autoincrement=True)
    spender_id = Column('spender', Integer)  # either 0 or 1
    amt_spent = Column('amt_spent', Integer)
    detail = Column('detail', Integer, ForeignKey('detail.detail'))


class BillDetail(Base):
    __tablename__ = 'detail'

    id = Column('detail', Integer, primary_key=True, autoincrement=True)
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
    who_paid = RadioField('Who Paid?', choices=[(0, 'Alex'), (1, 'Jenn'), (2, 'Split')], default=2)


# MySQL database login details, username, password, and address from login.py.
connection_string = 'mysql+pymysql://' + login.database_str

# Connect to database via engine creation.
engine = create_engine(connection_string, echo=True)
Base.metadata.create_all(bind=engine)

SQL_Session = sessionmaker(engine)
sql_sess = SQL_Session()


def add_sample_bills():
    for bill in sample_bill_data.sample_bills():
        detail = BillDetail()
        detail.restaurant = bill['restaurant']
        detail.date = bill['date']
        detail.notes = bill['notes']
        detail.who_paid = bill['who_paid']
        sql_sess.add(detail)
        sql_sess.flush()

        # Creating user 0 spending object
        bill_0 = BillSpending()
        bill_0.spender_id = 0
        bill_0.amt_spent = int(bill['spending_0'] * 100)
        bill_0.detail = detail.id

        # Creating user 1 spending object
        bill_1 = BillSpending()
        bill_1.spender_id = 1
        bill_1.amt_spent = int(bill['spending_1'] * 100)
        bill_1.detail = detail.id

        sql_sess.add(bill_0)
        sql_sess.add(bill_1)

    sql_sess.commit()
    sql_sess.close()


#add_sample_bills()


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

    if request.method == 'POST':
        detail = BillDetail()
        detail.restaurant = form.restaurant.data
        detail.date = form.date.data
        detail.notes = form.notes.data
        detail.who_paid = form.who_paid.data
        sql_sess.add(detail)
        sql_sess.flush()

        # Creating user 0 spending object
        trans0 = BillSpending()
        trans0.spender_id = 0
        trans0.amt_spent = int(form.user_0_spending.data * 100)
        trans0.detail = detail.id

        # Creating user 1 spending object
        trans1 = BillSpending()
        trans1.spender_id = 1
        trans1.amt_spent = int(form.user_1_spending.data * 100)
        trans1.detail = detail.id

        sql_sess.add(trans0)
        sql_sess.add(trans1)

        sql_sess.commit()
        sql_sess.close()

        flash("Bill Added!", 'success')

        return redirect(url_for('home'))

    return render_template('add.html', form=form)


# Starts the Flask app
if __name__ == '__main__':
    app.secret_key = login.secret_key
    app.run()

