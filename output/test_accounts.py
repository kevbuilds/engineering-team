import unittest
from datetime import datetime, timedelta
from accounts import get_share_price, Transaction, Account


class TestGetSharePrice(unittest.TestCase):
    def test_get_valid_share_price(self):
        self.assertEqual(get_share_price("AAPL"), 150.00)
        self.assertEqual(get_share_price("TSLA"), 200.00)
        self.assertEqual(get_share_price("GOOGL"), 2800.00)
    
    def test_get_invalid_share_price(self):
        with self.assertRaises(ValueError):
            get_share_price("INVALID")


class TestTransaction(unittest.TestCase):
    def test_deposit_transaction(self):
        trans = Transaction("DEPOSIT", amount=1000)
        self.assertEqual(trans.transaction_type, "DEPOSIT")
        self.assertEqual(trans.amount, 1000)
        self.assertEqual(trans.total_value, 1000)
    
    def test_buy_transaction(self):
        trans = Transaction("BUY", symbol="AAPL", quantity=10, price=150.00)
        self.assertEqual(trans.transaction_type, "BUY")
        self.assertEqual(trans.symbol, "AAPL")
        self.assertEqual(trans.quantity, 10)
        self.assertEqual(trans.total_value, 1500.00)
    
    def test_transaction_to_dict(self):
        trans = Transaction("DEPOSIT", amount=500)
        trans_dict = trans.to_dict()
        self.assertEqual(trans_dict["transaction_type"], "DEPOSIT")
        self.assertEqual(trans_dict["amount"], 500)


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("ACC001")
    
    def test_account_initialization(self):
        self.assertEqual(self.account.account_id, "ACC001")
        self.assertEqual(self.account.cash_balance, 0.0)
        self.assertEqual(len(self.account.holdings), 0)
    
    def test_deposit_success(self):
        result = self.account.deposit(1000)
        self.assertTrue(result)
        self.assertEqual(self.account.cash_balance, 1000)
        self.assertEqual(self.account.initial_deposit, 1000)
    
    def test_deposit_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)
        with self.assertRaises(ValueError):
            self.account.deposit(0)
    
    def test_withdraw_success(self):
        self.account.deposit(1000)
        result = self.account.withdraw(300)
        self.assertTrue(result)
        self.assertEqual(self.account.cash_balance, 700)
    
    def test_withdraw_insufficient_funds(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.withdraw(200)
    
    def test_buy_shares_success(self):
        self.account.deposit(2000)
        result = self.account.buy_shares("AAPL", 10)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 10)
        self.assertEqual(self.account.cash_balance, 500)
    
    def test_buy_shares_insufficient_funds(self):
        self.account.deposit(100)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 10)
    
    def test_buy_shares_invalid_quantity(self):
        self.account.deposit(1000)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -5)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 0)
    
    def test_sell_shares_success(self):
        self.account.deposit(2000)
        self.account.buy_shares("AAPL", 10)
        result = self.account.sell_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.cash_balance, 1250)
    
    def test_sell_shares_removes_empty_holding(self):
        self.account.deposit(1500)
        self.account.buy_shares("AAPL", 10)
        self.account.sell_shares("AAPL", 10)
        self.assertNotIn("AAPL", self.account.holdings)
    
    def test_sell_shares_not_owned(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 5)
    
    def test_sell_shares_insufficient_quantity(self):
        self.account.deposit(1500)
        self.account.buy_shares("AAPL", 5)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 10)
    
    def test_get_holdings(self):
        self.account.deposit(5000)
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 5)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings["AAPL"]["quantity"], 10)
        self.assertEqual(holdings["AAPL"]["current_price"], 150.00)
        self.assertEqual(holdings["TSLA"]["quantity"], 5)
    
    def test_get_portfolio_value(self):
        self.account.deposit(5000)
        self.account.buy_shares("AAPL", 10)
        portfolio_value = self.account.get_portfolio_value()
        expected_value = 3500 + (10 * 150)
        self.assertEqual(portfolio_value, expected_value)
    
    def test_get_profit_loss(self):
        self.account.deposit(3000)
        self.account.buy_shares("AAPL", 10)
        pl = self.account.get_profit_loss()
        self.assertEqual(pl["initial_deposit"], 3000)
        self.assertEqual(pl["current_value"], 3000)
        self.assertEqual(pl["profit_loss"], 0)
    
    def test_get_transaction_history(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 5)
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["transaction_type"], "DEPOSIT")
        self.assertEqual(history[1]["transaction_type"], "BUY")
    
    def test_get_transaction_history_filtered(self):
        self.account.deposit(1000)
        self.account.buy_shares("AAPL", 5)
        self.account.deposit(500)
        history = self.account.get_transaction_history(transaction_type="DEPOSIT")
        self.assertEqual(len(history), 2)
    
    def test_get_cash_balance(self):
        self.account.deposit(500)
        self.assertEqual(self.account.get_cash_balance(), 500)
    
    def test_get_account_summary(self):
        self.account.deposit(2000)
        self.account.buy_shares("AAPL", 5)
        summary = self.account.get_account_summary()
        self.assertEqual(summary["account_id"], "ACC001")
        self.assertIn("cash_balance", summary)
        self.assertIn("holdings", summary)
        self.assertIn("portfolio_value", summary)


if __name__ == "__main__":
    unittest.main()