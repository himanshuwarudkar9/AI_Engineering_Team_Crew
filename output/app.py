import gradio as gr
import pandas as pd
from datetime import datetime

def get_share_price(symbol: str) -> float:
    """
    Mock utility function to simulate real-time market data.
    Returns hardcoded prices for specific symbols.
    """
    prices = {
        "COALINDIA": 450.00,
        "MARICO": 670.00,
        "ICICIAMC": 1200.00
    }
    return prices.get(symbol.upper(), 0.0)

class Account:
    def __init__(self):
        self.user_name = ""
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.holdings = {} # Schema: { symbol: {"quantity": int, "avg_price": float} }
        self.transactions = []

    def onboard_user(self, name: str, initial_funding: float) -> tuple[bool, str]:
        if not name.strip():
            return False, "User name cannot be empty."
        if initial_funding <= 0:
            return False, "Initial funding must be greater than zero."
        
        self.user_name = name
        return self.deposit(initial_funding)

    def deposit(self, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Deposit amount must be positive."
        
        self.balance += amount
        self.initial_deposit += amount
        
        self._add_transaction("DEPOSIT", "-", 0, 0.0, amount)
        return True, f"Successfully deposited ${amount:,.2f}."

    def withdraw(self, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance for withdrawal."
        
        self.balance -= amount
        self._add_transaction("WITHDRAWAL", "-", 0, 0.0, -amount)
        return True, f"Successfully withdrew ${amount:,.2f}."

    def buy_share(self, symbol: str, quantity: int) -> tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be greater than zero."
        
        price = get_share_price(symbol)
        if price <= 0:
            return False, f"Invalid symbol or price unavailable for {symbol}."
        
        total_cost = price * quantity
        if total_cost > self.balance:
            return False, f"Insufficient balance. Total cost: ${total_cost:,.2f}, Available: ${self.balance:,.2f}."
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            current_data = self.holdings[symbol]
            new_qty = current_data["quantity"] + quantity
            new_avg = ((current_data["avg_price"] * current_data["quantity"]) + (price * quantity)) / new_qty
            self.holdings[symbol] = {"quantity": new_qty, "avg_price": new_avg}
        else:
            self.holdings[symbol] = {"quantity": quantity, "avg_price": price}
            
        self._add_transaction("BUY", symbol, quantity, price, -total_cost)
        return True, f"Successfully purchased {quantity} shares of {symbol}."

    def sell_share(self, symbol: str, quantity: int) -> tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be greater than zero."
        if symbol not in self.holdings:
            return False, f"You do not own any shares of {symbol}."
        if self.holdings[symbol]["quantity"] < quantity:
            return False, f"Insufficient shares. You only own {self.holdings[symbol]['quantity']} shares."
            
        price = get_share_price(symbol)
        total_proceeds = price * quantity
        self.balance += total_proceeds
        
        self.holdings[symbol]["quantity"] -= quantity
        if self.holdings[symbol]["quantity"] == 0:
            del self.holdings[symbol]
            
        self._add_transaction("SELL", symbol, quantity, price, total_proceeds)
        return True, f"Successfully sold {quantity} shares of {symbol}."

    def _add_transaction(self, t_type: str, symbol: str, quantity: int, price: float, amount: float):
        self.transactions.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": t_type,
            "symbol": symbol,
            "quantity": quantity,
            "price": f"${price:,.2f}",
            "amount": f"${amount:,.2f}",
            "status": "COMPLETED"
        })

    def get_portfolio_summary(self) -> dict:
        market_value = 0.0
        for symbol, data in self.holdings.items():
            market_value += get_share_price(symbol) * data["quantity"]
            
        total_value = self.balance + market_value
        total_pl = total_value - self.initial_deposit
        pl_percent = (total_pl / self.initial_deposit * 100) if self.initial_deposit > 0 else 0.0
        
        return {
            "balance": self.balance,
            "market_value": market_value,
            "total_value": total_value,
            "total_pl": total_pl,
            "pl_percent": pl_percent,
            "initial_deposit": self.initial_deposit
        }

# UI Module State
acc = Account()

def update_ui():
    summary = acc.get_portfolio_summary()
    
    # Process Holdings Dataframe
    holding_list = []
    for symbol, data in acc.holdings.items():
        cp = get_share_price(symbol)
        mv = cp * data["quantity"]
        cost_basis = data["avg_price"] * data["quantity"]
        h_pl = mv - cost_basis
        holding_list.append({
            "Symbol": symbol,
            "Qty": data["quantity"],
            "Avg Buy": f"${data['avg_price']:,.2f}",
            "Current Price": f"${cp:,.2f}",
            "Market Value": f"${mv:,.2f}",
            "P/L": f"${h_pl:,.2f}"
        })
    holdings_df = pd.DataFrame(holding_list) if holding_list else pd.DataFrame(columns=["Symbol", "Qty", "Avg Buy", "Current Price", "Market Value", "P/L"])
    
    # Process Transaction History
    history_df = pd.DataFrame(acc.transactions) if acc.transactions else pd.DataFrame(columns=["timestamp", "type", "symbol", "quantity", "price", "amount", "status"])
    if not history_df.empty:
        history_df = history_df.iloc[::-1] # Newest first
        
    pl_text = f"{summary['total_pl']:+,.2f} ({summary['pl_percent']:+.2f}%)"
    pl_color = "green" if summary['total_pl'] >= 0 else "red"
    
    summary_html = f"""
    <div style='display: flex; justify-content: space-around; background: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <div style='text-align: center;'>
            <p style='margin: 0; color: #555;'>Total Portfolio Value</p>
            <h2 style='margin: 0;'>${summary['total_value']:,.2f}</h2>
        </div>
        <div style='text-align: center;'>
            <p style='margin: 0; color: #555;'>Cash Balance</p>
            <h2 style='margin: 0;'>${summary['balance']:,.2f}</h2>
        </div>
        <div style='text-align: center;'>
            <p style='margin: 0; color: #555;'>Total Profit/Loss</p>
            <h2 style='margin: 0; color: {pl_color};'>{pl_text}</h2>
        </div>
    </div>
    """
    
    return (
        summary_html,
        holdings_df,
        history_df,
        gr.update(choices=list(acc.holdings.keys()) if acc.holdings else [])
    )

