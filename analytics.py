from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

class Statistics:
    # ...existing code...

    def calculate(self, habits):
        """Calculate various statistics based on the habits list."""
        self.habits = habits  # store the habit data
        self.total_habits = len(habits)  # calculate the total number of habits

        total_completions = 0
        total_days = 0
        completed_habits = 0
        habit_frequencies = {}

        for habit in habits:
            status = habit["status"]
            frequency = habit["frequency"]
            total_completions += sum(status.values())
            total_days += self.calculate_total_days(habit)
            completed_habits += any(status.values())

            if frequency in habit_frequencies:
                habit_frequencies[frequency] += 1
            else:
                habit_frequencies[frequency] = 1

        self.total_completions = total_completions
        self.average_rate = round(total_completions / total_days, 2)
        self.average_frequency = habit_frequencies
        self.longest_streak = self.get_longest_streak(habits)
        self.current_streak = self.get_current_streak(habits)

    def calculate_total_days(self, habit):
        """Calculate the total days for a habit based on its frequency."""
        frequency = habit["frequency"]
        start_date = datetime.strptime(habit["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(habit["end_date"], "%Y-%m-%d").date()
        total_days = (end_date - start_date).days + 1

        if frequency == "weekly":
            total_days //= 7
        elif frequency == "monthly":
            total_days //= 30

        return total_days

    def get_longest_streak(self, habits):
        """Get the longest streak of habit completions."""
        longest_streak = 0

        for habit in habits:
            status = habit["status"]
            frequency = habit["frequency"]
            streak = 0
            max_streak = 0
            today = datetime.today().date()

            if frequency == "daily":
                for date_str in sorted(status.keys()):
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if date <= today and status[date_str]:
                        streak += 1
                        max_streak = max(max_streak, streak)
                    else:
                        streak = 0

            elif frequency == "weekly":
                start_of_week = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
                for date_str in sorted(status.keys()):
                    if date_str >= start_of_week:
                        if status[date_str]:
                            streak += 1
                            max_streak = max(max_streak, streak)
                        else:
                            streak = 0

            elif frequency == "monthly":
                start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
                for date_str in sorted(status.keys()):
                    if date_str >= start_of_month:
                        if status[date_str]:
                            streak += 1
                            max_streak = max(max_streak, streak)
                        else:
                            streak = 0

            longest_streak = max(longest_streak, max_streak)

        return longest_streak

    def get_current_streak(self, habits):
        """Get the current streak of habit completions."""
        current_streak = 0

        for habit in habits:
            status = habit["status"]
            frequency = habit["frequency"]
            today = datetime.today().date()

            if frequency == "daily":
                if status.get(today.strftime("%Y-%m-%d")):
                    current_streak += 1
                else:
                    break

            elif frequency == "weekly":
                start_of_week = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
                for date_str in sorted(status.keys(), reverse=True):
                    if date_str >= start_of_week:
                        if status[date_str]:
                            current_streak += 1
                        else:
                            break

            elif frequency == "monthly":
                start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
                for date_str in sorted(status.keys(), reverse=True):
                    if date_str >= start_of_month:
                        if status[date_str]:
                            current_streak += 1
                        else:
                            break

        return current_streak

    def calculate_single(self, habits, value_id):
        """
        Calculate statistics for a single habit using a value ID.

        Args:
            habits (list): The list of habit data.
            value_id (float): The value ID of the habit to calculate statistics for.

        Returns:
            dict or None: A dictionary containing the calculated statistics for the habit, or None if no habit is found with the given value ID.
        """
        habit_data = next((habit for habit in habits if habit["id"] == float(value_id)), None)

        if habit_data is None:
            return None

        total_completions = sum(habit_data["status"].values())
        total_days = self.calculate_total_days(habit_data)
        completion_rate = round(total_completions / total_days, 2)

        longest_streak = self.get_longest_streak([habit_data])
        current_streak = self.get_current_streak([habit_data])

        return {
            "value_id": value_id,
            "total_completions": total_completions,
            "total_days": total_days,
            "completion_rate": completion_rate,
            "longest_streak": longest_streak,
            "current_streak": current_streak
        }

    def show_total(self):
        """Show the total number of habits and completions."""
        print(f"You have {self.total_habits} habits and {self.total_completions} completions.")
        print("")

    def show_average(self):
        """Show the average completion rate and frequency of habits."""
        print(f"Your average completion rate is {self.average_rate}.")
        print("Your average frequency of habits is:")
        for frequency, count in self.average_frequency.items():
            print(f"- Frequency {frequency}: {count} habits")
        print("")

    def show_streak(self):
        """Show the longest and current streaks of habit completions."""
        print(f"Your longest streak of habit completions is {self.longest_streak} days.")
        print(f"Your current streak of habit completions is {self.current_streak} days.")
        print("")
        
    def show_single(self, habits, value_id, name):
        """
        Show the statistics for a single habit using a value ID.

        Args:
            habits (list): The list of habit data.
            value_id (float): The value ID of the habit to show statistics for.
            name (str): The name of the habit.
        """
        habit_stats = self.calculate_single(habits, value_id)

        if habit_stats is None:
            print(f"No habit found with name \"{name}\".")
        else:
            print("")
            print(f"Statistics for habit \"{name}\" (Value ID {value_id}):")
            print(f"Total completions: {habit_stats['total_completions']}")
            print(f"Total days: {habit_stats['total_days']}")

            frequency = habits[0]["frequency"]  # Assuming all habits have the same frequency
            if frequency == "daily":
                print(f"Completion rate: {habit_stats['completion_rate']} per day")
            elif frequency == "weekly":
                print(f"Completion rate: {habit_stats['completion_rate']} per week")
            elif frequency == "monthly":
                print(f"Completion rate: {habit_stats['completion_rate']} per month")

            print(f"Longest streak: {habit_stats['longest_streak']} days")
            print(f"Current streak: {habit_stats['current_streak']} days")
            print("")

    def get_streak_with_id(self, habits, value_id):
        """
        Calculate the streak with the correct frequency for a habit based on its value ID.

        Args:
            habits (list): The list of habit data.
            value_id (float): The value ID of the habit.

        Returns:
            int or None: The streak of habit completions with the correct frequency for the specified habit, or None if no habit is found with the given value ID.
        """
        habit_data = next((habit for habit in habits if habit["id"] == float(value_id)), None)

        if habit_data is None:
            return None

        status = habit_data["status"]
        frequency = habit_data["frequency"]
        unit = "day(s)"
        streak = 0
        current_streak = 0
        today = datetime.today().date()

        # Calculate the streak based on the habit frequency
        if frequency == "daily":
            # Loop through each day from today to the start date and check the completion status
            start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d").date()
            for day in range((today - start_date).days + 1):
                date = start_date + timedelta(days=day)
                if status.get(date.strftime("%Y-%m-%d")):
                    current_streak += 1
                    streak = max(streak, current_streak)
                else:
                    current_streak = 0
        elif frequency == "weekly":
            unit = "week(s)"
            # Loop through each week from today to the start date and check the completion status
            start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d").date()
            for week in range((today - start_date).days // 7 + 1):
                start_date = start_date + timedelta(weeks=week)
                end_date = start_date + timedelta(days=6)
                week_status = [status.get(date.strftime("%Y-%m-%d")) for date in pd.date_range(start_date, end_date)]
                if any(week_status):
                    current_streak += 1
                    streak = max(streak, current_streak)
                else:
                    current_streak = 0
        elif frequency == "monthly":
            unit = "month(s)"
            # Loop through each month from today to the start date and check the completion status
            start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d").date().replace(day=1)
            for month in range((today.year - start_date.year) * 12 + (today.month - start_date.month) + 1):
                start_date = start_date + relativedelta(months=month)
                end_date = start_date + relativedelta(day=31)
                end_date = min(end_date, today)  # Limit the end date to today
                month_status = [status.get(date.strftime("%Y-%m-%d")) for date in pd.date_range(start_date, end_date)]
                if any(month_status):
                    current_streak += 1
                    streak = max(streak, current_streak)
                else:
                    current_streak = 0
        
        return f"{streak} {unit}"
