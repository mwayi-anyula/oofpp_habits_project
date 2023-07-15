import datetime
import json

class Habit:
    """A class to represent a habit object."""

    def __init__(self, id, name, description, frequency, start_date, end_date, status):
        """Initialize the habit with the given attributes."""
        self.id = id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def create(self):
        """Create a new habit and return it as a dictionary."""
        habit_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status
        }
        return habit_dict

    def update(self, attribute, value):
        """Update an attribute of the habit with the given value."""
        if attribute == "name":
            self.name = value
        elif attribute == "description":
            self.description = value
        elif attribute == "frequency":
            self.frequency = value
        elif attribute == "start_date":
            self.start_date = value
        elif attribute == "end_date":
            self.end_date = value
        else:
            print("Invalid attribute")

    def delete(self):
        """Delete the habit and return None."""
        return None

    def complete(self, date):
        """Mark the habit as completed for the given date."""
        if date >= self.start_date and date <= self.end_date:
            self.status[date] = True
        else:
            print("Invalid date")

    def to_database_dict(self):
        """Convert the habit object to a dictionary suitable for database insertion."""
        habit_dict = self.create()
        # Convert the 'status' dictionary to JSON string
        habit_dict['status'] = json.dumps(habit_dict['status'])
        return habit_dict

    @staticmethod
    def from_database_dict(habit_dict):
        """Create a Habit object from a dictionary retrieved from the database."""
        # Convert the 'status' JSON string to a dictionary
        habit_dict['status'] = json.loads(habit_dict['status'])
        return Habit(**habit_dict)