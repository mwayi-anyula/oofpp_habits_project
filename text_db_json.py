import json
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

today = datetime.now()
timeformat = "%Y-%m-%d"

def generate_predefined_habits():
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

    with open('test_db.json', 'w') as file:
        json.dump(predefined_habits, file, indent=4, default=str)

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

# Generate the predefined_habits.json file
generate_predefined_habits()