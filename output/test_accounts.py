import unittest
from unittest.mock import patch
from datetime import datetime
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account()

    def test_onboard_user_success(self):
        success, message = self.account.onboard_user("John Doe", 1000.0)
        self.assertTrue(success)
        self.assertEqual(self.account.user_name, "John Doe")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.initial_deposit, 1000.0)

    def test_onboard_user_empty_name(self):
        success, message = self.account.onboard_user("", 1000.0)
        self.assertFalse(success)
        self.assertEqual(message, "User name cannot be empty.")

    def test_onboard_user_invalid_funding(self):
        success, message = self.account.onboard_user("John Doe", 0)
        self.assertFalse(success)
        self.assertEqual(message, "Initial funding must be greater than zero.")

    def test_deposit_positive(self):
        self.account.onboard_user("John Doe", 1000.0)
        success, message = self.account.deposit(500.0)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)  # Initial + New

    def test_deposit_negative(self):
        success, message = self.account.deposit(-100.0)
        self.assertFalse(success)
        self.assertEqual(message, "Deposit amount must be positive.")

    def test_withdraw_success(self):
        self.account.onboard_user("John Doe", 1000.0)
        success, message = self.account.withdraw(400.0)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 600.0)

    def test_withdraw_insufficient_funds(self):
        self.account.onboard_user("John Doe", 100.0)
        success, message = self.account.withdraw(200.0)
        self.assertFalse(success)
        self.assertEqual(message, "Insufficient balance for withdrawal.")

    def test_buy_share_success(self):
        self.account.onboard_user("John Doe", 5000.0)
        # COALINDIA price is 450.0
        success, message = self.account.buy_share("COALINDIA", 2)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 4100.0)
        self.assertEqual(self.account.holdings["COALINDIA"]["quantity"], 2)
        self.assertEqual(self.account.holdings["COALINDIA"]["avg_price"], 450.0)

    def test_buy_share_insufficient_balance(self):
        self.account.onboard_user("John Doe", 100.0)
        success, message = self.account.buy_share("COALINDIA", 1)
        self.assertFalse(success)
        self.assertIn("Insufficient balance", message)

    def test_buy_share_invalid_symbol(self):
        self.account.onboard_user("John Doe", 1000.0)
        success, message = self.account.buy_share("INVALID", 1)
        self.assertFalse(success)
        self.assertIn("Invalid symbol", message)

    def test_sell_share_success(self):
        self.account.onboard_user("John Doe", 1000.0)
        self.account.buy_share("COALINDIA", 2) # Cost 900
        # Balance is 100
        success, message = self.account.sell_share("COALINDIA", 1)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 550.0)
        self.assertEqual(self.account.holdings["COALINDIA"]["quantity"], 1)

    def test_sell_share_not_owned(self):
        self.account.onboard_user("John Doe", 1000.0)
        success, message = self.account.sell_share("MARICO", 1)
        self.assertFalse(success)
        self.assertEqual(message, "You do not own any shares of MARICO.")

    def test_sell_share_insufficient_quantity(self):
        self.account.onboard_user("John Doe", 1000.0)
        self.account.buy_share("COALINDIA", 1)
        success, message = self.account.sell_share("COALINDIA", 2)
        self.assertFalse(success)
        self.assertIn("Insufficient shares", message)

    def test_portfolio_summary(self):
        self.account.onboard_user("John Doe", 1000.0)
        self.account.buy_share("COALINDIA", 1) # Price 450
        summary = self.account.get_portfolio_summary()
        self.assertEqual(summary["balance"], 550.0)
        self.assertEqual(summary["market_value"], 450.0)
        self.assertEqual(summary["total_value"], 1000.0)
        self.assertEqual(summary["total_pl"], 0.0)

    def test_get_share_price_helper(self):
        self.assertEqual(get_share_price("COALINDIA"), 450.00)
        self.assertEqual(get_share_price("MARICO"), 670.00)
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)

if __name__ == "__main__":
    unittest.main()