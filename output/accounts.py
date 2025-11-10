from datetime import datetime


def get_share_price(symbol):
    prices = {
        "AAPL": 150.00,
        "TSLA": 200.00,
        "GOOGL": 2800.00
    }
    if symbol not in prices:
        raise ValueError(f"Unknown stock symbol: {symbol}")
    return prices[symbol]


class Transaction:
    def __init__(self, transaction_type, amount=None, symbol=None, quantity=None, price=None):
        self.timestamp = datetime.now()
        self.transaction_type = transaction_type
        self.amount = amount
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        
        if transaction_type in ["DEPOSIT", "WITHDRAWAL"]:
            self.total_value = amount
        elif transaction_type in ["BUY", "SELL"]:
            self.total_value = quantity * price
        else:
            self.total_value = 0
    
    def __str__(self):
        if self.transaction_type in ["DEPOSIT", "WITHDRAWAL"]:
            return f"[{self.timestamp}] {self.transaction_type}: ${self.amount:.2f}"
        else:
            return f"[{self.timestamp}] {self.transaction_type}: {self.quantity} shares of {self.symbol} @ ${self.price:.2f} = ${self.total_value:.2f}"
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price": self.price,
            "total_value": self.total_value
        }


class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.cash_balance = 0.0
        self.initial_deposit = 0.0
        self.holdings = {}
        self.transactions = []
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.cash_balance += amount
        self.initial_deposit += amount
        
        transaction = Transaction("DEPOSIT", amount=amount)
        self.transactions.append(transaction)
        
        return True
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.cash_balance:
            raise ValueError("Insufficient funds for withdrawal")
        
        self.cash_balance -= amount
        
        transaction = Transaction("WITHDRAWAL", amount=amount)
        self.transactions.append(transaction)
        
        return True
    
    def buy_shares(self, symbol, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        
        price = get_share_price(symbol)
        total_cost = quantity * price
        
        if total_cost > self.cash_balance:
            raise ValueError("Insufficient funds to buy shares")
        
        self.cash_balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        transaction = Transaction("BUY", symbol=symbol, quantity=quantity, price=price)
        self.transactions.append(transaction)
        
        return True
    
    def sell_shares(self, symbol, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        
        if symbol not in self.holdings:
            raise ValueError(f"No holdings found for symbol: {symbol}")
        
        if quantity > self.holdings[symbol]:
            raise ValueError("Insufficient shares to sell")
        
        price = get_share_price(symbol)
        total_proceeds = quantity * price
        
        self.cash_balance += total_proceeds
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        transaction = Transaction("SELL", symbol=symbol, quantity=quantity, price=price)
        self.transactions.append(transaction)
        
        return True
    
    def get_holdings(self):
        holdings_report = {}
        
        for symbol, quantity in self.holdings.items():
            current_price = get_share_price(symbol)
            total_value = quantity * current_price
            
            holdings_report[symbol] = {
                "quantity": quantity,
                "current_price": current_price,
                "total_value": total_value
            }
        
        return holdings_report
    
    def get_portfolio_value(self):
        total_value = self.cash_balance
        
        for symbol, quantity in self.holdings.items():
            current_price = get_share_price(symbol)
            total_value += quantity * current_price
        
        return total_value
    
    def get_profit_loss(self):
        current_value = self.get_portfolio_value()
        profit_loss = current_value - self.initial_deposit
        
        if self.initial_deposit > 0:
            profit_loss_percentage = (profit_loss / self.initial_deposit) * 100
        else:
            profit_loss_percentage = 0.0
        
        return {
            "initial_deposit": self.initial_deposit,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage
        }
    
    def get_transaction_history(self, transaction_type=None, symbol=None, start_date=None, end_date=None):
        filtered_transactions = self.transactions
        
        if transaction_type:
            filtered_transactions = [t for t in filtered_transactions if t.transaction_type == transaction_type]
        
        if symbol:
            filtered_transactions = [t for t in filtered_transactions if t.symbol == symbol]
        
        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t.timestamp >= start_date]
        
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t.timestamp <= end_date]
        
        return [t.to_dict() for t in filtered_transactions]
    
    def get_cash_balance(self):
        return self.cash_balance
    
    def __str__(self):
        holdings_summary = ", ".join([f"{symbol}: {qty}" for symbol, qty in self.holdings.items()])
        if not holdings_summary:
            holdings_summary = "None"
        
        return f"Account {self.account_id}: Cash=${self.cash_balance:.2f}, Holdings=[{holdings_summary}]"
    
    def get_account_summary(self):
        return {
            "account_id": self.account_id,
            "cash_balance": self.cash_balance,
            "holdings": self.get_holdings(),
            "portfolio_value": self.get_portfolio_value(),
            "profit_loss": self.get_profit_loss(),
            "transaction_count": len(self.transactions)
        }