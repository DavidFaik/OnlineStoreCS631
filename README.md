# Online Computer Store (MySQL + Python/wxPython)

A desktop application that demonstrates an online computer store. It provisions a MySQL schema with sample data, exposes a wxPython GUI for core e‑commerce operations (customer registration, addresses, credit cards, basket/checkout), and includes six sales/statistics reports.

Note: On startup the app drops and recreates the demo database, then seeds data.

## Features
- Customer registration and profile management
- Credit card add/update/delete tied to customers
- Shipping address add/update/delete per customer
- Basket creation, add items, and order placement
- Order status updates and transaction history
- Six sales/statistics reports (some with date range filters)

## Tech Stack
- Python 3.8+ 
- MySQL Server (8.0+ recommended)
- wxPython (GUI)
- mysql-connector-python (DB driver)

## Repository Structure
- `ComputerStoreMenuApplication.py` — wxPython GUI and application entry point
- `DatabaseSchema.py` — MySQL connection, schema bootstrap, seed data, and DB operations
- `ComputerStoreSQLCommands.py` — All SQL DDL/DML and reporting queries as constants

## Prerequisites
- Python 3.8+ and `pip`
- MySQL Server running locally on `localhost:3306`
- A MySQL user with privileges to CREATE/DROP databases and tables (root works for local demos)

## Install
Optionally create and activate a virtual environment, then install dependencies:

```
pip install mysql-connector-python wxPython
```

If `wxPython` installation fails on your OS, see the official wheels and OS prerequisites: https://wxpython.org/pages/downloads/

## Database Warning (Data Reset)
This project intentionally resets the demo database during startup:
- Drops schema if it exists: `DatabaseSchema.py:17`
- Recreates and seeds tables: `DatabaseSchema.py:21`, `DatabaseSchema.py:22`, `DatabaseSchema.py:23`

The database name is `OnlineComputerStore`.

## Configure Database Credentials
The app currently uses hard-coded credentials that you should change before running:
- GUI app initialization: `ComputerStoreMenuApplication.py:13`
- Standalone schema runner (optional): `DatabaseSchema.py:253`–`DatabaseSchema.py:257`

Update `host`, `user`, and `password` to match your local MySQL setup. Example:

```python
# ComputerStoreMenuApplication.py:13
self.db = SQLConnections(host="localhost", user="root", password="<your_password>")
```

Tip: For a more secure setup, refactor to read from environment variables or a config file.

### Creating a dedicated MySQL user (optional)
From the MySQL shell:

```
CREATE USER 'storeuser'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON *.* TO 'storeuser'@'localhost';
FLUSH PRIVILEGES;
```

The user must be able to CREATE/DROP the `OnlineComputerStore` database for demo resets.

## Run
Launch the GUI:

```
python ComputerStoreMenuApplication.py
```

On first launch, the app will create the `OnlineComputerStore` schema, create tables, insert sample data, and apply constraints. Subsequent launches will repeat the reset as written.

## Using the App
The main window has three sections:

1) Registration + Management
- Register a new customer (first/last name, email, address, phone)
- Manage credit cards (add/update/delete)
- Manage shipping addresses (add/update/delete)

2) Online Sales
- Create a basket for a customer
- Add products to basket (quantity and selling price)
- Place an order by selecting credit card and shipping address
- Update and view order status

3) Sale Statistics
Generate six reports. Date filters require `YYYY-MM-DD` format when applicable.
- Report 1: Total charged per credit card — columns: `CCNUMBER`, `TOTAL_CHARGED`
- Report 2: Top customers by spend — columns: `CID`, `FNAME`, `LNAME`, `TOTAL_SPENT`
- Report 3: Units sold per product in date range — columns: `PID`, `PNAME`, `TOTAL_SOLD`
- Report 4: Unique customers per product in date range — columns: `PID`, `PNAME`, `NUM_CUSTOMERS`
- Report 5: Max basket total per credit card in date range — columns: `CCNUMBER`, `MAX_BASKET_TOTAL`
- Report 6: Average selling price by product type in date range — columns: `PTYPE`, `AVG_SELLING_PRICE`

## Data Model (Summary)
Tables and key relationships (see `ComputerStoreSQLCommands.py` for full DDL):
- `CUSTOMER(CID, ...)` — core customer table
- `SILVER_AND_ABOVE(CID, CREDITLINE)` — FK to `CUSTOMER`
- `CREDIT_CARD(CCNUMBER, ..., STOREDCARDCID)` — FK to `CUSTOMER(CID)`
- `SHIPPING_ADDRESS(CID, SANAME, ...)` — FK to `CUSTOMER(CID)`
- `BASKET(BID, CID)` — customer baskets
- `APPEARS_IN(BID, PID, QUANTITY, PRICESOLD)` — basket line items
- `PRODUCT(PID, PTYPE, PNAME, PPRICE, ...)` — catalog items
- `COMPUTER/PRINTER/LAPTOP(PID, ...)` — product-type specific details
- `TRANSACTION(BID, CCNUMBER, CID, SANAME, TDATE, TTAG)` — orders (status `TTAG`: C=Confirmed, S=Shipped, E=Enroute, D=Delivered, L=Lost)

## Troubleshooting
- MySQL connection errors: Verify server is running, host/port, and credentials. Ensure the user can CREATE/DROP databases.
- `wx` import error: Install `wxPython` and ensure OS prerequisites. Try `pip install -U pip setuptools wheel` then reinstall.
- Foreign key errors on updates: The app surfaces friendly messages for common FK issues (e.g., invalid customer/credit card/shipping address references).

## Notes
- Credentials are hard-coded for convenience; prefer environment variables or config for real projects.
- The schema reset is for demo consistency. Remove or comment out the drop/seed calls in `DatabaseSchema.py` if you want persistence.
