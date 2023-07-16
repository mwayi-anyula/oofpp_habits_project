import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from unittest.mock import patch
from cli import CLI

class TestCLI:
    @pytest.fixture
    def cli(self):
        return CLI()

    @patch('builtins.input')
    def test_create_habit(self, mock_input, cli):
        mock_input.side_effect = [
            "My Habit",
            "Habit Description",
            "Daily",
            "2023-07-01",
            "2023-08-01",
            "n"  # Do not show the habit after creation
        ]
        cli.create_habit_db = lambda args: None  # Mock the create_habit_db method

        cli.create_habit()

        # Assert that the mock_input was called with the expected prompts
        assert mock_input.call_args_list == [
            (("Enter the name of the habit:",),),
            (("Enter the description of the habit:",),),
            (("Enter the frequency of the habit:",),),
            (("Enter the start date of the habit (YYYY-MM-DD):",),),
            (("Enter the end date of the habit (YYYY-MM-DD):",),),
            (("Show the created habit? (y/n):",),)
        ]

    @patch('builtins.input')
    def test_update_habit(self, mock_input, cli):
        mock_input.side_effect = [
            "1",
            "Updated Habit",
            "",
            "",
            "",
            "",
        ]
        cli.update_habit_db = lambda args: None  # Mock the update_habit_db method

        cli.update_habit()

        # Assert that the mock_input was called with the expected prompts
        assert mock_input.call_args_list == [
            (("Enter the ID of the habit to update:",),),
            (("Enter the new name of the habit (leave empty to keep unchanged):",),),
            (("Enter the new description of the habit (leave empty to keep unchanged):",),),
            (("Enter the new frequency of the habit (leave empty to keep unchanged):",),),
            (("Enter the new start date of the habit (YYYY-MM-DD, leave empty to keep unchanged):",),),
            (("Enter the new end date of the habit (YYYY-MM-DD, leave empty to keep unchanged):",),),
        ]

    @patch('builtins.input')
    def test_delete_habit(self, mock_input, cli):
        mock_input.return_value = "1"
        cli.db.delete_habit = lambda habit_id: None  # Mock the delete_habit method

        cli.delete_habit()

        # Assert that the mock_input was called with the expected prompt
        mock_input.assert_called_once_with("Enter the ID of the habit to delete:")

    @patch('builtins.input')
    def test_check_habit(self, mock_input, cli):
        mock_input.side_effect = [
            "1",
            "2023-07-15",
        ]
        cli.db.fetch_habit = lambda habit_id: {"frequency": "daily", "status": {}}
        cli.update_habit_db = lambda args: None  # Mock the update_habit_db method

        with patch('cli.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 7, 15)
            cli.check_habit()

        # Assert that the mock_input was called with the expected prompts
        assert mock_input.call_args_list == [
            (("Enter the ID of the habit to check:",),),
            (("Enter the date to mark as completed (YYYY-MM-DD):",),),
        ]

    @patch('builtins.input')
    def test_filter_by_frequency(self, mock_input, cli):
        mock_input.side_effect = [
            "Daily",
            "list"
        ]
        cli.db.fetch_habits_by_frequency = lambda frequency: [{"name": "Habit 1"}, {"name": "Habit 2"}]
        cli.list_habits = lambda: None  # Mock the list_habits method

        cli.filter_by_frequency()

        # Assert that the mock_input was called with the expected prompts
        assert mock_input.call_args_list == [
            (("Please select a habit frequency:",),),
            (("Show a habit/ list all habits:",),),
        ]
