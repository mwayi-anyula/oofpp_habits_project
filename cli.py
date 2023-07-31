from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import questionary
from analytics import Statistics
from habit import Habit
from tabulate import tabulate
from database import Database
import json

# Reusable variables and constants

back = "<< Back"
menu = "Main menu"
go_back = [{"value": back, "name": back}, {"value": menu, "name": menu}]
dateformat = "%d.%m.%Y"
timeformat = "%Y-%m-%d"
today = datetime.now()
one_month_from_now = (today + relativedelta(months=1)).strftime(timeformat)
table_header = ["Id", "Name", "Description", "Frequency", "Longest Streak", "Start Date", "End Date"]
habits_not_found = "\n🚫 No habit(s) found in the database.\n"


def tablify(data, table_header):
    if table_header == "no_header":
        tabulated = tabulate(data, tablefmt='psql', showindex=False)
    elif table_header == "no_header_right":
        tabulated = tabulate(data, tablefmt='psql', colalign=("right",), showindex=False)
    elif table_header == "header_keys":
        tabulated = tabulate(data, headers="keys", tablefmt='psql', showindex=False)
    else:
        tabulated = tabulate(data, headers=table_header, tablefmt='psql', showindex=False)

    print(f"\n{tabulated}\n")


class CLI:
    """A class to implement the command-line interface for the app."""

    def __init__(self):
        """Initialize the CLI with a database."""
        self.db = Database("habits.db")  # create a database object

    def run(self):
        """Run the app by parsing the user input and executing the commands."""
        self.db.connect()  # connect to the database
        self.db.create_table()  # create the table if not exists
        self.welcome()  # display a welcome message

        while True:  # loop until the user exits
            command = questionary.select("What do you want to do?", choices=[
                {"name": "Show a habit/ list all habits", "value": "show"},
                {"name": "Create, update, delete a habit", "value": "modify"},
                {"name": "Check/Complete a task", "value": "log"},
                {"name": "View statistics", "value": "stats"},
                {"name": "Need some help?", "value": "help"},
                {"name": "Exit", "value": "exit"},
            ]).ask()  # get the user input

            if command == "create":
                self.create_habit()
            elif command == "show":
                command_show = questionary.select("Show a habit/ list all habits:", choices=[
                    {"value": "single", "name": "Show single habit"},
                    {"value": "list", "name": "List all habits"},
                    {"value": "list_frequency", "name": "List habits by frequency"},
                    {"value": "mock_database", "name": "Load predefine data"},
                    {"value": back, "name": back},
                ]).ask()
                if command_show == "single":
                    self.show_menu_habit()
                elif command_show == "list":
                    self.list_habits()
                elif command_show == "list_frequency":
                    self.filter_by_frequency()
                elif command_show == "mock_database":
                    try:
                        self.db.generate_predefined_habits()
                    except:
                        print("\nDatabase seems not to be empty. Clear the database and try again\n")
                    else:
                        print("\nPredefined/ mock data has successfully been added to the database")
                        self.list_habits()
                elif command_show == back:
                    self.run()
            elif command == "modify":
                command_modify = questionary.select("Create, update, delete a habit:", choices=[
                    {"value": "create", "name": "Create a new habit"},
                    {"value": "update", "name": "Update/Edit an existing habit"},
                    {"value": "delete", "name": "Delete an existing habit"},
                    {"value": back, "name": back},
                ]).ask()
                if command_modify == "create":
                    self.create_habit()
                elif command_modify == "update":
                    self.update_habit()
                elif command_modify == "delete":
                    self.delete_habit()
                elif command_modify == back:
                    self.run()
            elif command == "log":
                try:
                    self.show_stats()
                except:
                    print(habits_not_found)
                else:
                    command_log = questionary.select("Check/ Complete habit:", choices=[
                        {"value": "check_in", "name": "Check habit as done"},
                        {"value": "clear_log", "name": "Clear check-in / log data"},
                        {"value": back, "name": back},
                    ]).ask()
                    if command_log == "check_in":
                        self.check_habit()
                    elif command_log == "clear_log":
                        self.clear_habit_status()
                    elif command_log == back:
                        self.run()
            elif command == "stats":
                try:
                    self.show_stats()
                except:
                    print(habits_not_found)
            elif command == "help":
                self.show_help()
            elif command == "exit":
                print("\n👋 Keep your habit streaks!\n🤗 Until next time, bye.\n")
                break

        self.db.close()  # close the database connection and cursor

    def welcome(self):
        """Display a welcome message and a list of available commands."""
        print("\n\nWelcome to the habit tracking app!\n")

    def create_habit(self):
        """Create a new habit with the given arguments."""
        name = questionary.text("Enter the name of the habit:",
                                validate=lambda name: True if name.isalpha() and len(name) > 1
                                else "Please enter a valid name").ask()
        description = questionary.text("Enter the description of the habit:").ask()
        frequency = questionary.select("Enter the frequency of the habit:",
                                       choices=["Daily", "Weekly", "Monthly"]).ask().lower()
        start_date = questionary.text("Enter the start date of the habit (YYYY-MM-DD):").ask()
        end_date = questionary.text("Enter the end date of the habit (YYYY-MM-DD):").ask()

        args = {
            'name': name,
            'description': description,
            'frequency': frequency,
            'start_date': start_date,
            'end_date': end_date
        }

        self.create_habit_db(args)

    def create_habit_db(self, args):
        """Create a new habit in the database with the given arguments."""
        id = None
        name = args['name']
        description = args['description']
        frequency = args['frequency']
        start_date = datetime.strptime(args['start_date'], timeformat).date() if args['start_date'] else today.date()
        end_date = datetime.strptime(args['end_date'], timeformat).date() if args['end_date'] else one_month_from_now
        status = {}

        habit = Habit(id, name, description, frequency, start_date, end_date, status)
        habit_dict = habit.create()
        self.db.insert_habit(habit_dict)
        print(f"\n✔ Successfully created a new habit: {name}")
        self.show_habit(self.db.get_latest_entry_id())

    def list_habits(self):
        """List all habits stored in the database."""
        try:
            habits = self.db.fetch_all_habits()
            self.tabulate_list(habits)
        except:
            print(habits_not_found)

    def show_habit(self, id):
        """Show single habit stored in the database."""
        habits = self.db.fetch_all_habits()
        stats = Statistics()
        stats.calculate(habits)
        if habits:
            data = []
            for habit in habits:
                if habit["id"] == id:
                    habit_data = [
                        habit["id"],
                        habit["name"],
                        habit["description"],
                        habit["frequency"],
                        stats.get_streak_with_id(habits, habit["id"]),
                        habit["start_date"],
                        habit["end_date"],
                    ]
                    data.append(habit_data)
            tablify(data, table_header)
        else:
            print(habits_not_found)

    def show_menu_habit(self):
        """Delete an existing habit with the given ID."""
        try:
            habit_selected = self.habits_from_db()
            if habit_selected != back:
                self.show_habit(int(habit_selected))
                self.show_menu_habit()  # Returns to previous menu
        except:
            print(habits_not_found)

    def update_habit(self):
        """Update an existing habit with the given arguments."""
        habit_selected = self.habits_from_db()
        if habit_selected == back:
            return
        else:
            habit_id = habit_selected
            name = questionary.text("Enter the new name of the habit (leave empty to keep unchanged):").ask()
            description = questionary.text("Enter the new description of the habit (leave empty to keep unchanged):").ask()
            frequency = questionary.select("Enter the frequency of the habit (leave empty to keep unchanged):",
                                           choices=["Daily", "Weekly", "Monthly"]).ask().lower()
            start_date = questionary.text("Enter the new start date of the habit (YYYY-MM-DD, leave empty to keep unchanged):").ask()
            end_date = questionary.text("Enter the new end date of the habit (YYYY-MM-DD, leave empty to keep unchanged):").ask()

            args = {
                'habit_id': habit_id,
                'name': name,
                'description': description,
                'frequency': frequency,
                'start_date': start_date,
                'end_date': end_date
            }

            self.update_habit_db(args)

    def update_habit_db(self, args):
        """Update an existing habit in the database with the given arguments."""
        habit_id = args["habit_id"]
        habit = self.db.fetch_habit(habit_id)

        if habit:
            name = args["name"]
            description = args["description"]
            frequency = args["frequency"]
            start_date = args["start_date"]
            end_date = args["end_date"]

            # Update only the non-empty and non-whitespace values
            if name.strip() and not name.isspace():
                habit["name"] = name
            if description.strip() and not description.isspace():
                habit["description"] = description
            if frequency.strip() and not frequency.isspace():
                habit["frequency"] = frequency
            if start_date.strip() and not start_date.isspace():
                habit["start_date"] = start_date
            if end_date.strip() and not end_date.isspace():
                habit["end_date"] = end_date

            self.db.update_habit(habit_id, habit)
            print(f"\n✔ Habit has been successfully updated.\n")
        else:
            print(f"\n🚫 No habit found.\n")

    def delete_habit(self):
        """Delete an existing habit with the given ID."""
        habit_selected = self.habits_from_db()
        if habit_selected != back:
            habit_id = habit_selected
            self.db.delete_habit(habit_id)
            print(f"\n✔ Habit with ID {habit_id} has been successfully deleted.\n")

    def check_habit(self):
        """Mark a habit as completed for a given date."""
        habit_selected = self.habits_from_db()
        if habit_selected == back:
            return
        else:
            habit_id = habit_selected
            start_date, end_date = self.db.fetch_date_range(habit_id)
            date = self.select_date(start_date, end_date)

            args = {
                'habit_id': habit_id,
                'date': str(date),
            }

            self.check_habit_db(args)

    def check_habit_db(self, args):
        habit_id = args['habit_id']
        date = args['date']

        habit = self.db.fetch_habit(habit_id)

        if habit:
            frequency = habit['frequency']
            status = habit['status']

            if self.is_valid_log_date(date, frequency, status):
                status[date] = True
                self.update_missing_logs(status, habit['start_date'], date)  # Update missing logs
                self.db.complete_habit(habit_id, status)
                print(f"\n✔ \"{habit['name']}\" has been marked as completed for date: {date}\n")
            else:
                print(f"\n🚫 Logging for this habit is allowed only \"{frequency.lower()}\"\n")

        else:
            print(f"No habit found with ID {habit_id}.")

    def clear_habit_status(self):
        """Clear the logged data in the status column of a habit."""
        habit_selected = self.habits_from_db()
        if habit_selected == back:
            return
        else:
            habit_id = habit_selected
            self.db.clear_habit_status(habit_id)
            print(f"\n✔ Logged data for habit with ID {habit_id} has been cleared.\n")

    def filter_by_frequency(self):
        """Display the habit names available in the database for the user to choose from."""
        frequency_choice = questionary.select(
            "Please select a habit frequency:",
            choices=["Daily", "Weekly", "Monthly", back]
        ).ask()

        if frequency_choice == back:
            return back

        try:
            habits = self.db.fetch_habits_by_frequency(frequency_choice)
            self.tabulate_list(habits)
            self.filter_by_frequency()
        except:
            print(f"\n🚫 Habits with the frequency \"{frequency_choice}\" are not currently being tracked\n")

    def tabulate_list(self, habits):
        """Reusable function to tabulate default list of habits"""
        stats = Statistics()
        stats.calculate(habits)
        if habits:
            data = []
            for habit in habits:
                habit_data = [
                    habit["id"],
                    habit["name"],
                    habit["description"],
                    habit["frequency"],
                    stats.get_streak_with_id(habits, habit["id"]),
                    habit["start_date"],
                    habit["end_date"],
                ]
                data.append(habit_data)
            tablify(data, table_header)
        else:
            print("\n🚫 No habits found in the database.\n")

    def is_valid_log_date(self, date, frequency, status):
        """Check if the given date is a valid log date based on the habit's frequency and existing logs."""
        if date in status:
            return False  # Log already exists for the given date

        if frequency.lower() == "daily":
            return True  # Log is allowed for any date since it's a daily habit

        if frequency.lower() == "weekly":
            # Check if any log exists in the same week as the given date
            week_start = self.get_week_start(date)
            week_end = self.get_week_end(date)
            return not any(log_date for log_date in status if week_start <= log_date <= week_end)

        if frequency.lower() == "monthly":
            # Check if any log exists in the same month as the given date
            month_start = self.get_month_start(date)
            month_end = self.get_month_end(date)
            return not any(log_date for log_date in status if month_start <= log_date <= month_end)

        return False  # Invalid frequency

    def get_week_start(self, date):
        """Get the start date of the week for the given date."""
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()  # Convert input date to date object
        week_start = date_obj - timedelta(days=date_obj.weekday())  # Subtract timedelta from date_obj
        return week_start

    def get_week_end(self, date):
        """Get the end date of the week for the given date."""
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()  # Convert input date to date object
        week_end = date_obj + timedelta(days=6 - date_obj.weekday())  # Add timedelta to date_obj
        return week_end

    def get_month_start(self, date):
        """Get the start date of the month for the given date."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert input date to datetime object
        month_start = date_obj.replace(day=1).date()  # Set day component to 1 and convert back to date object
        return month_start

    def get_month_end(self, date):
        """Get the end date of the month for the given date."""
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert input date to datetime object
        next_month = date.replace(day=28) + timedelta(days=4)
        month_end = next_month - timedelta(days=next_month.day)
        return month_end

    def update_missing_logs(self, status, start_date, end_date):
        """Update missing logs in the status dictionary from the start date to the given end date."""
        current_date = datetime.strptime(start_date, timeformat).date()
        end_date = datetime.strptime(end_date, timeformat).date()

        while current_date <= end_date:
            if current_date.strftime(timeformat) not in status:
                status[current_date.strftime(timeformat)] = False
            current_date += timedelta(days=1)

    def validate_date(self, date, start_date, end_date):
        """Validate if the date is within the start and end date range."""
        date_obj = self.date_to_timestamp(date)
        start_date_obj = self.date_to_timestamp(start_date)
        end_date_obj = self.date_to_timestamp(end_date)
        # return start_date_obj <= date_obj <= end_date_obj
        return start_date_obj <= date_obj <= end_date_obj

    def select_date(self, start_date, end_date):
        """Prompt the user to select a date for marking habit completion."""
        choices = [
            "Today's date",
            "Yesterday's date",
            "Enter a specific date",
            back
        ]

        date_option = questionary.select(
            "Select a date option:",
            choices=choices
        ).ask()

        if date_option == choices[0]:
            date = datetime.now().date()
        elif date_option == choices[1]:
            date = (datetime.now().date() - timedelta(days=1))
        elif date_option == back:
            self.run()
        else:
            date_input = questionary.text("Enter a specific date (YYYY-MM-DD):").ask()

            try:
                date = datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please try again (YYYY-MM-DD).")
                return self.select_date(start_date, end_date)

        if not self.validate_date(date, start_date, end_date):
            print("Invalid date. Please select a date within the specified range.")
            return self.select_date(start_date, end_date)

        return date

    def habits_from_db(self):
        """Display the habit names available in the database for the user to choose from."""
        try:
            habits = self.db.fetch_all_habits()

            if habits:
                habit_choices = [{"name": habit["name"], "value": str(habit["id"])} for habit in habits]
                habit_choices.append({"name": back, "value": back})
                return questionary.select("Please select a habit:", choices=habit_choices).ask()
            else:
                raise ValueError("No habit in the database. Add a habit first to use this function.")
        except:
            print(habits_not_found)

    def show_total_stats(self, stats, long):
        total_streaks = stats.show_total().split("|")
        total_streaks_arr = total_streaks[1].replace("'", "\"")
        total_streaks_arr2 = json.loads(total_streaks_arr)
        total_streaks_arr2.sort(key=lambda x: x["Streak"], reverse=True)
        if long == 1:
            print("Your longest streak of habit completions is", total_streaks_arr2[0]["Streak"])
            tablify([total_streaks_arr2[0]], "header_keys")
        else:
            print("\n", total_streaks[0])
            tablify(total_streaks_arr2, "header_keys")

    def show_stats(self):
        """Show various statistics based on your habit data."""
        habits = self.db.fetch_all_habits()
        stats = Statistics()
        stats.calculate(habits)

        options = [
            {"value": "all", "name": "Show all statistics"},
            {"value": "single_stat", "name": "Show longest streak"},
            {"value": "single_habit", "name": "Show single habit statistics"},
            {"value": back, "name": back},
        ]

        choice = questionary.select("What statistics would you like to see?", choices=options).ask()

        if choice == "all":
            # Show all statistics
            self.show_total_stats(stats, 0)
            stats.show_average()
            stats.show_streak()
            back_choice = questionary.select("Would like to go back?", choices=go_back).ask()
            if back_choice == back:
                self.run()
            else:
                self.show_stats()
        elif choice == "single_stat":
            # Show longest streak
            self.show_total_stats(stats, 1)
            back_choice = questionary.select("Would like to go back?", choices=go_back).ask()
            if back_choice == back:
                self.run()
            else:
                self.show_stats()
        elif choice == "single_habit":
            # Show single habit statistics
            habit_selected = self.habits_from_db()
            if habit_selected == back:
                return
            else:
                habit_id = habit_selected
                habit = self.db.fetch_habit(habit_id)
                if habit:
                    habit_stats = stats.show_single_habit_stats(habit)
                    if habit_stats:
                        tablify([habit_stats], "header_keys")
                    else:
                        print(f"\n🚫 No statistics found for habit with ID {habit_id}.\n")
                else:
                    print(f"\n🚫 No habit found with ID {habit_id}.\n")
            back_choice = questionary.select("Would like to go back?", choices=go_back).ask()
            if back_choice == back:
                self.run()
            else:
                self.show_stats()

    def show_help(self):
        """Display help instructions for using the habit tracking app."""
        print("\nThis app helps you track your habits and maintain streaks. You can create habits, update their details, mark them as completed, and view various statistics.\n"
              "\n- To create a new habit, choose the 'Create, update, delete a habit' option and then select 'Create a new habit'."
              "\n- To update an existing habit, choose the 'Create, update, delete a habit' option and then select 'Update/Edit an existing habit'."
              "\n- To delete a habit, choose the 'Create, update, delete a habit' option and then select 'Delete an existing habit'."
              "\n- To mark a habit as completed, choose the 'Check/Complete a task' option and then select 'Check habit as done'."
              "\n- To view statistics, choose the 'View statistics' option and select the desired statistics to view."
              "\n- To exit the app, choose the 'Exit' option."
              "\n\nNote: You can always go back by selecting the appropriate option from the menus."
              "\n")

    def date_to_timestamp(self, date):
        """Convert the date string to a timestamp for comparison."""
        return datetime.strptime(date, "%Y-%m-%d").timestamp()
