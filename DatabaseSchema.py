import mysql.connector
from ComputerStoreSQLCommands import ComputerStoreSQlConstants

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
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}")
        self.conn.database = self.DB_NAME
        self.create_tables()
        #self.populate_tables()

    def create_tables(self):
        tables = {
            "CUSTOMERS": self.sql.CUSTOMER_DEF,
            "SILVER_AND_ABOVE": self.sql.SILVER_AND_ABOVE_DEF,
            "CREDIT_CARD": self.sql.CREDIT_CARD_DEF,
            "SHIPPING_ADDRESS": self.sql.SHIPPING_ADDRESS_DEF,
            "TRANSACTIONS": self.sql.TRANSACTIONS_DEF,
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
        test_data = [self.sql.CUSTOMER_DATA, self.sql.CREDIT_CARD_DATA]
        for data in test_data:
            self.cursor.execute(data)
            self.conn.commit()

    def update_constraints(self):
        constraints = [self.sql.SILVER_AND_ABOVE_CONSTRAINTS, self.sql.SHIPPING_ADDRESS_CONSTRAINTS, self.sql.APPEARS_IN_CONSTRAINTS, 
                       self.sql.BASKET_CONSTRAINTS, self.sql.CREDIT_CARD_CONSTRAINTS, self.sql.LAPTOP_CONSTAINTS, 
                       self.sql.PRODUCT_CONSTRAINTS, self.sql.COMPUTER_CONSTRAINTS, self.sql.PRINTER_CONSTRAINTS,
                       self.sql.OFFER_PRODUCT_CONSTAINTS, self.sql.TRANSACTION_CONSTRAINTS]
        for table in constraints:
            self.cursor.execute(table)
            self.conn.commit()

    def register_customer(self, cid, fname, lname, email, address, phone):
        insert_customer = """
                INSERT INTO CUSTOMER (CID, FNAME, LNAME, EMAIL, ADDRESS, PHONE)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
        self.cursor.execute(insert_customer, (cid, fname, lname, email, address, phone))
        self.conn.commit()
    
    def register_credit_card(self, ccnumber, secnumber, ownername, cctype, billaddress, expdate, storedcardcid):
        ##How will the ownername and storedcardcid be stored so they don't have to input that data?
        insert_credit_card = """
                INSERT INTO CREDIT_CARD (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        self.cursor.execute(insert_credit_card, (ccnumber, secnumber, ownername, cctype, billaddress, expdate, storedcardcid))
        self.conn.commit()
    
    def register_shipping_address(self):
        pass
        #insert_shipping_address = """
                #INSERT INTO SHIPPING_ADDRESS (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID)
                #VALUES (%s, %s, %s, %s, %s, %s, %s)
            #"""
        #self.cursor.execute(insert_shipping_address, (ccnumber, secnumber, ownername, cctype, billaddress, expdate, storedcardcid))
        #self.conn.commit()
    
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

if __name__ == "__main__":
    schema = SQLConnections(
        host="localhost",
        user="root",
        password="KHlovesburton13!"
    )


