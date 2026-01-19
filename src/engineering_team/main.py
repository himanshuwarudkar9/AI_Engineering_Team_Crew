#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
requirements = """
A simple account management system with an interactive, responsive UI for a trading simulation platform
The UI should support user onboarding with guided steps to create an account
The system should allow users to deposit and withdraw funds using intuitive input forms and real-time balance updates
The system should allow users to buy or sell shares via an interactive trade panel, providing quantity and symbol selection
The UI should display instant validation messages for insufficient balance, invalid quantity, or unavailable holdings
The system should calculate and visually display the total portfolio value, including real-time profit or loss from the initial deposit
The system should allow users to view current holdings through a dynamic table or card-based layout
The system should allow users to view profit or loss at any point in time using charts or highlighted indicators
The system should allow users to view transaction history in a sortable and filterable timeline or table
The system should prevent invalid actions such as negative balance withdrawals, buying beyond available funds, or selling shares not owned, with clear UI feedback
The system should provide confirmation modals or notifications for successful trades and fund operations
The system has access to a function get_share_price(symbol) which returns the current price of a share, with a test implementation for Coal India, Marico, and ICICI AMC
The UI should maintain a clean, modern design with clear navigation, responsive layout, and user-friendly interactions
"""
module_name="accounts.py"
class_name="Account"
def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }
    
    try:
        EngineeringTeam().engineering_team().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()