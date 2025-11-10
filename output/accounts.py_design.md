# Account Management System - Detailed Design Specification

## Module: `accounts.py`

This module implements a simple account management system for a trading simulation platform. The system tracks cash balance, share holdings, and transaction history while enforcing business rules to prevent invalid operations.

---

## Classes

### 1. `Transaction`

Represents a single transaction in the system.

#### Attributes:
- `timestamp` (datetime): The date and time when the transaction occurred
- `transaction_type` (str): Type of transaction - "DEPOSIT", "WITHDRAWAL", "BUY", or "SELL"
- `amount` (float): Cash amount involved (for deposits/withdrawals)
- `symbol` (str): Stock symbol (for buy/sell transactions)
- `quantity` (int): Number of shares (for buy/sell transactions)
- `price` (float): Price per share at transaction time (for buy/sell transactions)
- `total_value` (float): Total value of the transaction

#### Methods:
- `__init__(self, transaction_type, amount=None, symbol=None, quantity=None, price=None)`: Initialize a transaction record
- `__str__(self)`: Return a human-readable string representation of the transaction
- `to_dict(self)`: Return a dictionary representation of the transaction for serialization

---

### 2. `Account`

The main account class that manages user funds, holdings, and transactions.

#### Attributes:
- `account_id` (str): Unique identifier for the account
- `cash_balance` (float): Current available cash in the account
- `initial_deposit` (float): The total amount deposited initially (for P&L calculation)
- `holdings` (dict): Dictionary mapping stock symbols to quantities held (e.g., {"AAPL": 10, "TSLA": 5})
- `transactions` (list): List of Transaction objects representing the transaction history

#### Methods:

##### Account Management Methods:
- `__init__(self, account_id)`: 
  - Initialize a new account with the given account_id
  - Set cash_balance to 0
  - Initialize empty holdings dictionary
  - Initialize empty transactions list
  - Set initial_deposit to 0

- `deposit(self, amount)`:
  - Add funds to the account
  - Parameters: `amount` (float) - amount to deposit
  - Validation: amount must be positive
  - Updates cash_balance and initial_deposit
  - Records a DEPOSIT transaction
  - Returns: True if successful, raises ValueError if amount is invalid

- `withdraw(self, amount)`:
  - Remove funds from the account
  - Parameters: `amount` (float) - amount to withdraw
  - Validation: 
    - amount must be positive
    - amount must not exceed cash_balance (prevents negative balance)
  - Updates cash_balance
  - Records a WITHDRAWAL transaction
  - Returns: True if successful, raises ValueError if validation fails

##### Trading Methods:
- `buy_shares(self, symbol, quantity)`:
  - Purchase shares of a given stock
  - Parameters: 
    - `symbol` (str) - stock symbol (e.g., "AAPL")
    - `quantity` (int) - number of shares to buy
  - Process:
    - Get current share price using `get_share_price(symbol)`
    - Calculate total cost (quantity × price)
    - Validate: 
      - quantity must be positive integer
      - total cost must not exceed cash_balance
    - Update cash_balance (subtract total cost)
    - Update holdings (add to existing quantity or create new entry)
    - Record a BUY transaction
  - Returns: True if successful, raises ValueError if validation fails

- `sell_shares(self, symbol, quantity)`:
  - Sell shares of a given stock
  - Parameters:
    - `symbol` (str) - stock symbol
    - `quantity` (int) - number of shares to sell
  - Process:
    - Get current share price using `get_share_price(symbol)`
    - Calculate total proceeds (quantity × price)
    - Validate:
      - quantity must be positive integer
      - symbol must exist in holdings
      - quantity must not exceed owned shares
    - Update cash_balance (add total proceeds)
    - Update holdings (subtract quantity, remove entry if zero)
    - Record a SELL transaction
  - Returns: True if successful, raises ValueError if validation fails

