# Habit Tracking App

The Habit Tracking App is a command-line application that allows you to track your habits, maintain streaks, and view statistics. It helps you stay accountable and motivated towards your daily habits.

## Features

- **Habit Creation**: Easily create new habits by providing a name, description, frequency (daily, weekly, or monthly), and start/end dates.
- **Habit Modification**: Update existing habits by changing their name, description, frequency, or date range.
- **Habit Deletion**: Delete unwanted habits from the database.
- **Habit Completion**: Mark habits as completed for a specific date, maintaining streaks and tracking progress.
- **Viewing Habits**: Display or view a single habit or list all habits stored in the database.
- **Statistics**: View detailed statistics about your habits, including total habits, average completion rate, and longest streaks.
- **Flexible Tracking**: Choose from daily, weekly, or monthly frequency options for each habit, allowing customization based on your habit requirements.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mwayi-anyula/oofpp_habits_project.git
   ```

2. Change into the project directory:

   ```bash
   cd oofpp_habits_project
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

## Usage

Once the application is running, follow the menu prompts to perform different actions:

- **View Habits**: Choose the option to show a single habit or list all habits, and view the details of each habit, including its name, description, frequency, start date, end date, and streak statistics.
- **Create a Habit**: Choose the option to create a new habit, and provide the required information such as name, description, frequency, and date range.
- **Update a Habit**: Select the option to update an existing habit, choose the habit you want to update, and modify the necessary fields.
- **Delete a Habit**: Choose the option to delete a habit, select the habit you want to delete from the list, and confirm the deletion.
- **Mark a Habit as Completed**: Select the option to check/complete a habit, choose the habit you want to mark as completed, and enter the date for which you completed the habit.
- **View Statistics**: Choose the option to view statistics and select the desired statistics to display, such as total habits, average completion rate, or longest streaks.
- **Get Help**: If you need assistance or want to know more about each command and its usage, select the option for help. The app will provide instructions and explanations for using the different features.
- **Exit the App**: When you are finished using the Habit Tracking App, select the exit option to close the application.

```bash
Welcome to the habit tracking app!

? What do you want to do? (Use arrow keys)
 » Show a habit/ list all habits
   Create, update, delete a habit
   Check/Complete a task
   View statistics
   Need some help?
   Exit
```

## Testing

To run the tests for the Habit Tracking App, you can use the pytest framework. Make sure you have pytest installed (it should be included in the requirements.txt file):

```bash
pip install -r requirements.txt
```

Then, navigate to the project directory and run the tests:

```bash
pytest
```

The tests are defined in the `test_cli.py` file and cover various scenarios to ensure the proper functionality of the app.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/mwayi-anyula/oofpp_habits_project/issues).

To contribute to the project, follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

[MIT License](LICENSE)

## Contact

If you have any questions or need assistance, feel free to reach out to [mwai3d@gmail.com](mailto:mwai3d@gmail.com).

---

Happy habit tracking!