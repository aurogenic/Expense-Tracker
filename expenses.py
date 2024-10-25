import sqlite3
from datetime import datetime
import csv
import matplotlib.pyplot as plt


CATEGORIES = ["Others", "Food and Snacks", "Shopping and Clothing", "Medical and Healthcar", "Utilities", "Rent and Recharges", "Miscellaneous"]


# Database setup
def create_table():
    conn = sqlite3.connect('expenses.db')
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

# Add expense to database
def add_expense(title, category, amount, time, note):

    time = datetime.now().strftime('%Y-%m-%d') + "::" + time

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (title, category, amount, time, note) VALUES (?, ?, ?, ?, ?)',
                   (title, category, amount, time, note))
    conn.commit()
    conn.close()
    load_expenses()

# Load and display expenses from the database
def load_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    expenses = [list(x) for x in expenses]
    for exp in expenses:
        exp[4] = datetime.strptime(exp[4], '%Y-%m-%d::%I:%M %p')
    return expenses


def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', 
                   (str(id)))
    conn.commit()
    conn.close()

def update_expense(id, title, category, amount, note):
    
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses SET title = ?, category = ?, amount = ?, note = ? WHERE id = ?
    """, (title, category, amount, note, id))
    conn.commit()
    conn.close()

def export_to_csv():
    expenses = load_expenses()
    with open('expenses.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Title', 'Category', 'Amount', 'Date', 'Time', 'Note'])
        writer.writerows(expenses)


def category_wise():
    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        results = cursor.fetchall()
        return results
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
        conn.close()
        return []

def show_bar_chart(event=None):
        results = category_wise()
        if results:
            categories = [row[0] for row in results]
            amounts = [row[1] for row in results]

            plt.bar(categories, amounts)
            plt.xlabel('Category')
            plt.ylabel('Amount')
            plt.title('Spending by Category')
            plt.show()
        else:
            print("No data available for visualization.")

def show_pie_chart(event=None):
    results = category_wise()
    if results:
        categories = [row[0] for row in results]
        amounts = [row[1] for row in results]
        plt.fill()
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.show()
    else:
        print("No data available for visualization.")


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

