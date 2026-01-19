import streamlit as st
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
            # Update average price: (existing total cost + new cost) / new total quantity
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
            "price": price,
            "amount": amount,
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

def main():
    st.set_page_config(page_title="Trading Sim Account Management", layout="wide", initial_sidebar_state="expanded")

    # Persistent State Management
    if 'account' not in st.session_state:
        st.session_state.account = Account()
    
    acc = st.session_state.account

    # 1. Onboarding Flow
    if not acc.user_name:
        st.title("🚀 Welcome to TradeSim")
        st.subheader("Guided User Onboarding")
        st.write("To start your trading simulation, please provide your details and initial funding.")
        
        with st.container():
            name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
            funding = st.number_input("Initial Deposit Amount ($)", min_value=1.0, value=5000.0, step=100.0)
            
            if st.button("Initialize Account"):
                success, msg = acc.onboard_user(name, funding)
                if success:
                    st.success(f"Account created successfully for {name}!")
                    st.rerun()
                else:
                    st.error(msg)
        return

    # 2. Main Navigation Sidebar
    st.sidebar.title(f"👋 {acc.user_name}")
    st.sidebar.divider()
    nav = st.sidebar.radio("Navigation", ["Dashboard", "Trade Panel", "History", "Settings"])

    summary = acc.get_portfolio_summary()

    if nav == "Dashboard":
        st.title("Portfolio Overview")
        
        # Real-time balance and P/L metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Portfolio Value", f"${summary['total_value']:,.2f}")
        m2.metric("Cash Balance", f"${summary['balance']:,.2f}")
        
        pl_label = "Total Profit/Loss"
        m3.metric(pl_label, f"${summary['total_pl']:,.2f}", f"{summary['pl_percent']:.2f}%")
        m4.metric("Market Value", f"${summary['market_value']:,.2f}")

        # Holdings Display
        st.subheader("Current Holdings")
        if acc.holdings:
            holding_list = []
            for symbol, data in acc.holdings.items():
                cp = get_share_price(symbol)
                mv = cp * data["quantity"]
                cost_basis = data["avg_price"] * data["quantity"]
                h_pl = mv - cost_basis
                holding_list.append({
                    "Symbol": symbol,
                    "Quantity": data["quantity"],
                    "Avg Buy Price": f"${data['avg_price']:,.2f}",
                    "Current Price": f"${cp:,.2f}",
                    "Market Value": f"${mv:,.2f}",
                    "P/L": f"${h_pl:,.2f}"
                })
            st.table(holding_list)
        else:
            st.info("Your portfolio is currently empty. Head to the Trade Panel to buy your first shares!")

    elif nav == "Trade Panel":
        st.title("Interactive Trade Panel")
        
        t1, t2, t3 = st.tabs(["Buy Shares", "Sell Shares", "Fund Operations"])
        
        # Available Symbols for Trading
        available_symbols = ["COALINDIA", "MARICO", "ICICIAMC"]
        
        with t1:
            st.subheader("Purchase Equity")
            col_a, col_b = st.columns(2)
            with col_a:
                buy_sym = st.selectbox("Select Symbol", available_symbols)
                buy_qty = st.number_input("Purchase Quantity", min_value=1, step=1)
            
            current_price = get_share_price(buy_sym)
            total_cost = current_price * buy_qty
            
            with col_b:
                st.write(f"**Current Price:** ${current_price:,.2f}")
                st.write(f"**Total Cost:** ${total_cost:,.2f}")
                if total_cost > acc.balance:
                    st.warning("Insufficient funds for this quantity.")
            
            if st.button("Execute Buy Order"):
                success, msg = acc.buy_share(buy_sym, buy_qty)
                if success:
                    st.success(msg)
                    st.balloons()
                else:
                    st.error(msg)

        with t2:
            st.subheader("Liquidate Holdings")
            if not acc.holdings:
                st.warning("You do not have any holdings to sell.")
            else:
                col_c, col_d = st.columns(2)
                with col_c:
                    sell_sym = st.selectbox("Select Holding", list(acc.holdings.keys()))
                    max_sell = acc.holdings[sell_sym]["quantity"]
                    sell_qty = st.number_input("Sell Quantity", min_value=1, max_value=max_sell, step=1)
                
                sell_price = get_share_price(sell_sym)
                total_credit = sell_price * sell_qty
                
                with col_d:
                    st.write(f"**Market Price:** ${sell_price:,.2f}")
                    st.write(f"**Proceeds:** ${total_credit:,.2f}")
                
                if st.button("Execute Sell Order"):
                    success, msg = acc.sell_share(sell_sym, sell_qty)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

        with t3:
            st.subheader("Balance Management")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.write("**Deposit Funds**")
                d_amt = st.number_input("Amount to Deposit", min_value=0.0, step=100.0, key="dep")
                if st.button("Confirm Deposit"):
                    success, msg = acc.deposit(d_amt)
                    if success: st.toast(msg)
                    else: st.error(msg)
            
            with f_col2:
                st.write("**Withdraw Funds**")
                w_amt = st.number_input("Amount to Withdraw", min_value=0.0, step=100.0, key="with")
                if st.button("Confirm Withdrawal"):
                    success, msg = acc.withdraw(w_amt)
                    if success: st.toast(msg)
                    else: st.error(msg)

    elif nav == "History":
        st.title("Transaction History")
        if not acc.transactions:
            st.info("No transaction records found.")
        else:
            df = pd.DataFrame(acc.transactions)
            # Styling for positive/negative amounts
            st.dataframe(df.sort_index(ascending=False), use_container_width=True)

    elif nav == "Settings":
        st.title("Account Settings")
        st.write(f"**Account Holder:** {acc.user_name}")
        st.write(f"**Initial Investment:** ${acc.initial_deposit:,.2f}")
        st.divider()
        if st.button("Reset Simulation"):
            st.session_state.account = Account()
            st.rerun()

if __name__ == "__main__":
    main()