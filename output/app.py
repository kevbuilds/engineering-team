import gradio as gr
from accounts import Account

account = Account("USER001")

def deposit_funds(amount):
    try:
        account.deposit(float(amount))
        return f"✓ Deposited ${amount:.2f}. New balance: ${account.get_cash_balance():.2f}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def withdraw_funds(amount):
    try:
        account.withdraw(float(amount))
        return f"✓ Withdrew ${amount:.2f}. New balance: ${account.get_cash_balance():.2f}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, int(quantity))
        return f"✓ Bought {quantity} shares of {symbol}. Cash balance: ${account.get_cash_balance():.2f}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, int(quantity))
        return f"✓ Sold {quantity} shares of {symbol}. Cash balance: ${account.get_cash_balance():.2f}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def show_holdings():
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings"
    result = "Holdings:\n"
    for symbol, data in holdings.items():
        result += f"{symbol}: {data['quantity']} shares @ ${data['current_price']:.2f} = ${data['total_value']:.2f}\n"
    return result

def show_portfolio():
    portfolio_value = account.get_portfolio_value()
    cash = account.get_cash_balance()
    result = f"Cash Balance: ${cash:.2f}\n"
    result += f"Total Portfolio Value: ${portfolio_value:.2f}\n"
    return result

def show_profit_loss():
    pl = account.get_profit_loss()
    result = f"Initial Deposit: ${pl['initial_deposit']:.2f}\n"
    result += f"Current Value: ${pl['current_value']:.2f}\n"
    result += f"Profit/Loss: ${pl['profit_loss']:.2f} ({pl['profit_loss_percentage']:.2f}%)\n"
    return result

def show_transactions():
    transactions = account.get_transaction_history()
    if not transactions:
        return "No transactions"
    result = "Transaction History:\n"
    for t in transactions:
        ts = t['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        if t['transaction_type'] in ["DEPOSIT", "WITHDRAWAL"]:
            result += f"[{ts}] {t['transaction_type']}: ${t['amount']:.2f}\n"
        else:
            result += f"[{ts}] {t['transaction_type']}: {t['quantity']} {t['symbol']} @ ${t['price']:.2f}\n"
    return result

with gr.Blocks(title="Trading Account Demo") as demo:
    gr.Markdown("# Trading Account Management Demo")
    
    with gr.Tab("Manage Funds"):
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Deposit Amount", value=1000)
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                deposit_btn.click(deposit_funds, inputs=[deposit_amount], outputs=[deposit_output])
            
            with gr.Column():
                withdraw_amount = gr.Number(label="Withdraw Amount", value=100)
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                withdraw_btn.click(withdraw_funds, inputs=[withdraw_amount], outputs=[withdraw_output])
    
    with gr.Tab("Trade Shares"):
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Symbol", value="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
                buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=[buy_output])
            
            with gr.Column():
                sell_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Symbol", value="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=5)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
                sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=[sell_output])
    
    with gr.Tab("View Account"):
        with gr.Row():
            with gr.Column():
                holdings_btn = gr.Button("Show Holdings")
                holdings_output = gr.Textbox(label="Holdings", lines=5)
                holdings_btn.click(show_holdings, outputs=[holdings_output])
            
            with gr.Column():
                portfolio_btn = gr.Button("Show Portfolio")
                portfolio_output = gr.Textbox(label="Portfolio", lines=5)
                portfolio_btn.click(show_portfolio, outputs=[portfolio_output])
        
        with gr.Row():
            with gr.Column():
                pl_btn = gr.Button("Show Profit/Loss")
                pl_output = gr.Textbox(label="Profit/Loss", lines=5)
                pl_btn.click(show_profit_loss, outputs=[pl_output])
            
            with gr.Column():
                transactions_btn = gr.Button("Show Transactions")
                transactions_output = gr.Textbox(label="Transaction History", lines=10)
                transactions_btn.click(show_transactions, outputs=[transactions_output])

if __name__ == "__main__":
    demo.launch()