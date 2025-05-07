# DatabaseSchema.py connects SQL statements to the SQL server (Connects front end & back end)

import mysql.connector
from ComputerStoreSQLCommands import ComputerStoreSQlConstants
from datetime import date

class SQLConnections:
    def __init__(self, host, user, password):
        self.sql = ComputerStoreSQlConstants()
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        self.DB_NAME = "OnlineComputerStore"
        self.cursor.execute(f"DROP SCHEMA IF EXISTS `{self.DB_NAME}`")
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}")
        self.conn.database = self.DB_NAME

        self.create_tables()
        self.populate_tables()
        self.update_constraints()

    def create_tables(self):
        tables = {
            "CUSTOMERS": self.sql.CUSTOMER_DEF,
            "SILVER_AND_ABOVE": self.sql.SILVER_AND_ABOVE_DEF,
            "CREDIT_CARD": self.sql.CREDIT_CARD_DEF,
            "SHIPPING_ADDRESS": self.sql.SHIPPING_ADDRESS_DEF,
            "TRANSACTION": self.sql.TRANSACTION_DEF,
            "BASKET": self.sql.BASKET_DEF,
            "APPEARS_IN": self.sql.APPEARS_IN_DEF,
            "OFFER_PRODUCT": self.sql.OFFER_PRODUCT_DEF,
            "PRODUCT": self.sql.PRODUCT_DEF,
            "COMPUTER": self.sql.COMPUTER_DEF,
            "PRINTER": self.sql.PRINTER_DEF,
            "LAPTOP": self.sql.LAPTOP_DEF
        }

        for table_name, ddl in tables.items():
            print(f"Creating table {table_name}...")
            self.cursor.execute(ddl)

    def populate_tables(self):
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
    
        for table in tables:
            self.cursor.execute(f"TRUNCATE TABLE `{table}`")
            self.conn.commit()

        test_data = [
            self.sql.CUSTOMER_DATA,
            self.sql.SILVER_AND_ABOVE_DATA, 
            self.sql.SHIPPING_ADDRESS_DATA, 
            self.sql.APPEARS_IN_DATA, 
            self.sql.BASKET_DATA, 
            self.sql.CREDIT_CARD_DATA, 
            self.sql.LAPTOP_DATA, 
            self.sql.PRODUCT_DATA, 
            self.sql.COMPUTER_DATA, 
            self.sql.PRINTER_DATA,
            self.sql.OFFER_PRODUCT_DATA, 
            self.sql.TRANSACTION_DATA
        ]
        
        for data in test_data:
            self.cursor.execute(data)
            self.conn.commit()

    def update_constraints(self):
        constraints = [
            self.sql.SILVER_AND_ABOVE_CONSTRAINTS, 
            self.sql.SHIPPING_ADDRESS_CONSTRAINTS, 
            self.sql.APPEARS_IN_CONSTRAINTS_1, 
            self.sql.APPEARS_IN_CONSTRAINTS_2,
            self.sql.BASKET_CONSTRAINTS, 
            self.sql.CREDIT_CARD_CONSTRAINTS, 
            self.sql.LAPTOP_CONSTAINTS, 
            self.sql.COMPUTER_CONSTRAINTS, 
            self.sql.PRINTER_CONSTRAINTS,
            self.sql.OFFER_PRODUCT_CONSTAINTS, 
            self.sql.TRANSACTION_CONSTRAINTS_1,
            self.sql.TRANSACTION_CONSTRAINTS_2,
            self.sql.TRANSACTION_CONSTRAINTS_3
        ]

        for table in constraints:
            self.cursor.execute(table)
            self.conn.commit()
    
    def statistic_1(self, start_date=None, end_date=None):
        self.cursor.execute(self.sql.STATISTIC_1)
        return self.cursor.fetchall()
    
    def statistic_2(self, start_date=None, end_date=None):
        self.cursor.execute(self.sql.STATISTIC_2)
        return self.cursor.fetchall()
    
    def statistic_3(self, start_date, end_date):
        self.cursor.execute(self.sql.STATISTIC_3, (start_date, end_date))
        return self.cursor.fetchall()
    
    def statistic_4(self, start_date, end_date):
        self.cursor.execute(self.sql.STATISTIC_4, (start_date, end_date))
        return self.cursor.fetchall()
    
    def statistic_5(self, start_date, end_date):
        self.cursor.execute(self.sql.STATISTIC_5, (start_date, end_date))
        return self.cursor.fetchall()
    
    def statistic_6(self, start_date, end_date):
        self.cursor.execute(self.sql.STATISTIC_6, (start_date, end_date))
        return self.cursor.fetchall()

    def _next_id(self, table, column) -> str:
        self.cursor.execute(f"SELECT {column} FROM {table} ORDER BY {column} DESC LIMIT 1")
        row = self.cursor.fetchone()
        if row and row[0] and row[0].isdigit():
            return str(int(row[0]) + 1).zfill(5)
        return "00001"

    # Credit‑Card
    def register_credit_card(self, ccnumber, secnumber, ownername,
                           cctype, billaddress, expdate):
        self.cursor.execute(self.sql.INSERT_CREDIT_CARD,
                            (secnumber, ownername, cctype,
                             billaddress, expdate, ccnumber))
        self.conn.commit()

    def update_credit_card(self, ccnumber, secnumber, ownername,
                           cctype, billaddress, expdate):
        self.cursor.execute(self.sql.UPDATE_CREDIT_CARD,
                            (secnumber, ownername, cctype,
                             billaddress, expdate, ccnumber))
        self.conn.commit()

    def delete_credit_card(self, ccnumber):
        self.cursor.execute(self.sql.DELETE_CREDIT_CARD, (ccnumber,))
        self.conn.commit()

    # Shipping‑Address
    def register_shipping_address(self, cid, saname, recepientname, street,
                                  snumber, city, zipc, state, country):
        self.cursor.execute(self.sql.INSERT_SHIPPING_ADDRESS,
                            (cid, saname, recepientname, street, snumber,
                             city, zipc, state, country))
        self.conn.commit()

    def update_shipping_address(self, cid, saname, recepientname, street,
                                snumber, city, zipc, state, country):
        self.cursor.execute(self.sql.UPDATE_SHIPPING_ADDRESS,
                            (recepientname, street, snumber,
                             city, zipc, state, country, cid, saname))
        self.conn.commit()

    def delete_shipping_address(self, cid, saname):
        self.cursor.execute(self.sql.DELETE_SHIPPING_ADDRESS, (cid, saname))
        self.conn.commit()

    # Product
    def get_product(self, pid):
        self.cursor.execute("SELECT PPRICE, PNAME FROM PRODUCT WHERE PID=%s", (pid,))
        return self.cursor.fetchone()

    # Basket & Transaction
    def create_basket(self, cid) -> str:
        bid = self._next_id("BASKET", "BID")
        self.cursor.execute(self.sql.INSERT_BASKET, (cid, bid))
        self.conn.commit()
        return bid

    def add_to_basket(self, bid, pid, qty, price_sold):
        self.cursor.execute(self.sql.INSERT_APPEARS, (bid, pid, qty, price_sold))
        self.conn.commit()

    def place_order(self, cid, bid, ccnumber, saname):
        self.cursor.execute(self.sql.INSERT_TRANS,
                            (bid, ccnumber, cid, saname, date.today()))
        self.conn.commit()

    def update_order_status(self, bid, status_tag):
        self.cursor.execute(self.sql.UPDATE_TRANS_STATUS, (status_tag, bid))
        self.conn.commit()

    def get_order_status(self, bid):
        self.cursor.execute(self.sql.SELECT_TRANS_STATUS, (bid,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def transaction_history(self, cid, product_name=None,
                             begin=None, end=None):
        extra = []
        params = [cid]
        if product_name:
            extra.append("AND P.PNAME LIKE %s")
            params.append(f"%{product_name}%")
        if begin:
            extra.append("AND T.TDATE >= %s")
            params.append(begin)
        if end:
            extra.append("AND T.TDATE <= %s")
            params.append(end)

        cond = " ".join(extra) if extra else ""
        query = self.sql.SELECT_TRANS_HISTORY.format(extra_conditions=cond)
        self.cursor.execute(query, tuple(params))
        return self.cursor.fetchall()

if __name__ == "__main__":
    schema = SQLConnections(
        host="localhost",
        user="root",
        password="KHlovesburton13!"
    )


