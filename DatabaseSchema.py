import mysql.connector
from ComputerStoreSQLCommands import ComputerStoreSQlConstants

class DatabaseSchema:
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
        self.populate_tables()

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
        test_data = [self.sql.CUSTOMER_DATA]
        for data in test_data:
            print("Populating Tables...")
            self.cursor.execute(data)
            self.conn.commit()

    def update_constraints(self):
        pass

if __name__ == "__main__":
    schema = DatabaseSchema(
        host="localhost",
        user="root",
        password="KHlovesburton13!"
    )


