import sqlite3
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

today = datetime.now()
timeformat = "%Y-%m-%d"

class Database:
    """A class to handle the connection and interaction with the SQLite database."""

    def __init__(self, db_name):
        """Initialize the database with the given name."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the database and create a cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create a table in the database to store habit records."""
        sql = """CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            frequency TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )"""
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_habit(self, habit_dict):
        """Insert a habit record into the database table."""
        # Convert the 'status' value to JSON string
        habit_dict['status'] = json.dumps(habit_dict['status'])
        sql = """INSERT INTO habits (id, name, description, frequency, start_date, end_date, status)
                 VALUES (:id, :name, :description, :frequency, :start_date, :end_date, :status)"""
        self.cursor.execute(sql, habit_dict)
        self.conn.commit()

    def update_habit(self, habit_id, habit_dict):
        """Update multiple attributes of a habit record in the database table."""
        set_clauses = []
        values = []
        for key, value in habit_dict.items():
            if value is not None:
                if key == 'status':
                    # Fetch the current status dictionary from the habit record
                    current_status = self.fetch_habit(habit_id).get('status') or {}
                    # Update the current status dictionary with the new data
                    current_status.update(value)
                    # Convert the updated status to JSON string
                    value = json.dumps(current_status)
                set_clauses.append(f"{key} = ?")
                values.append(value)
        if set_clauses:
            set_clause = ", ".join(set_clauses)
            values.append(habit_id)
            sql = f"UPDATE habits SET {set_clause} WHERE id = ?"
            self.cursor.execute(sql, values)
            self.conn.commit()

    def delete_habit(self, id):
        """Delete a habit record from the database table."""
        sql = "DELETE FROM habits WHERE id = ?"
        self.cursor.execute(sql, (id,))
        self.conn.commit()

    def fetch_habit(self, id):
        """Fetch a habit record from the database table by its ID."""
        sql = "SELECT * FROM habits WHERE id = ?"
        self.cursor.execute(sql, (id,))
        row = self.cursor.fetchone()
        if row:
            habit_dict = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "frequency": row[3],
                "start_date": row[4],
                "end_date": row[5],
                "status": json.loads(row[6])  # Convert the 'status' value from JSON string to a Python object
            }
            return habit_dict
        else:
            return None

    def fetch_all_habits(self):
        """Fetch all habit records from the database table and return them as a list of dictionaries."""
        habits = []
        sql = "SELECT * FROM habits"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            habit_dict = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "frequency": row[3],
                "start_date": row[4],
                "end_date": row[5],
                "status": json.loads(row[6])  # Convert the 'status' value from JSON string to a Python object
            }
            habits.append(habit_dict)
        return habits
    
    def fetch_habits_by_frequency(self, frequency):
        """Fetch all habit records with a specific frequency from the database table and return them as a list of dictionaries."""
        habits = []
        sql = "SELECT * FROM habits WHERE frequency = ?"
        self.cursor.execute(sql, (frequency.lower(),))
        rows = self.cursor.fetchall()
        for row in rows:
            habit_dict = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "frequency": row[3],
                "start_date": row[4],
                "end_date": row[5],
                "status": json.loads(row[6])  # Convert the 'status' value from JSON string to a Python object
            }
            habits.append(habit_dict)
        return habits
    
    def fetch_date_range(self, id):
        """Fetch the start_date and end_date from the database for a specific habit record ID."""
        sql = "SELECT start_date, end_date FROM habits WHERE id = ?"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        if result:
            start_date, end_date = result
            return start_date, end_date
        else:
            return None, None

    def complete_habit(self, id, log_data):
        """Log habit data and update the 'status' column in the database table."""
        habit = self.fetch_habit(id)
        if habit:
            status = habit['status'] or {}  # Retrieve the current status or initialize as an empty dictionary
            status.update(log_data)  # Update the status dictionary with the log_data
            # Convert the updated status to JSON string
            status_json = json.dumps(status)
            sql = "UPDATE habits SET status = ? WHERE id = ?"
            self.cursor.execute(sql, (status_json, id))
            self.conn.commit()
    
    def get_latest_entry_id(self):
        """Get the ID of the latest entry based on the maximum 'id' value in the 'habits' table."""
        sql = "SELECT MAX(id) FROM habits"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            latest_id = result[0]
            return latest_id
        else:
            return None
        
    def clear_habit_status(self, habit_id):
        """Clear the logged data in the status column of a habit."""
        sql = "UPDATE habits SET status = '{}' WHERE id = ?"
        self.cursor.execute(sql, (habit_id,))
        self.conn.commit()
        
    def generate_predefined_habits(self):
        """Generate predefined habits and store them in the database."""
        self.connect()
        self.create_table()

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
            habit['status'] = self.generate_logged_status(start_date, end_date, habit['frequency'])
            self.insert_habit(habit)

    def generate_logged_status(self,start_date, end_date, frequency):
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


    def close(self):
        """Close the connection and cursor."""
        self.cursor.close()
        self.conn.close()