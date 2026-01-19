# Technical Design Document: Trading Simulation Account Management System

**Author:** Engineering Lead  
**Module Name:** `accounts.py`  
**Primary Class:** `Account`  
**Target:** Backend Developer / Full-stack Developer

## 1. Overview
The goal is to provide a robust, single-module backend and UI logic for a trading simulation. The system will handle financial transactions (deposits/withdrawals) and equity trades (buy/sell) with real-time portfolio valuation and a guided onboarding flow. The design follows a Clean Architecture approach within a single file, using `Streamlit` as the UI framework to ensure the "responsive UI" and "interactive" requirements are met in a self-contained manner.

## 2. External Dependencies (Mocked)
### `get_share_price(symbol: str) -> float`
A standalone utility function to simulate real-time market data.
- **Logic:** Returns hardcoded prices for:
    - `COALINDIA`: 450.00
    - `MARICO`: 670.00
    - `ICICIAMC`: 1200.00
- **Fallback:** Returns `0.0` or raises `ValueError` for unknown symbols.

---

## 3. Data Structures
To maintain clean records, the following internal dictionary structures/schemas will be used:
- **Holding:** `{ "symbol": str, "quantity": int, "avg_price": float }`
- **Transaction:** `{ "timestamp": datetime, "type": str, "symbol": str, "quantity": int, "price": float, "amount": float, "status": str }`

---

## 4. Class: `Account`
This class encapsulates the business logic, state management, and validation.

### Attributes:
- `user_name`: str (Set during onboarding)
- `balance`: float (Available cash)
- `initial_deposit`: float (Total cash put into the system)
- `holdings`: Dict[str, Holding] (Keyed by symbol)
- `transactions`: List[Transaction] (History log)

### Methods:

#### `__init__(self)`
- Initializes an empty account with zero balance and empty holdings.

#### `onboard_user(self, name: str, initial_funding: float) -> Tuple[bool, str]`
- Sets the user profile.
- Validates that `initial_funding` > 0.
- Calls `deposit` internally to set up initial state.

#### `deposit(self, amount: float) -> Tuple[bool, str]`
- **Validation:** Amount must be > 0.
- **Logic:** Increases `balance` and `initial_deposit`. Logs a "DEPOSIT" transaction.
- **Return:** `(True, "Success message")` or `(False, "Error message")`.

#### `withdraw(self, amount: float) -> Tuple[bool, str]`
- **Validation:** Amount must be > 0 and <= current `balance`.
- **Logic:** Decreases `balance`. Logs a "WITHDRAWAL" transaction.
- **Return:** `(True, "Success message")` or `(False, "Error message")`.

#### `buy_share(self, symbol: str, quantity: int) -> Tuple[bool, str]`
- **Validation:** 
    - Quantity > 0.
    - Symbol must be valid.
    - Total cost (`price * quantity`) <= `balance`.
- **Logic:** 
    - Fetches current price via `get_share_price`.
    - Deducts cost from `balance`.
    - Updates/Creates the holding entry (calculating new average price).
    - Logs a "BUY" transaction.
- **Return:** Result tuple with status message.

#### `sell_share(self, symbol: str, quantity: int) -> Tuple[bool, str]`
- **Validation:** 
    - Quantity > 0.
    - User must own the symbol.
    - User must have `holdings[symbol].quantity >= quantity`.
- **Logic:** 
    - Fetches current price.
    - Adds proceeds to `balance`.
    - Decrements quantity in holdings (removes key if 0).
    - Logs a "SELL" transaction.
- **Return:** Result tuple with status message.

#### `get_portfolio_summary(self) -> dict`
- **Logic:** 
    - Calculates current market value of all holdings.
    - Calculates `total_value` (balance + market value).
    - Calculates `total_pl` (total_value - initial_deposit).
- **Return:** Dictionary containing `balance`, `market_value`, `total_value`, `total_pl`, and `pl_percentage`.

---

## 5. UI Logic (Streamlit implementation inside `accounts.py`)
To make the module "ready to be tested," the bottom of the script will contain a `main()` function using Streamlit.

### UI Components:
1.  **Sidebar/Navigation:** 
    - Dashboard, Trade, History, Account Settings.
2.  **Onboarding Wizard:**
    - Use `st.session_state` to check if a user is initialized. If not, show a multi-step form (Name -> Initial Funding).
3.  **Dashboard (Real-time Updates):**
    - Metric cards for Total Value, Cash Balance, and Total P/L (colored green/red).
    - A dynamic table showing current holdings (Symbol, Qty, Avg Price, Current Price, Current Value, P/L).
4.  **Trade Panel:**
    - Tabs for Buy and Sell.
    - Selectbox for Symbols (Coal India, Marico, ICICI AMC).
    - Number input for Quantity.
    - Instant validation: Display `st.error` if the "Total Cost" exceeds balance or "Quantity" exceeds holdings.
5.  **Transaction History:**
    - A sortable `st.dataframe` showing the `transactions` list.
6.  **Notifications:**
    - Use `st.toast` or `st.success` for trade confirmations.

---

## 6. Execution Flow
1. User runs `streamlit run accounts.py`.
2. `Account` object is stored in `st.session_state.account` to persist data between reruns.
3. If `account.user_name` is empty, the onboarding UI is rendered.
4. Once onboarded, the main dashboard becomes accessible.
5. Every action (Buy/Sell/Deposit) triggers a state update and immediate UI refresh.

---

## 7. Error Handling & Validation
- **Insufficient Funds:** Block "Buy" and "Withdraw" buttons or show error on click.
- **Negative Inputs:** Force `min_value=0.01` on all numeric inputs.
- **Missing Holdings:** "Sell" tab should only populate symbols currently in the `holdings` dictionary.