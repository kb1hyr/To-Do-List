# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


def do_menu():
    result = 7
    while result not in [0, 1, 2, 3, 4, 5, 6]:
        print('1) Today\'s tasks\n2) Week\'s tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit')
        # print("1) Today's activity")
        # print("2) Week's activity")
        # print("3) All tasks")
        # print("4) Missed tasks")
        # print("5) Add task")
        # print("6) Delete task")
        # print("0) Exit")
        result = int(input())
    return result


def add_task():
    global session
    print('Enter task')
    the_task = input()
    print('Enter deadline')
    the_entered_date = input()
    the_deadline = datetime.strptime(the_entered_date, "%Y-%m-%d")
    new_row = Table(task=the_task, deadline=the_deadline.date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def todays_tasks():
    global session
    today = datetime.today()
    print(f"Today: {today.strftime('%-d %b')}:")
    rows = session.query(Table).filter(Table.deadline == today.date())
    counter = 0
    for row in rows:
        print(row.task)
        counter += 1
    if counter == 0:
        print('Nothing to do!')
    print('')


def weeks_tasks():
    global session
    today = datetime.today()
    for delta in range(0, 7):
        the_day = today + timedelta(days=delta)
        print(f"{the_day.strftime('%A %-d %b')}")
        rows = session.query(Table).filter(Table.deadline == the_day.date())
        if rows.count == 0:
            print('Nothing to do!')
            print('')
        else:
            counter = 0
            for row in rows:
                counter += 1
                print(f"{str(counter)}. {row.task}")
            print('')


def all_tasks():
    global session
    rows = session.query(Table).order_by(Table.deadline).all()
    print('All tasks:')
    counter = 0
    for row in rows:
        counter += 1
        print(f"{str(counter)}. {row.task}. {row.deadline.strftime('%-d %b')}")
    if counter == 0:
        print('Nothing to do!')
    print('')


def missed_tasks():
    global session
    today = datetime.today()
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline <= today.date()).all()
    counter = 0
    for row in rows:
        counter += 1
        print(f"{str(counter)}. {row.task}. {row.deadline.strftime('%-d %b')}")
    if counter == 0:
        print('Nothing is missed!')
    print('')


def delete_task():
    global session
    rows = session.query(Table).order_by(Table.deadline).all()
    print('Choose the number of the task you want to delete:')
    counter = 0
    my_dict = {}
    for row in rows:
        counter += 1
        print(f"{str(counter)}. {row.task}. {row.deadline.strftime('%-d %b')}")
        my_dict[counter] = row
    if counter == 0:
        print('Nothing to do!')
        print('')
        return
    row_num = int(input())
    session.delete(my_dict.get(row_num))
    session.commit()
    print('The task has been deleted!')
    print('')


# Main program
# Set up database
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Do program loop
menu_choice = -1

while menu_choice != 0:
    menu_choice = do_menu()
    if menu_choice == 1:
        todays_tasks()
    if menu_choice == 2:
        weeks_tasks()
    if menu_choice == 3:
        all_tasks()
    if menu_choice == 4:
        missed_tasks()
    if menu_choice == 5:
        add_task()
    if menu_choice == 6:
        delete_task()


print('')
print('Bye!')
