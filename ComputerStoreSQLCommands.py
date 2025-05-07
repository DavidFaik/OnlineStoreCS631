##Constaints for SQL Table Definitions
##Note: must populate tables first with basic data than add foregin keys to avoid referencing problems

class ComputerStoreSQlConstants:
    """
    A class containing SQL constants for the Computer Store application.
    """
    SILVER_AND_ABOVE_DEF = """CREATE TABLE IF NOT EXISTS SILVER_AND_ABOVE
                    (CID CHAR(5) NOT NULL,
                    CREDITLINE INT);"""

    CUSTOMER_DEF = """CREATE TABLE IF NOT EXISTS CUSTOMER
            (CID CHAR(5) NOT NULL, 
            FNAME VARCHAR(15) NOT NULL,
            LNAME VARCHAR(15) NOT NULL,
            EMAIL VARCHAR(30),
            ADDRESS VARCHAR(50),
            PHONE CHAR(10),
            STATUS CHAR DEFAULT'R',
            PRIMARY KEY(CID));""" #Status R=Regular, S=Silver, G=Gold, & P=Platinum
    #CID, PID, & BID are 5 digit strings

    CREDIT_CARD_DEF = """CREATE TABLE IF NOT EXISTS CREDIT_CARD
                (CCNUMBER CHAR(16) NOT NULL,
                SECNUMBER CHAR(3) NOT NULL,
                OWNERNAME VARCHAR(15) NOT NULL,
                CCType VARCHAR(10) NOT NULL,
                BILLADDRESS VARCHAR(100),
                EXPDATE CHAR(5),
                STOREDCARDCID CHAR(5),
                PRIMARY KEY(CCNUMBER));"""

    SHIPPING_ADDRESS_DEF = """CREATE TABLE IF NOT EXISTS SHIPPING_ADDRESS
                    (CID CHAR(5) NOT NULL,
                    SANAME VARCHAR(50) NOT NULL,
                    RECEPIENTNAME VARCHAR(30),
                    STREET VARCHAR(15),
                    SNUMBER INT,
                    CITY VARCHAR(20),
                    ZIP CHAR(5),
                    STATE CHAR(2),
                    COUNTRY VARCHAR(15));"""

    TRANSACTIONS_DEF = """CREATE TABLE IF NOT EXISTS TRANSACTIONS
                (BID CHAR(5) NOT NULL,
                CCNUMBER CHAR(16) NOT NULL,
                CID CHAR(5) NOT NULL,
                SANAME VARCHAR(30) NOT NULL,
                TDATE DATE,
                TTAG CHAR DEFAULT'C');""" ##TTAG options assume C=confirmed, S=Shipped, E=Enroute, D=Delivered, L=Lost

    BASKET_DEF = """CREATE TABLE IF NOT EXISTS BASKET
            (CID CHAR(5) NOT NULL,
            BID CHAR(5) NOT NULL);"""

    APPEARS_IN_DEF = """CREATE TABLE IF NOT EXISTS APPEARS_IN
                (BID CHAR(5) NOT NULL,
                PID CHAR(5) NOT NULL,
                QUANTITY INT,
                PRICESOLD DECIMAL(10,2));"""

    OFFER_PRODUCT_DEF = """CREATE TABLE IF NOT EXISTS OFFER_PRODUCT
                    (PID CHAR(5) NOT NULL,
                    OFFERPRICE DECIMAL(10,2));"""

    PRODUCT_DEF = """CREATE TABLE IF NOT EXISTS PRODUCT
                (PID CHAR(5) NOT NULL,
                PType CHAR, 
                PNAME VARCHAR(15),
                PPRICE DECIMAL(10,2),
                DESCRIPTION VARCHAR(15),
                PQUANTITY INT);""" ##PType options assume C=Computer P=Printer L=Laptop M=Miscelenous

    COMPUTER_DEF = """CREATE TABLE IF NOT EXISTS COMPUTER
                (PID CHAR(5) NOT NULL,
                CPUTYPE VARCHAR(10));"""

    PRINTER_DEF = """CREATE TABLE IF NOT EXISTS PRINTER
                (PID CHAR(5) NOT NULL,
                PRINTERTYPE VARCHAR(10),
                RESOLUTION VARCHAR(10));"""

    LAPTOP_DEF = """CREATE TABLE IF NOT EXISTS LAPTOP
                (PID CHAR(5) NOT NULL,
                BTYPE VARCHAR(15),
                WEIGHT INT);"""
    
    SILVER_AND_ABOVE_CONSTRAINTS = """ALTER TABLE SILVER_AND_ABOVE
                                    ADD CONSTRAINT CUSTOMERSILVERFK FOREIGN KEY CID REFERENCES CUSTOMER
                                    ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    CREDIT_CARD_CONSTRAINTS = """ALTER TABLE CREDIT_CARD
                                ADD CONSTRAINT STOREDCARDRFK FOREIGN KEY STOREDCARDCID REFERENCES CUSTOMER
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    SHIPPING_ADDRESS_CONSTRAINTS = """ALTER TABLE SHIPPING_ADDRESS
                                ADD CONSTRAINT CIDSHIPPINGFK FOREIGN KEY CID REFERENCES SILVER_AND_ABOVE
                                ON DELETE CASCADE ON UPDATE CASCADE;"""

    TRANSACTION_CONSTRAINTS = ["""ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONCCFK FOREIGN KEY CCNUMBER REFERENCES CREDIT_CARD
                                ON DELETE CASCADE ON UPDATE CASCADE;""",
                                """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONSANAMECIDFK FOREIGN KEY (CID,SANAME) REFERENCES SHIPPING_ADDRESS
                                ON DELETE CASCADE ON UPDATE CASCADE;""",
                                """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONBIDFK FOREIGN KEY BID REFERENCES BASKET
                                ON DELETE CASCADE ON UPDATE CASCADE;"""]
    
    BASKET_CONSTRAINTS = """ALTER TABLE BASKET
                        ADD CONSTRAINT BASKETCIDFK FOREIGN KEY CID REFERENCES CUSTOMER
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    APPEARS_IN_CONSTRAINTS = ["""ALTER TABLE APPEARS_IN
                        ADD CONSTRAINT APPEARSBIDFK FOREIGN KEY BID REFERENCES BASKET
                        ON DELETE CASCADE ON UPDATE CASCADE;""",
                        """ALTER TABLE APPEARS_IN
                        ADD CONSTRAINT APPEARSINPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE;"""]

    OFFER_PRODUCT_CONSTAINTS = """ALTER TABLE OFFER_PRODUCT
                        ADD CONSTRAINT OFFERPRODUCTPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    PRODUCT_CONSTRAINTS = """ALTER TABLE PRODUCT
                        ADD CONSTRAINT LAPTOPPIDFK FOREIGN KEY PID REFERENCES COMPUTER
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    COMPUTER_CONSTRAINTS = """ALTER TABLE COMPUTER
                        ADD CONSTRAINT COMPUTERPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    PRINTER_CONSTRAINTS = """ALTER TABLE PRINTER
                        ADD CONSTRAINT PRINTERPIDFK FOREIGN KEY PID REFERENCES PRODUCT
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    LAPTOP_CONSTAINTS = """ALTER TABLE LAPTOP
                        ADD CONSTRAINT LAPTOPPIDFK FOREIGN KEY PID REFERENCES COMPUTER
                        ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    CUSTOMER_DATA = """INSERT INTO CUSTOMER (CID, FNAME, LNAME, EMAIL, ADDRESS, PHONE, STATUS)
                    VALUES
                    ('00001', 'Bob', 'Edwards', 'bobedwards123@gmail.com', '13 Pleasant Street, Newark NJ, 07103', '9783022229', 'R'),
                    ('00002', 'Dylan', 'Clark', 'clark3246@gmail.com', '22 Roosevelt Ave, Princeton NJ, 01827', '9788662409', 'R'),
                    ('00003', 'Riley', 'Mucci', 'rileyam@icloud.com', '25 Sycamore Street, Boston MA, 03452', '1234567890', 'S'),
                    ('00004', 'Kimberly', 'Harding', 'harding7134@gmail.com', '202 Warren Street, Newark NJ, 07103', '7653458903', 'S'),
                    ('00005', 'Richard', 'Morena', 'ram6789@icloud.com', '100 Lock Street, Newark NJ, 07103', '9784923765', 'G');"""
    
    CREDIT_CARD_DATA = """INSERT INTO CREDIT_CARD (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID)
                    VALUES
                    ('123456789123456', '827', 'Bob Edwards', 'Mastercard', '13 Pleasant Street, Newark NJ, 07103', '04/28', 00001),
                    ('122256789993456', '437', 'Dylan Clark', 'Discover', '22 Roosevelt Ave, Princeton NJ, 01827', '08/29', 00002),
                    ('110256780993336', '789', 'Riley Mucci', 'Mastercard', '25 Sycamore Street, Boston MA, 03452', '07/35', 00003),
                    ('11025670093336', '789', 'Kimberly Harding', 'Mastercard', '202 Warren Street, Newark NJ, 07103', '03/28', 00004),
                    ('34567809999999', '123', 'Richard Morena', 'Mastercard', '100 Lock Street, Newark NJ, 07103', '09/31', 00005);"""
    
    STATISTIC_1 = """SELECT CCNUMBER, SUM(AI.QUANTITY*AI.PRICE) AS TOTAL_CHARGED
                    FROM TRANSACTIONS T, APPEARS_IN AI
                    WHERE T.BID = AI.BID
                    GROUP BY CCNUMBER"""
    
    STATISTIC_2 = """SELECT C.CID, C.FNAME, C.LNAME, SUM(AI.QUANTITY*AI.PRICESOLD) AS TOTAL_SPENT
                    FROM CUSTOMER C, TRANSACTIONS T, APPEARS_IN AI
                    WHERE C.CID =T.CID AND T.BID = AI.BID
                    GROUP BY C.CID, C.FNAME, C.LNAME
                    ORDER BY TOTAL_SPENT DESC"""
    
    STATISTIC_3 = 