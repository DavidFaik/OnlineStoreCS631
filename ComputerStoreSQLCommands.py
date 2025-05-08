## ComputerStoreSQLCommands.py for all SQL statements
##Note: must populate tables first with basic data than add foregin keys to avoid referencing problems

class ComputerStoreSQlConstants:
    """
    A class containing SQL constants for the Computer Store application. 
    """

    """
    1) SQL Table Definitons
    """
    SILVER_AND_ABOVE_DEF = """CREATE TABLE IF NOT EXISTS SILVER_AND_ABOVE
                    (CID CHAR(5) NOT NULL,
                    CREDITLINE INT,
                    PRIMARY KEY(CID));"""

    CUSTOMER_DEF = """CREATE TABLE IF NOT EXISTS CUSTOMER
            (CID CHAR(5) NOT NULL, 
            FNAME VARCHAR(15) NOT NULL,
            LNAME VARCHAR(15) NOT NULL,
            EMAIL VARCHAR(30) UNIQUE,
            ADDRESS VARCHAR(100),
            PHONE CHAR(10),
            STATUS CHAR DEFAULT'R',
            PRIMARY KEY(CID));""" #Status R=Regular, S=Silver, G=Gold, & P=Platinum
    #CID, PID, & BID are 5 digit strings

    CREDIT_CARD_DEF = """CREATE TABLE IF NOT EXISTS CREDIT_CARD
                (CCNUMBER CHAR(16) NOT NULL,
                SECNUMBER CHAR(3) NOT NULL,
                OWNERNAME VARCHAR(30) NOT NULL,
                CCType VARCHAR(10) NOT NULL,
                BILLADDRESS VARCHAR(100),
                EXPDATE CHAR(5),
                STOREDCARDCID CHAR(5),
                PRIMARY KEY(CCNUMBER));"""

    SHIPPING_ADDRESS_DEF = """CREATE TABLE IF NOT EXISTS SHIPPING_ADDRESS
                    (CID CHAR(5) NOT NULL,
                    SANAME VARCHAR(50) NOT NULL,
                    RECEPIENTNAME VARCHAR(30) NOT NULL,
                    STREET VARCHAR(15),
                    SNUMBER INT,
                    CITY VARCHAR(20),
                    ZIP CHAR(5),
                    STATE CHAR(2),
                    COUNTRY VARCHAR(15),
                    PRIMARY KEY(CID, SANAME));"""

    TRANSACTION_DEF = """CREATE TABLE IF NOT EXISTS TRANSACTION
                (BID CHAR(5) NOT NULL,
                CCNUMBER CHAR(16) NOT NULL,
                CID CHAR(5) NOT NULL,
                SANAME VARCHAR(30) NOT NULL,
                TDATE DATE,
                TTAG CHAR DEFAULT'C',
                PRIMARY KEY(BID, CCNUMBER, CID, SANAME));""" ##TTAG options assume C=confirmed, S=Shipped, E=Enroute, D=Delivered, L=Lost

    BASKET_DEF = """CREATE TABLE IF NOT EXISTS BASKET
            (CID CHAR(5) NOT NULL,
            BID CHAR(5) NOT NULL,
            PRIMARY KEY(BID));"""

    APPEARS_IN_DEF = """CREATE TABLE IF NOT EXISTS APPEARS_IN
                (BID CHAR(5) NOT NULL,
                PID CHAR(5) NOT NULL,
                QUANTITY INT,
                PRICESOLD DECIMAL(10,2),
                PRIMARY KEY(BID,PID));"""

    OFFER_PRODUCT_DEF = """CREATE TABLE IF NOT EXISTS OFFER_PRODUCT
                    (PID CHAR(5) NOT NULL,
                    OFFERPRICE DECIMAL(10,2),
                    PRIMARY KEY(PID));"""

    PRODUCT_DEF = """CREATE TABLE IF NOT EXISTS PRODUCT
                (PID CHAR(5) NOT NULL,
                PType CHAR, 
                PNAME VARCHAR(15),
                PPRICE DECIMAL(10,2),
                DESCRIPTION VARCHAR(15),
                PQUANTITY INT DEFAULT 0,
                PRIMARY KEY(PID));""" ##PType options assume C=Computer P=Printer L=Laptop M=Miscelenous

    COMPUTER_DEF = """CREATE TABLE IF NOT EXISTS COMPUTER
                (PID CHAR(5) NOT NULL,
                CPUTYPE VARCHAR(30),
                PRIMARY KEY(PID));"""

    PRINTER_DEF = """CREATE TABLE IF NOT EXISTS PRINTER
                (PID CHAR(5) NOT NULL,
                PRINTERTYPE VARCHAR(10),
                RESOLUTION VARCHAR(10),
                PRIMARY KEY(PID));"""

    LAPTOP_DEF = """CREATE TABLE IF NOT EXISTS LAPTOP
                (PID CHAR(5) NOT NULL,
                BTYPE VARCHAR(15),
                WEIGHT INT,
                PRIMARY KEY(PID));"""
    
    """
    2) SQL Table Constraints
    """
    SILVER_AND_ABOVE_CONSTRAINTS = """ALTER TABLE SILVER_AND_ABOVE
                                    ADD CONSTRAINT CUSTOMERSILVERFK FOREIGN KEY (CID) REFERENCES CUSTOMER(CID)
                                    ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    CREDIT_CARD_CONSTRAINTS = """ALTER TABLE CREDIT_CARD
                                ADD CONSTRAINT STOREDCARDRFK FOREIGN KEY (STOREDCARDCID) REFERENCES CUSTOMER(CID)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    SHIPPING_ADDRESS_CONSTRAINTS = """ALTER TABLE SHIPPING_ADDRESS
                                ADD CONSTRAINT CIDSHIPPINGFK FOREIGN KEY (CID) REFERENCES SILVER_AND_ABOVE(CID)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""

    TRANSACTION_CONSTRAINTS_1 = """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONCCFK FOREIGN KEY (CCNUMBER) REFERENCES CREDIT_CARD(CCNUMBER)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    TRANSACTION_CONSTRAINTS_2 = """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONSANAMECIDFK FOREIGN KEY (CID,SANAME) REFERENCES SHIPPING_ADDRESS(CID,SANAME)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    TRANSACTION_CONSTRAINTS_3 = """ALTER TABLE TRANSACTION
                                ADD CONSTRAINT TRANSACTIONBIDFK FOREIGN KEY (BID) REFERENCES BASKET(BID)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    BASKET_CONSTRAINTS = """ALTER TABLE BASKET
                        ADD CONSTRAINT BASKETCIDFK FOREIGN KEY (CID) REFERENCES CUSTOMER(CID)
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    APPEARS_IN_CONSTRAINTS_1 = """ALTER TABLE APPEARS_IN
                                ADD CONSTRAINT APPEARSBIDFK FOREIGN KEY (BID) REFERENCES BASKET(BID)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    APPEARS_IN_CONSTRAINTS_2 = """ALTER TABLE APPEARS_IN
                                ADD CONSTRAINT APPEARSINPIDFK FOREIGN KEY (PID) REFERENCES PRODUCT(PID)
                                ON DELETE CASCADE ON UPDATE CASCADE;"""

    OFFER_PRODUCT_CONSTAINTS = """ALTER TABLE OFFER_PRODUCT
                        ADD CONSTRAINT OFFERPRODUCTPIDFK FOREIGN KEY (PID) REFERENCES PRODUCT(PID)
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    COMPUTER_CONSTRAINTS = """ALTER TABLE COMPUTER
                        ADD CONSTRAINT COMPUTERPIDFK FOREIGN KEY (PID) REFERENCES PRODUCT(PID)
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    PRINTER_CONSTRAINTS = """ALTER TABLE PRINTER
                        ADD CONSTRAINT PRINTERPIDFK FOREIGN KEY (PID) REFERENCES PRODUCT(PID)
                        ON DELETE CASCADE ON UPDATE CASCADE;"""

    LAPTOP_CONSTAINTS = """ALTER TABLE LAPTOP
                        ADD CONSTRAINT LAPTOPPIDFK FOREIGN KEY (PID) REFERENCES COMPUTER(PID)
                        ON DELETE CASCADE ON UPDATE CASCADE;"""
    
    """
    3) SQL Populate Table Commands
    """
    CUSTOMER_DATA = """INSERT INTO CUSTOMER (CID, FNAME, LNAME, EMAIL, ADDRESS, PHONE, STATUS)
                    VALUES
                    ('C0001', 'Bob', 'Edwards', 'bobedwards123@gmail.com', '13 Pleasant Street, Newark NJ, 07103', '9783022229', 'R'),
                    ('C0002', 'Dylan', 'Clark', 'clark3246@gmail.com', '22 Roosevelt Ave, Princeton NJ, 01827', '9788662409', 'R'),
                    ('C0003', 'Riley', 'Mucci', 'rileyam@icloud.com', '25 Sycamore Street, Boston MA, 03452', '1234567890', 'S'),
                    ('C0004', 'Kimberly', 'Harding', 'harding7134@gmail.com', '202 Warren Street, Newark NJ, 07103', '7653458903', 'S'),
                    ('C0005', 'Richard', 'Morena', 'ram6789@icloud.com', '100 Lock Street, Newark NJ, 07103', '9784923765', 'G');"""
    
    CREDIT_CARD_DATA = """INSERT INTO CREDIT_CARD (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID)
                    VALUES
                    ('123456789123456', '827', 'Bob Edwards', 'Mastercard', '13 Pleasant Street, Newark NJ, 07103', '04/28', 00001),
                    ('122256789993456', '437', 'Dylan Clark', 'Discover', '22 Roosevelt Ave, Princeton NJ, 01827', '08/29', 00002),
                    ('110256780993336', '789', 'Riley Mucci', 'Mastercard', '25 Sycamore Street, Boston MA, 03452', '07/35', 00003),
                    ('11025670093336', '789', 'Kimberly Harding', 'Mastercard', '202 Warren Street, Newark NJ, 07103', '03/28', 00004),
                    ('34567809999999', '123', 'Richard Morena', 'Mastercard', '100 Lock Street, Newark NJ, 07103', '09/31', 00005);"""
    
    SILVER_AND_ABOVE_DATA = """INSERT INTO SILVER_AND_ABOVE (CID, CREDITLINE) 
                            VALUES
                            ('C0003', 8000),
                            ('C0004', 1000),
                            ('C0005', 7500);"""

    SHIPPING_ADDRESS_DATA = """INSERT INTO SHIPPING_ADDRESS (CID, SANAME, RECEPIENTNAME, STREET, SNUMBER, CITY, ZIP, STATE, COUNTRY)
                        VALUES
                        ('C0003', 'Riley Home', 'Riley Mucci', 'Sycamore Street', 25, 'Boston', '03452', 'MA', 'USA'),
                        ('C0004', 'Hardings Residence', 'Kimberly Harding', 'Warren Street', 202, 'Newark', '07103', 'NJ', 'USA'),
                        ('C0005', 'Richard Work', 'Richard Morena', 'Lock Street', 100, 'Newark', '07103', 'NJ', 'USA');"""

    TRANSACTION_DATA = """INSERT INTO TRANSACTION (BID, CCNUMBER, CID, SANAME, TDATE, TTAG) 
                        VALUES
                        ('B0001', '110256780993336', '00003', 'Riley Home', '2024-03-20', 'C'),
                        ('B0002', '11025670093336', '00004', 'Hardings Residence', '2024-04-05', 'E'),
                        ('B0003', '34567809999999', '00005', 'Richard Work', '2024-05-01', 'L');"""

    BASKET_DATA = """INSERT INTO BASKET (CID, BID) 
                    VALUES
                    ('C0003', 'B0001'),
                    ('C0004', 'B0002'),
                    ('C0005', 'B0003');"""
    
    PRODUCT_DATA = """INSERT INTO PRODUCT (PID, PTYPE, PNAME, PPRICE, DESCRIPTION, PQUANTITY) 
                    VALUES
                    ('P0001', 'C', 'Alienware', 1299.99, 'Gaming PC', 10),
                    ('P0002', 'L', 'MacBook Air', 999.99, 'Light Laptop', 15),
                    ('P0003', 'P', 'HP LaserJet', 299.99, 'Office Printer', 20),
                    ('P0004', 'M', 'USB Hub', 19.99, '4-port Hub', 50),
                    ('P0005', 'L', 'Dell XPS', 1199.99, 'Ultrabook', 8);"""

    COMPUTER_DATA = """INSERT INTO COMPUTER (PID, CPUTYPE) 
                    VALUES
                    ('P0001', 'Intel Core i7 Processor');"""
    
    PRINTER_DATA = """INSERT INTO PRINTER (PID, PRINTERTYPE, RESOLUTION)
                    VALUES
                    ('P0003', 'laser', '1200dpi');"""
    
    LAPTOP_DATA = """INSERT INTO LAPTOP(PID, BTYPE, WEIGHT)
                    VALUES
                    ('P0003', 'MacBook', 3),
                    ('P0005', 'Dell XPS', 4);"""
    
    APPEARS_IN_DATA = """INSERT INTO APPEARS_IN (BID, PID, QUANTITY, PRICESOLD)
                    VALUES
                    ('B0001', 'P0001', 1, 1299.99),
                    ('B0002', 'P0002', 1, 949.99),
                    ('B0003', 'P0003', 2, 299.99);"""
    
    OFFER_PRODUCT_DATA = """INSERT INTO OFFER_PRODUCT (PID, OFFERPRICE) 
                    VALUES
                    ('P0001', 1199.99),
                    ('P0002', 899.99),
                    ('P0003', 249.99),
                    ('P0004', 14.99),
                    ('P0005', 1099.99);"""

    """
    4) SQL Statistic Queries
    """
    STATISTIC_1 = """SELECT CCNUMBER, SUM(AI.QUANTITY*AI.PRICESOLD) AS TOTAL_CHARGED
                    FROM TRANSACTION T, APPEARS_IN AI
                    WHERE T.BID = AI.BID
                    GROUP BY CCNUMBER;"""
    
    STATISTIC_2 = """SELECT C.CID, C.FNAME, C.LNAME, SUM(AI.QUANTITY*AI.PRICESOLD) AS TOTAL_SPENT
                    FROM CUSTOMER C, TRANSACTION T, APPEARS_IN AI
                    WHERE C.CID =T.CID AND T.BID = AI.BID
                    GROUP BY C.CID, C.FNAME, C.LNAME
                    ORDER BY TOTAL_SPENT DESC;"""
    
    STATISTIC_3 = """SELECT AI.PID, P.PNAME, SUM(AI.QUANTITY) AS TOTAL_SOLD
                    FROM TRANSACTION T, APPEARS_IN AI, PRODUCT P
                    WHERE T.BID = AI.BID AND AI.PID = P.PID AND T.TDATE BETWEEN %s AND %s
                    GROUP BY AI.PID, P.PNAME
                    ORDER BY TOTAL_SOLD DESC;"""
    
    STATISTIC_4 = """SELECT AI.PID, P.PNAME, COUNT(DISTINCT T.CID) AS NUM_CUSTOMERS
                    FROM TRANSACTION T, APPEARS_IN AI, PRODUCT P
                    WHERE T.BID = AI.BID AND AI.PID = P.PID AND T.TDATE BETWEEN %s AND %s
                    GROUP BY AI.PID, P.PNAME
                    ORDER BY NUM_CUSTOMERS DESC;"""

    STATISTIC_5 = """SELECT CCNUMBER, MAX(BASKET_TOTAL) AS MAX_BASKET_TOTAL
                    FROM (
                        SELECT T.CCNUMBER, T.BID, SUM(AI.QUANTITY*AI.PRICESOLD) AS BASKET_TOTAL
                        FROM TRANSACTION T, APPEARS_IN AI
                        WHERE T.BID = AI.BID AND T.TDATE BETWEEN %s AND %s
                        GROUP BY T.CCNUMBER, T.BID
                    )
                    AS BASKET_TOTALS
                    GROUP BY CCNUMBER;"""

    STATISTIC_6 = """SELECT P.PTYPE, AVG(AI.PRICESOLD) AS AVG_AVG_SELLING_PRICE
                    FROM TRANSACTION T, APPEARS_IN AI, PRODUCT P
                    WHERE T.BID = AI.BID AND AI.PID = P.PID AND T.TDATE BETWEEN %s AND %s
                    GROUP BY P.PTYPE;"""

    """
    5) SQL Credit Card INSERT, UPDATE & DELETE
    """
    INSERT_CREDIT_CARD = """INSERT INTO SHIPPING_ADDRESS
                                 (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, 
                                 BILLADDRESS, EXPDATE)
                                 VALUES (%s,%s,%s,%s,%s,%s);"""
    
    UPDATE_CREDIT_CARD = """UPDATE CREDIT_CARD
                            SET SECNUMBER = %s,
                                OWNERNAME = %s,
                                CCTYPE     = %s,
                                BILLADDRESS= %s,
                                EXPDATE    = %s
                            WHERE CCNUMBER = %s;"""

    DELETE_CREDIT_CARD = "DELETE FROM CREDIT_CARD WHERE CCNUMBER = %s;"

    """
    6) SQL Shipping Adrress INSERT, UPDATE & DELETE
    """
    INSERT_SHIPPING_ADDRESS = """INSERT INTO SHIPPING_ADDRESS
                                 (CID, SANAME, RECEPIENTNAME, STREET, SNUMBER,
                                  CITY, ZIP, STATE, COUNTRY)
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    UPDATE_SHIPPING_ADDRESS = """UPDATE SHIPPING_ADDRESS
                                 SET RECEPIENTNAME=%s, STREET=%s, SNUMBER=%s,
                                     CITY=%s, ZIP=%s, STATE=%s, COUNTRY=%s
                                 WHERE CID=%s AND SANAME=%s;"""

    DELETE_SHIPPING_ADDRESS = """DELETE FROM SHIPPING_ADDRESS
                                 WHERE CID=%s AND SANAME=%s;"""

    """
    7) SQL Basket & Transactions INSERT, UPDATE & DELETE
    """
    INSERT_BASKET   = "INSERT INTO BASKET (CID, BID) VALUES (%s,%s);"

    INSERT_APPEARS  = """INSERT INTO APPEARS_IN
                         (BID, PID, QUANTITY, PRICESOLD)
                         VALUES (%s,%s,%s,%s);"""

    INSERT_TRANS    = """INSERT INTO TRANSACTION
                         (BID, CCNUMBER, CID, SANAME, TDATE, TTAG)
                         VALUES (%s,%s,%s,%s,%s,'C');"""

    UPDATE_TRANS_STATUS = """UPDATE TRANSACTION
                             SET TTAG = %s
                             WHERE BID = %s;"""

    SELECT_TRANS_STATUS = """SELECT TTAG FROM TRANSACTION WHERE BID = %s;"""

    SELECT_TRANS_HISTORY = """SELECT T.BID, T.TDATE, T.TTAG, AI.PID, P.PNAME,
                                     AI.QUANTITY, AI.PRICESOLD
                              FROM TRANSACTION T
                              JOIN APPEARS_IN AI ON T.BID = AI.BID
                              JOIN PRODUCT P     ON AI.PID = P.PID
                              WHERE T.CID = %s
                              {extra_conditions}
                              ORDER BY T.TDATE DESC;"""