##### Reporting Methods:
- `get_holdings(self)`:
  - Return current holdings with current market values
  - Returns: Dictionary with structure:
    ```python
    {
      "AAPL": {
        "quantity": 10,
        "current_price": 150.00,
        "total_value": 1500.00
      },
      "TSLA": {
        "quantity": 5,
        "current_price": 200.00,
        "total_value": 1000.00
      }
    }
    ```

- `get_portfolio_value(self)`:
  - Calculate total portfolio value (cash + market value of all holdings)
  - Returns: float - total value of cash plus all share holdings at current prices

- `get_profit_loss(self)`:
  - Calculate profit or loss from initial deposit
  - Formula: current_portfolio_value - initial_deposit
  - Returns: Dictionary with structure:
    ```python
    {
      "initial_deposit": 10000.00,
      "current_value": 11500.00,
      "profit_loss": 1500.00,
      "profit_loss_percentage": 15.0
    }
    ```

- `get_transaction_history(self)`:
  - Return list of all transactions
  - Parameters: Optional filters like `transaction_type`, `symbol`, `start_date`, `end_date`
  - Returns: List of Transaction objects (or dictionaries via to_dict())

- `get_cash_balance(self)`:
  - Return current cash balance
  - Returns: float - current available cash

##### Utility Methods:
- `__str__(self)`:
  - Return a human-readable string representation of the account
  - Includes account_id, cash balance, and summary of holdings

- `get_account_summary(self)`:
  - Return comprehensive account information
  - Returns: Dictionary containing:
    - account_id
    - cash_balance
    - holdings (detailed)
    - portfolio_value
    - profit_loss
    - transaction_count

---

## Module-Level Functions

### `get_share_price(symbol)`

Returns the current price of a share for a given symbol.

#### Parameters:
- `symbol` (str): The stock symbol (e.g., "AAPL", "TSLA", "GOOGL")

#### Returns:
- `float`: The current price of the share

#### Test Implementation:
```python
def get_share_price(symbol):
    """
    Test implementation that returns fixed prices for specific symbols.
    In production, this would call a real market data API.
    """
    prices = {
        "AAPL": 150.00,
        "TSLA": 200.00,
        "GOOGL": 2800.00
    }
    if symbol not in prices:
        raise ValueError(f"Unknown stock symbol: {symbol}")
    return prices[symbol]
```

---

## Error Handling

The module should implement proper error handling:

- **ValueError**: Raised for invalid inputs (negative amounts, insufficient funds, unknown symbols, etc.)
- **KeyError**: Raised when trying to access non-existent holdings
- All errors should include descriptive messages to help identify the issue

---

## Data Validation Rules

1. **Deposits**: Amount must be > 0
2. **Withdrawals**: Amount must be > 0 AND ≤ cash_balance
3. **Buy Shares**: 
   - Quantity must be positive integer
   - Total cost must not exceed cash_balance
   - Symbol must be valid (recognized by get_share_price)
4. **Sell Shares**:
   - Quantity must be positive integer
   - Symbol must exist in holdings
   - Quantity must not exceed owned shares

---

## Usage Example

```python
# Create an account
account = Account("USER_001")

# Deposit funds
account.deposit(10000.00)

# Buy shares
account.buy_shares("AAPL", 10)
account.buy_shares("TSLA", 5)

# Check holdings
holdings = account.get_holdings()

# Check portfolio value
portfolio_value = account.get_portfolio_value()

# Check profit/loss
profit_loss = account.get_profit_loss()

# Sell shares
account.sell_shares("AAPL", 5)

# Withdraw funds
account.withdraw(1000.00)

# View transaction history
transactions = account.get_transaction_history()

# Get account summary
summary = account.get_account_summary()
```

---

## Implementation Notes

1. All monetary values should be stored as floats with 2 decimal precision
2. Timestamps should use Python's `datetime` module
3. The module should be completely self-contained and importable
4. All methods should include docstrings with parameter and return type information
5. The module should include basic input validation before processing operations
6. Transaction history should maintain chronological order
7. Holdings dictionary should only contain non-zero quantities