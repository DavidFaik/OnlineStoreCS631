##Constaints for SQL Table Definitions
##Note: must populate tables first with basic data than add foregin keys to avoid referencing problems

class ComputerStoreSQlConstants:
    """
    A class containing SQL constants for the Computer Store application.
    """
    SILVER_AND_ABOVE_DEF = """CREATE TABLE IF NOT EXIST SILVER_AND_ABOVE
                    (CID CHAR(10) NOT NULL,
                    CREDITLINE INT
                    PRIMARY KEY (CID)"""

    CUSTOMER_DEF = """CREATE TABLE IF NOT EXIST CUSTOMER
            (CID CHAR(10) NOT NULL,
            FNAME VARCHAR(15) NOT NULL,
            LNAME VARCHAR(15) NOT NULL,
            EMAIL VARCHAR(30),
            ADDRESS VARCHAR(30),
            PHONE CHAR(10),
            STATUS CHAR NOT NULL DEFAULT'R',
            PRIMARY KEY (CID),
            UNIQUE (EMAIL))"""

    CREDIT_CARD_DEF = """CREATE TABLE IF NOT EXIST CREDIT_CARD
                (CCNUMBER CHAR(16) NOT NULL,
                SECNUMBER CHAR(3) NOT NULL,
                OWNERNAME VARCHAR(15) NOT NULL,
                CCType VARCHAR(10) NOT NULL,
                BILLADDRESS VARCHAR(30),
                EXPDATE DATE,
                STOREDCARDCID CHAR(10),
                PRIMARY KEY(CCNUMBER))"""

    SHIPPING_ADDRESS_DEF = """CREATE TABLE IF NOT EXIST SHIPPING_ADDRESS
                    (CID CHAR(10) NOT NULL,
                    SANAME VARCHAR(30) NOT NULL,
                    RECEPIENTNAME VARCHAR(30),
                    STREET VARCHAR(10),
                    SNUMBER INT,
                    CITY VARCHAR(15),
                    ZIP CHAR(5),
                    STATE CHAR(2),
                    COUNTRY VARCHAR(15))"""

    TRANSACTIONS_DEF = """CREATE TABLE IF NOT EXIST TRANSACTIONS
                (BID CHAR(10) NOT NULL,
                CCNUMBER CHAR(16) NOT NULL,
                CID CHAR(10) NOT NULL,
                SANAME VARCHAR(30) NOT NULL,
                TDATE DATE,
                TTAG CHAR DEFAULT'C')""" ##TTAG options assume C=confirmed, S=Shipped, E=Enroute, D=Delivered, L=Lost

    BASKET_DEF = """CREATE TABLE IF NOT EXIST BASKET
            (CID CHAR(10) NOT NULL,
            BID CHAR(10) NOT NULL)"""

    APPEARS_IN_DEF = """CREATE TABLE IF NOT EXIST APPEARS_IN
                (BID CHAR(10) NOT NULL,
                PID CHAR(10) NOT NULL,
                QUANTITY INT,
                PRICESOLD DECIMAL(10,2))"""

    OFFER_PRODUCT_DEF = """CREATE TABLE IF NOT EXIST OFFER_PRODUCT
                    (PID CHAR(10) NOT NULL,
                    OFFERPRICE DECIMAL(10,2))"""

    PRODUCT_DEF = """CREATE TABLE IF NOT EXIST PRODUCT
                (PID CHAR(10) NOT NULL,
                PType CHAR, 
                PNAME VARCHAR(15),
                PPRICE DECIMAL(10,2),
                DESCRIPTION VARCHAR(15),
                PQUANTITY INT)""" ##PType options assume C=Computer P=Printer L=Laptop M=Miscelenous

    COMPUTER_DEF = """CREATE TABLE IF NOT EXIST COMPUTER
                CREATE TABLE COMPUTER
                (PID CHAR(10) NOT NULL,
                CPUTYPE VARCHAR(10))"""

    PRINTER_DEF = """CREATE TABLE IF NOT EXIST PRINTER
                (PID CHAR(10) NOT NULL,
                PRINTER TYPE VARCHAR(10),
                RESOLUTION VARCHAR(10))"""

    LAPTOP_DEF = """CREATE TABLE IF NOT EXIST LAPTOP
                (PID CHAR(10) NOT NULL,
                BTYPE VARCHAR(15),
                WEIGHT INT)"""
    
    SILVER_AND_ABOVE_CONSTRAINTS = """ALTER TABLE SILVER_AND_ABOVE
                                    ADD CONSTRAINT CUSTOMERSILVERFK FOREIGN KEY CID REFERENCES CUSTOMER
                                    ON DELETE CASCADE ON UPDATE CASCADE"""
    
    CREDIT_CARD_CONSTRAINTS = """ALTER TABLE CREDIT_CARD
                                ADD CONSTRAINT STOREDCARDRFK FOREIGN KEY STOREDCARDCID REFERENCES CUSTOMER
                                ON DELETE CASCADE ON UPDATE CASCADE"""
    
    SHIPPING_ADDRESS_CONSTRAINTS = """ALTER TABLE SHIPPING_ADDRESS
                                ADD CONSTRAINT CIDSHIPPINGFK FOREIGN KEY CID REFERENCES SILVER_AND_ABOVE
                                ON DELETE CASCADE ON UPDATE CASCADE"""

    TRANSACTION_CONSTRAINTS = ["""ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONCCFK FOREIGN KEY CCNUMBER REFERENCES CREDIT_CARD
                                ON DELETE CASCADE ON UPDATE CASCADE""",
                                """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONSANAMECIDFK FOREIGN KEY (CID,SANAME) REFERENCES SHIPPING_ADDRESS
                                ON DELETE CASCADE ON UPDATE CASCADE""",
                                """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONBIDFK FOREIGN KEY BID REFERENCES BASKET
                                ON DELETE CASCADE ON UPDATE CASCADE"""]
    
    BASKET_CONSTRAINTS = """ALTER TABLE BASKET
                        ADD CONSTRAINT BASKETCIDFK FOREIGN KEY CID REFERENCES CUSTOMER
                        ON DELETE CASCADE ON UPDATE CASCADE"""

    APPEARS_IN_CONSTRAINTS = ["""ALTER TABLE APPEARS_IN
                        ADD CONSTRAINT APPEARSBIDFK FOREIGN KEY BID REFERENCES BASKET
                        ON DELETE CASCADE ON UPDATE CASCADE""",
                        """ALTER TABLE APPEARS_IN
                        ADD CONSTRAINT APPEARSINPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE"""]

    OFFER_PRODUCT_CONSTAINTS = """ALTER TABLE OFFER_PRODUCT
                        ADD CONSTRAINT OFFERPRODUCTPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE"""

    PRODUCT_CONSTRAINTS = """ALTER TABLE PRODUCT
                        ADD CONSTRAINT LAPTOPPIDFK FOREIGN KEY PID REFERENCES COMPUTER
                        ON DELETE CASCADE ON UPDATE CASCADE"""

    COMPUTER_CONSTRAINTS = """ALTER TABLE COMPUTER
                        ADD CONSTRAINT COMPUTERPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE"""

    PRINTER_CONSTRAINTS = """ALTER TABLE PRINTER
                        ADD CONSTRAINT PRINTERPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE"""

    LAPTOP_CONSTAINTS = """ALTER TABLE LAPTOP
                        ADD CONSTRAINT LAPTOPPIDFK FOREIGN KEY PID REFERENCES COMPUTER
                        ON DELETE CASCADE ON UPDATE CASCADE"""
    
    
    