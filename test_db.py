import sqlite3
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

today = datetime.now()
timeformat = "%Y-%m-%d"

def create_habits_table(conn):
    """Create the 'habits' table in the database."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            frequency TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )
    """)
    conn.commit()

def insert_habit(conn, habit):
    """Insert a habit into the 'habits' table."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habits (id, name, description, frequency, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (habit['id'], habit['name'], habit['description'], habit['frequency'],
          habit['start_date'], habit['end_date'], json.dumps(habit['status'])))
    conn.commit()

def generate_predefined_habits():
    """Generate predefined habits and store them in the database."""
    conn = sqlite3.connect('test.db')
    create_habits_table(conn)

    predefined_habits = [
        {
            'id': 1,
            'name': 'Exercise',
            'description': 'Daily workout routine',
            'frequency': 'daily'
        },
        {
            'id': 2,
            'name': 'Read',
            'description': 'Read a book for at least 30 minutes',
            'frequency': 'weekly'
        },
        {
            'id': 3,
            'name': 'Meditation',
            'description': 'Practice meditation for 10 minutes',
            'frequency': 'daily'
        },
        {
            'id': 4,
            'name': 'Drink Water',
            'description': 'Drink at least 8 glasses of water',
            'frequency': 'weekly'
        },
        {
            'id': 5,
            'name': 'Learn a Language',
            'description': 'Spend 30 minutes learning a new language',
            'frequency': 'daily'
        }
    ]

    for habit in predefined_habits:
        start_date = (today - timedelta(weeks=4)).strftime(timeformat)
        end_date = today.strftime(timeformat)
        habit['start_date'] = start_date
        habit['end_date'] = end_date
        habit['status'] = generate_logged_status(start_date, end_date, habit['frequency'])
        insert_habit(conn, habit)

    conn.close()

def generate_logged_status(start_date, end_date, frequency):
    start_datetime = datetime.strptime(start_date, timeformat)
    end_datetime = datetime.strptime(end_date, timeformat)
    days = (end_datetime - start_datetime).days + 1

    if frequency == 'daily':
        return {str((start_datetime + timedelta(days=i)).date()): random.choice([True, False]) for i in range(days)}
    elif frequency == 'weekly':
        return {str((start_datetime + timedelta(weeks=i)).date()): random.choice([True, False]) for i in range(days // 7)}
    elif frequency == 'monthly':
        return {str((start_datetime + relativedelta(months=i)).date()): random.choice([True, False]) for i in range(days // 30)}
    else:
        return {}

# Generate the predefined habits and store them in the database file 'test.db'
generate_predefined_habits()
