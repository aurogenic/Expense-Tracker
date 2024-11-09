import sqlite3
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import shutil
from constants import *


DB_FILENAME = 'expenses.db'


def create_table():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            amount REAL,
            time TEXT,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(title, category, amount, time, note):

    time = datetime.now().strftime('%Y-%m-%d') + "::" + time

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (title, category, amount, time, note) VALUES (?, ?, ?, ?, ?)',
                   (title, category, amount, time, note))
    conn.commit()
    conn.close()
    load_expenses()

def load_expenses():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    expenses = [list(x) for x in expenses]
    for exp in expenses:
        exp[4] = datetime.strptime(exp[4], '%Y-%m-%d::%I:%M %p')
    return expenses

def delete_expense(id):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', 
                   (str(id)))
    conn.commit()
    conn.close()

def update_expense(id, title, category, amount, note):
    
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses SET title = ?, category = ?, amount = ?, note = ? WHERE id = ?
    """, (title, category, amount, note, id))
    conn.commit()
    conn.close()

def export_to_csv(filename):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'category', 'amount', 'time', 'note'])
        writer.writerows(expenses)

def import_from_csv(filename, overwrite=True):

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    if overwrite:
        clear_data()
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('INSERT INTO expenses (title, category, amount, time, note) VALUES (?, ?, ?, ?, ?)',
                  [ *(list(row.values())[1:])])
    conn.commit()
    conn.close()

def category_wise():
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        results = cursor.fetchall()
        return results
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        conn.close()
        return []

def expenses_by_day(expenses, day=datetime.now().date()):
    return [exp for exp in expenses if exp[4].date() == day]

def expenses_between_days(expenses, start, end=datetime.now().date()):
    return [exp for exp in expenses if start <= exp[4].date() <= end]

def expenses_by_week(expenses, date=datetime.now().date()):
    week = date.isocalendar()[1]
    year = date.year
    return [exp for exp in expenses
            if exp[4].isocalendar()[1] == week and exp[4].year == year]

def expenses_by_month(expenses, year=datetime.now().year , month=datetime.now().month):
    return [exp for exp in expenses
            if exp[4].year == year and month == exp[4].month]

def total(expenses):
    return sum(exp[3] for exp in expenses)

from collections import defaultdict
def category_total(data):
    result = defaultdict(float) 
    for exp in data:
        result[exp[2]] += exp[3]
    return result

def timeperiod_total(expenses, period="Weekly"):
    result = defaultdict(float)

    for exp in expenses:
        date = exp[4]

        if period == "Weekly":
            key = date.isocalendar()[1]
        elif period == "Monthly" or period == "Total":
            key = (date.year, date.month)
        else:
            key = date.date()
        
        result[key] += exp[3]
    return result

def show_bar_chart(data, period="Weekly"):
    if data:
        if (period=="Weekly"):
            labels = [f"Week {week}" for week in data.keys()]
        elif period=="Monthly":
            labels = [f"{year}-{month:02d}" for year, month in data.keys()]
        else:
            labels = [date.strftime("%Y-%m-%d") for date in data.keys()]
        values = list(data.values())


        plt.bar(labels, values, color=sec_bg)
        plt.ylabel('Expenses')
        plt.title(f"{period} Expenditure", fontsize=20, pad=5)
        plt.figtext(0.05, .90, f"Total: {sum(values)}", fontsize=15, color="darkblue")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("No data available for visualization.")

def show_pie_chart(data, title):
    if(data):
        categories = data.keys()
        amounts = data.values()
        plt.fill()
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', textprops={'color': 'White'} )
        plt.title(title, fontsize=20, pad=5)
        plt.figtext(0.05, .90, f"Total: {sum(amounts)}", fontsize=15, color="darkblue")
        plt.tight_layout()
        plt.legend(loc='lower right')
        plt.show()

def import_data(filename):
    try:
        if filename.endswith('.csv'):
            import_from_csv(filename)
        if filename.endswith('.db'):
            shutil.copy(filename, DB_FILENAME)
    except Exception as e:
        print("Unsupported file type")


def export_data(filename):
    try:
        if filename.endswith('.csv'):
            export_to_csv(filename)
        if filename.endswith('.db'):
            shutil.copy(DB_FILENAME, filename)
    except Exception as e:
        print("Unsupported file type")

    

def clear_data():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE expenses')
    conn.commit()
    conn.close()
    create_table()

# export_to_csv('daata.csv')
# import_from_csv('daata.csv')
# print(load_expenses)