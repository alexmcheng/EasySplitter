# EasySplitter by Alex Cheng

# Using Flask framework and SQLAlchemy ORM for SQL querying.
import login
import sample_bill_data
import datetime

from flask import Flask, render_template, redirect, url_for, request, flash

from wtforms import Form, StringField, IntegerField, TextAreaField, validators, FloatField, RadioField
from wtforms.validators import InputRequired

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query, join


app = Flask(__name__)
Base = declarative_base()


# Defining table columns.
class BillSpending(Base):
    __tablename__ = 'spending'

    id = Column('spending', Integer, primary_key=True,autoincrement=True)
    user_id = Column('user_id', Integer)  # either 0 or 1
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
engine = create_engine(connection_string, echo=False)
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
        bill_0.user_id = 0
        bill_0.amt_spent = int(bill['spending_0'] * 100)
        bill_0.detail = detail.id

        # Creating user 1 spending object
        bill_1 = BillSpending()
        bill_1.user_id = 1
        bill_1.amt_spent = int(bill['spending_1'] * 100)
        bill_1.detail = detail.id

        sql_sess.add(bill_0)
        sql_sess.add(bill_1)

    sql_sess.commit()
    sql_sess.close()


# add_sample_bills()


# Creating default Flask route.
@app.route('/')
def home():
    bills_0_qry = sql_sess.query(BillSpending, BillDetail).join(BillDetail, BillSpending.detail == BillDetail.id). \
        filter(BillSpending.user_id == 0). \
        order_by(desc(BillDetail.date))
    bills_1_qry = sql_sess.query(BillSpending, BillDetail).join(BillDetail, BillSpending.detail == BillDetail.id). \
        filter(BillSpending.user_id == 1). \
        order_by(desc(BillDetail.date))

    two_weeks_ago = (datetime.datetime.today() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    spending_list = [0]

    two_weeks_0_qry = sql_sess. \
        query(func.sum(BillSpending.amt_spent), BillDetail). \
        join(BillDetail, BillSpending.detail == BillDetail.id). \
        filter(BillSpending.user_id == 0 and BillDetail.date >= two_weeks_ago).scalar() #and BillDetail.date >= two_weeks_ago )

    #spending_list.append(two_weeks_0_qry)

    two_weeks_1_qry = sql_sess. \
        query(func.sum(BillSpending.amt_spent)). \
        join(BillDetail, BillSpending.detail == BillDetail.id). \
        filter(BillSpending.user_id == 1). \
        filter(BillDetail.date >= two_weeks_ago).scalar()


    user_0_extra = 0
    user_1_extra = 0

    for bills in bills_0_qry:
        if bills.BillDetail.who_paid == 1:
            user_1_extra += bills.BillSpending.amt_spent

    for bills in bills_1_qry:
        if bills.BillDetail.who_paid == 0:
            user_0_extra += bills.BillSpending.amt_spent

    if(user_0_extra > user_1_extra):
        spent_more = "Alex has covered $" + str((user_0_extra - user_1_extra) / 100) + " for Jenn"
    else:
        spent_more = "Jenn has covered $" + str((user_1_extra - user_0_extra) / 100) + " for Alex"

    return render_template('home.html', bills_0_qry=bills_0_qry, bills_1_qry=bills_1_qry, spent_more=spent_more, spending_list=spending_list)


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
        trans0.user_id = 0
        trans0.amt_spent = int(form.user_0_spending.data * 100)
        trans0.detail = detail.id

        # Creating user 1 spending object
        trans1 = BillSpending()
        trans1.user_id = 1
        trans1.amt_spent = int(form.user_1_spending.data * 100)
        trans1.detail = detail.id

        sql_sess.add(trans0)
        sql_sess.add(trans1)

        sql_sess.commit()
        sql_sess.close()

        flash("Bill Added!", 'success')

        return redirect(url_for('home'))

    return render_template('add.html', form=form)


# spending = sql_sess.query(BillSpending, BillDetail).join(BillDetail, BillSpending.detail == BillDetail.id).\
#         filter(BillSpending.user_id == 0)
#
# print(str(spending[0].BillSpending.user_id) + " spent: " + str(spending[0].BillSpending.amt_spent))


# Starts the Flask app
if __name__ == '__main__':
    app.secret_key = login.secret_key
    app.run(debug=True)