def handle_onboarding(name, amount):
    success, msg = acc.onboard_user(name, amount)
    if success:
        ui_updates = update_ui()
        return (
            gr.update(visible=False), 
            gr.update(visible=True), 
            f"Welcome, {name}!", 
            *ui_updates
        )
    else:
        raise gr.Error(msg)

def handle_deposit(amount):
    success, msg = acc.deposit(amount)
    if success:
        gr.Info(msg)
        return update_ui()
    else:
        raise gr.Error(msg)

def handle_withdraw(amount):
    success, msg = acc.withdraw(amount)
    if success:
        gr.Info(msg)
        return update_ui()
    else:
        raise gr.Error(msg)

def handle_buy(symbol, qty):
    success, msg = acc.buy_share(symbol, qty)
    if success:
        gr.Info(msg)
        return update_ui()
    else:
        raise gr.Error(msg)

def handle_sell(symbol, qty):
    success, msg = acc.sell_share(symbol, qty)
    if success:
        gr.Info(msg)
        return update_ui()
    else:
        raise gr.Error(msg)

def get_live_price(symbol):
    price = get_share_price(symbol)
    return f"Live Price: ${price:,.2f}"

with gr.Blocks(theme=gr.themes.Soft(), title="TradeSim Pro") as demo:
    gr.Markdown("# 🚀 TradeSim Pro Management System")
    
    # 1. Onboarding Container
    with gr.Column(visible=True) as onboarding_box:
        gr.Markdown("### User Onboarding")
        with gr.Row():
            username_input = gr.Textbox(label="Full Name", placeholder="Enter your name...")
            initial_fund_input = gr.Number(label="Initial Deposit ($)", value=10000.0)
        start_btn = gr.Button("Initialize My Trading Account", variant="primary")

    # 2. Main Interface Container
    with gr.Column(visible=False) as main_interface:
        welcome_msg = gr.Markdown("## Welcome")
        
        with gr.Tabs():
            # Tab 1: Dashboard
            with gr.TabItem("📊 Dashboard"):
                summary_display = gr.HTML()
                gr.Markdown("### Current Holdings")
                holdings_table = gr.Dataframe(interactive=False)
            
            # Tab 2: Trade Panel
            with gr.TabItem("📉 Trade Panel"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Buy/Sell Shares")
                        symbol_select = gr.Dropdown(choices=["COALINDIA", "MARICO", "ICICIAMC"], label="Select Stock Symbol", value="COALINDIA")
                        price_display = gr.Markdown("Live Price: $450.00")
                        quantity_input = gr.Number(label="Quantity", value=1, minimum=1)
                        
                        with gr.Row():
                            buy_btn = gr.Button("Execute Buy Order", variant="primary")
                            sell_btn = gr.Button("Execute Sell Order", variant="stop")
                        
                        gr.Markdown("---")
                        sell_select = gr.Dropdown(choices=[], label="Sell from Holdings (Only symbols you own)")
                        
                    with gr.Column(scale=1):
                        gr.Markdown("### Fund Operations")
                        fund_amount = gr.Number(label="Operation Amount ($)", value=100.0)
                        with gr.Row():
                            dep_btn = gr.Button("Deposit Cash")
                            with_btn = gr.Button("Withdraw Cash")
                
            # Tab 3: Transaction History
            with gr.TabItem("📜 History"):
                gr.Markdown("### Transaction Log")
                history_table = gr.Dataframe(interactive=False)

    # Event Bindings
    start_btn.click(
        handle_onboarding, 
        inputs=[username_input, initial_fund_input], 
        outputs=[onboarding_box, main_interface, welcome_msg, summary_display, holdings_table, history_table, sell_select]
    )
    
    symbol_select.change(get_live_price, inputs=[symbol_select], outputs=[price_display])
    
    dep_btn.click(handle_deposit, inputs=[fund_amount], outputs=[summary_display, holdings_table, history_table, sell_select])
    with_btn.click(handle_withdraw, inputs=[fund_amount], outputs=[summary_display, holdings_table, history_table, sell_select])
    
    buy_btn.click(handle_buy, inputs=[symbol_select, quantity_input], outputs=[summary_display, holdings_table, history_table, sell_select])
    sell_btn.click(handle_sell, inputs=[sell_select, quantity_input], outputs=[summary_display, holdings_table, history_table, sell_select])

if __name__ == "__main__":
    demo.launch()