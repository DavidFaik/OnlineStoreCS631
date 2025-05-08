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
                CCTYPE VARCHAR(10) NOT NULL,
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
                PNAME VARCHAR(30),
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
                    ('C0005', 'Richard', 'Morena', 'ram6789@icloud.com', '100 Lock Street, Newark NJ, 07103', '9784923765', 'G'),
                    ('C0006', 'Olivia', 'Carter', 'olivia.carter@gmail.com', '62 Elm St, Clifton NJ, 07103', '5156327956', 'P'),
                    ('C0007', 'Ethan', 'Wells', 'ethan.wells@gmail.com', '32 Grove St, Bayonne NJ, 07060', '4245757235', 'S'),
                    ('C0008', 'Sophia', 'Hernandez', 'sophia.hernandez@gmail.com', '184 Maple St, Paterson NJ, 07002', '8525288978', 'S'),
                    ('C0009', 'Liam', 'Nguyen', 'liam.nguyen@gmail.com', '107 Kennedy Blvd, Paterson NJ, 07030', '7416525595', 'R'),
                    ('C0010', 'Emma', 'Wong', 'emma.wong@gmail.com', '126 Kennedy Blvd, Jersey City NJ, 07011', '2605169362', 'S'),
                    ('C0011', 'James', 'Lee', 'james.lee@gmail.com', '285 Main St, Bayonne NJ, 08102', '2321795240', 'P'),
                    ('C0012', 'Isabella', 'Murphy', 'isabella.murphy@gmail.com', '164 Elm St, Clifton NJ, 08102', '6354504309', 'P'),
                    ('C0013', 'Benjamin', 'Kim', 'benjamin.kim@gmail.com', '129 State St, Paterson NJ, 07011', '4325339998', 'S'),
                    ('C0014', 'Mia', 'Turner', 'mia.turner@gmail.com', '257 Oak St, Edison NJ, 08817', '9035768049', 'R'),
                    ('C0015', 'Alexander', 'Scott', 'alexander.scott@gmail.com', '238 Kennedy Blvd, Camden NJ, 07103', '5634862141', 'R'),
                    ('C0016', 'Charlotte', 'Lopez', 'charlotte.lopez@gmail.com', '158 Grove St, Jersey City NJ, 07030', '3085132183', 'G'),
                    ('C0017', 'Michael', 'Patel', 'michael.patel@gmail.com', '252 Elm St, Edison NJ, 07030', '5143022031', 'R'),
                    ('C0018', 'Amelia', 'Garcia', 'amelia.garcia@gmail.com', '287 Oak St, Bayonne NJ, 07501', '9383101901', 'G'),
                    ('C0019', 'Daniel', 'Ramirez', 'daniel.ramirez@gmail.com', '253 Elm St, Trenton NJ, 08817', '8398802903', 'G'),
                    ('C0020', 'Ava', 'Bennett', 'ava.bennett@gmail.com', '158 State St, Paterson NJ, 07011', '7883254617', 'G'),
                    ('C0021', 'Logan', 'Hughes', 'logan.hughes@gmail.com', '153 Grove St, Hoboken NJ, 07002', '2061619027', 'G'),
                    ('C0022', 'Grace', 'Reed', 'grace.reed@gmail.com', '60 Grove St, Newark NJ, 07002', '8422264320', 'G'),
                    ('C0023', 'Matthew', 'Diaz', 'matthew.diaz@gmail.com', '42 Maple St, Jersey City NJ, 08102', '4965276899', 'P'),
                    ('C0024', 'Chloe', 'Griffin', 'chloe.griffin@gmail.com', '180 State St, Edison NJ, 07060', '4327448809', 'S'),
                    ('C0025', 'Elijah', 'Cooper', 'elijah.cooper@gmail.com', '13 Pine St, Newark NJ, 07103', '9904194206', 'R'),
                    ('C0026', 'Ella', 'Ward', 'ella.ward@gmail.com', '136 Pine St, Clifton NJ, 07030', '9553870421', 'S'),
                    ('C0027', 'Sebastian', 'Brooks', 'sebastian.brooks@gmail.com', '12 Kennedy Blvd, Plainfield NJ, 08102', '9498715042', 'R'),
                    ('C0028', 'Aria', 'Perez', 'aria.perez@gmail.com', '270 River Rd, Newark NJ, 07002', '8184557983', 'S'),
                    ('C0029', 'Henry', 'Russell', 'henry.russell@gmail.com', '194 State St, Edison NJ, 07307', '9471590568', 'P'),
                    ('C0030', 'Scarlett', 'Sanders', 'scarlett.sanders@gmail.com', '60 Maple St, Camden NJ, 08608', '4366024821', 'G');
                    """
    
    CREDIT_CARD_DATA = """INSERT INTO CREDIT_CARD (CCNUMBER, SECNUMBER, OWNERNAME, CCTYPE, BILLADDRESS, EXPDATE, STOREDCARDCID)
                    VALUES
                    ('123456789123456', '827', 'Bob Edwards', 'Mastercard', '13 Pleasant Street, Newark NJ, 07103', '04/28', 'C0001'),
                    ('122256789993456', '437', 'Dylan Clark', 'Discover', '22 Roosevelt Ave, Princeton NJ, 01827', '08/29', 'C0002'),
                    ('110256780993336', '789', 'Riley Mucci', 'Mastercard', '25 Sycamore Street, Boston MA, 03452', '07/35', 'C0003'),
                    ('11025670093336', '789', 'Kimberly Harding', 'Mastercard', '202 Warren Street, Newark NJ, 07103', '03/28', 'C0004'),
                    ('34567809999999', '123', 'Richard Morena', 'Mastercard', '100 Lock Street, Newark NJ, 07103', '09/31', 'C0005'),
                    ('4000002940000006', '610', 'Olivia Carter', 'Visa', '62 Elm St, Clifton NJ, 07103', '08/29', 'C0006'),
                    ('4000000019370007', '836', 'Ethan Wells', 'Mastercard', '32 Grove St, Bayonne NJ, 07060', '11/28', 'C0007'),
                    ('4000000204850008', '311', 'Sophia Hernandez', 'Visa', '184 Maple St, Paterson NJ, 07002', '04/35', 'C0008'),
                    ('4000000028460009', '676', 'Liam Nguyen', 'Discover', '107 Kennedy Blvd, Paterson NJ, 07030', '11/31', 'C0009'),
                    ('4000000010980010', '283', 'Emma Wong', 'Amex', '126 Kennedy Blvd, Jersey City NJ, 07011', '05/34', 'C0010'),
                    ('4000000020440011', '424', 'James Lee', 'Discover', '285 Main St, Bayonne NJ, 08102', '12/26', 'C0011'),
                    ('4012320000000012', '852', 'Isabella Murphy', 'Amex', '164 Elm St, Clifton NJ, 08102', '01/27', 'C0012'),
                    ('4000018897000013', '973', 'Benjamin Kim', 'Visa', '129 State St, Paterson NJ, 07011', '02/29', 'C0013'),
                    ('4000000000000014', '746', 'Mia Turner', 'Discover', '257 Oak St, Edison NJ, 08817', '05/30', 'C0014'),
                    ('4000000000000015', '259', 'Alexander Scott', 'Visa', '238 Kennedy Blvd, Camden NJ, 07103', '02/30', 'C0015'),
                    ('4000000000000016', '931', 'Charlotte Lopez', 'Mastercard', '158 Grove St, Jersey City NJ, 07030', '03/34', 'C0016'),
                    ('4000000000000017', '263', 'Michael Patel', 'Visa', '252 Elm St, Edison NJ, 07030', '08/32', 'C0017'),
                    ('4000000000000018', '415', 'Amelia Garcia', 'Mastercard', '287 Oak St, Bayonne NJ, 07501', '07/35', 'C0018'),
                    ('4000000000000019', '326', 'Daniel Ramirez', 'Discover', '253 Elm St, Trenton NJ, 08817', '09/29', 'C0019'),
                    ('4000000000000020', '827', 'Ava Bennett', 'Visa', '158 State St, Paterson NJ, 07011', '04/33', 'C0020'),
                    ('4000000000000021', '514', 'Logan Hughes', 'Visa', '153 Grove St, Hoboken NJ, 07002', '06/31', 'C0021'),
                    ('4000000000000022', '739', 'Grace Reed', 'Mastercard', '60 Grove St, Newark NJ, 07002', '12/34', 'C0022'),
                    ('4000000000000023', '300', 'Matthew Diaz', 'Amex', '42 Maple St, Jersey City NJ, 08102', '11/30', 'C0023'),
                    ('4000000000000024', '678', 'Chloe Griffin', 'Discover', '180 State St, Edison NJ, 07060', '03/28', 'C0024'),
                    ('4000000000000025', '198', 'Elijah Cooper', 'Visa', '13 Pine St, Newark NJ, 07103', '08/27', 'C0025'),
                    ('4000000000000026', '881', 'Ella Ward', 'Amex', '136 Pine St, Clifton NJ, 07030', '10/35', 'C0026'),
                    ('4000000000000027', '469', 'Sebastian Brooks', 'Visa', '12 Kennedy Blvd, Plainfield NJ, 08102', '01/30', 'C0027'),
                    ('4000000000000028', '704', 'Aria Perez', 'Mastercard', '270 River Rd, Newark NJ, 07002', '09/33', 'C0028'),
                    ('4000000000000029', '546', 'Henry Russell', 'Discover', '194 State St, Edison NJ, 07307', '07/26', 'C0029'),
                    ('4000000000000030', '394', 'Scarlett Sanders', 'Visa', '60 Maple St, Camden NJ, 08608', '05/32', 'C0030');
                    """
    
    SILVER_AND_ABOVE_DATA = """INSERT INTO SILVER_AND_ABOVE (CID, CREDITLINE) 
                            VALUES
                            ('C0003', 8000),
                            ('C0004', 1000),
                            ('C0005', 7500),
                            ('C0006', 10000),
                            ('C0007', 2500),
                            ('C0008', 5000),
                            ('C0010', 7500),
                            ('C0011', 10000),
                            ('C0012', 2500),
                            ('C0013', 5000),
                            ('C0016', 7500),
                            ('C0018', 2500),
                            ('C0019', 5000),
                            ('C0020', 7500),
                            ('C0021', 10000),
                            ('C0022', 2500),
                            ('C0023', 5000),
                            ('C0024', 1000),
                            ('C0026', 5000),
                            ('C0028', 2500),
                            ('C0029', 10000),
                            ('C0030', 7500);
                            """
                            

    SHIPPING_ADDRESS_DATA = """INSERT INTO SHIPPING_ADDRESS (CID, SANAME, RECEPIENTNAME, STREET, SNUMBER, CITY, ZIP, STATE, COUNTRY)
                        VALUES
                        ('C0003', 'Riley Home', 'Riley Mucci', 'Sycamore Street', 25, 'Boston', '03452', 'MA', 'USA'),
                        ('C0004', 'Hardings Residence', 'Kimberly Harding', 'Warren Street', 202, 'Newark', '07103', 'NJ', 'USA'),
                        ('C0005', 'Richard Work', 'Richard Morena', 'Lock Street', 100, 'Newark', '07103', 'NJ', 'USA'),
                        ('C0006', 'Carter Home', 'Olivia Carter', 'Elm St', 62, 'Clifton', '07103', 'NJ', 'USA'),
                        ('C0007', 'Wells Home', 'Ethan Wells', 'Grove St', 32, 'Bayonne', '07060', 'NJ', 'USA'),
                        ('C0008', 'Hernandez Home', 'Sophia Hernandez', 'Maple St', 184, 'Paterson', '07002', 'NJ', 'USA'),
                        ('C0010', 'Wong Home', 'Emma Wong', 'Kennedy Blvd', 126, 'Jersey City', '07011', 'NJ', 'USA'),
                        ('C0011', 'Lee Home', 'James Lee', 'Main St', 285, 'Bayonne', '08102', 'NJ', 'USA'),
                        ('C0012', 'Murphy Home', 'Isabella Murphy', 'Elm St', 164, 'Clifton', '08102', 'NJ', 'USA'),
                        ('C0013', 'Kim Home', 'Benjamin Kim', 'State St', 129, 'Paterson', '07011', 'NJ', 'USA'),
                        ('C0016', 'Lopez Home', 'Charlotte Lopez', 'Grove St', 158, 'Jersey City', '07030', 'NJ', 'USA'),
                        ('C0018', 'Garcia Home', 'Amelia Garcia', 'Oak St', 287, 'Bayonne', '07501', 'NJ', 'USA'),
                        ('C0019', 'Ramirez Home', 'Daniel Ramirez', 'Elm St', 253, 'Trenton', '08817', 'NJ', 'USA'),
                        ('C0020', 'Bennett Home', 'Ava Bennett', 'State St', 158, 'Paterson', '07011', 'NJ', 'USA'),
                        ('C0021', 'Hughes Home', 'Logan Hughes', 'Grove St', 153, 'Hoboken', '07002', 'NJ', 'USA'),
                        ('C0022', 'Reed Home', 'Grace Reed', 'Grove St', 60, 'Newark', '07002', 'NJ', 'USA'),
                        ('C0023', 'Diaz Home', 'Matthew Diaz', 'Maple St', 42, 'Jersey City', '08102', 'NJ', 'USA'),
                        ('C0024', 'Griffin Home', 'Chloe Griffin', 'State St', 180, 'Edison', '07060', 'NJ', 'USA'),
                        ('C0026', 'Ward Home', 'Ella Ward', 'Pine St', 136, 'Clifton', '07030', 'NJ', 'USA'),
                        ('C0028', 'Perez Home', 'Aria Perez', 'River Rd', 270, 'Newark', '07002', 'NJ', 'USA'),
                        ('C0029', 'Russell Home', 'Henry Russell', 'State St', 194, 'Edison', '07307', 'NJ', 'USA'),
                        ('C0030', 'Sanders Home', 'Scarlett Sanders', 'Maple St', 60, 'Camden', '08608', 'NJ', 'USA');
                        """

    TRANSACTION_DATA = """INSERT INTO TRANSACTION (BID, CCNUMBER, CID, SANAME, TDATE, TTAG) 
                        VALUES
                        ('B0001', '110256780993336', '00003', 'Riley Home', '2024-03-20', 'C'),
                        ('B0002', '11025670093336', '00004', 'Hardings Residence', '2024-04-05', 'E'),
                        ('B0003', '34567809999999', '00005', 'Richard Work', '2024-05-01', 'L'),
                        ('B0006', '4000000000000006', 'C0006', 'Carter Home', '2024-01-21', 'C'),
                        ('B0007', '4000000000000007', 'C0007', 'Wells Home', '2024-02-14', 'E'),
                        ('B0008', '4000000000000008', 'C0008', 'Hernandez Home', '2024-03-11', 'S'),
                        ('B0010', '4000000000000010', 'C0010', 'Wong Home', '2024-04-02', 'D'),
                        ('B0011', '4000000000000011', 'C0011', 'Lee Home', '2024-01-25', 'C'),
                        ('B0012', '4000000000000012', 'C0012', 'Murphy Home', '2024-03-08', 'L'),
                        ('B0013', '4000000000000013', 'C0013', 'Kim Home', '2024-02-28', 'S'),
                        ('B0016', '4000000000000016', 'C0016', 'Lopez Home', '2024-03-15', 'E'),
                        ('B0018', '4000000000000018', 'C0018', 'Garcia Home', '2024-04-07', 'D'),
                        ('B0019', '4000000000000019', 'C0019', 'Ramirez Home', '2024-04-15', 'C'),
                        ('B0020', '4000000000000020', 'C0020', 'Bennett Home', '2024-02-19', 'S'),
                        ('B0021', '4000000000000021', 'C0021', 'Hughes Home', '2024-03-02', 'E'),
                        ('B0022', '4000000000000022', 'C0022', 'Reed Home', '2024-01-12', 'C'),
                        ('B0023', '4000000000000023', 'C0023', 'Diaz Home', '2024-02-10', 'D'),
                        ('B0024', '4000000000000024', 'C0024', 'Griffin Home', '2024-04-03', 'L'),
                        ('B0026', '4000000000000026', 'C0026', 'Ward Home', '2024-03-19', 'E'),
                        ('B0028', '4000000000000028', 'C0028', 'Perez Home', '2024-04-09', 'C'),
                        ('B0029', '4000000000000029', 'C0029', 'Russell Home', '2024-02-20', 'S'),
                        ('B0030', '4000000000000030', 'C0030', 'Sanders Home', '2024-03-27', 'D');
                        """

    BASKET_DATA = """INSERT INTO BASKET (CID, BID) 
                    VALUES
                    ('C0003', 'B0001'),
                    ('C0004', 'B0002'),
                    ('C0005', 'B0003'),
                    ('C0006', 'B0006'),
                    ('C0007', 'B0007'),
                    ('C0008', 'B0008'),
                    ('C0010', 'B0010'),
                    ('C0011', 'B0011'),
                    ('C0012', 'B0012'),
                    ('C0013', 'B0013'),
                    ('C0016', 'B0016'),
                    ('C0018', 'B0018'),
                    ('C0019', 'B0019'),
                    ('C0020', 'B0020'),
                    ('C0021', 'B0021'),
                    ('C0022', 'B0022'),
                    ('C0023', 'B0023'),
                    ('C0024', 'B0024'),
                    ('C0026', 'B0026'),
                    ('C0028', 'B0028'),
                    ('C0029', 'B0029'),
                    ('C0030', 'B0030');
                    """
    
    PRODUCT_DATA = """INSERT INTO PRODUCT (PID, PTYPE, PNAME, PPRICE, DESCRIPTION, PQUANTITY) 
                    VALUES
                    ('P0001', 'C', 'Alienware', 1299.99, 'Gaming PC', 10),
                    ('P0002', 'L', 'MacBook Air', 999.99, 'Light Laptop', 15),
                    ('P0003', 'P', 'HP LaserJet', 299.99, 'Office Printer', 20),
                    ('P0004', 'M', 'USB Hub', 19.99, '4-port Hub', 50),
                    ('P0005', 'L', 'Dell XPS', 1199.99, 'Ultrabook', 8),
                    ('P0006', 'M', 'HDMI Cable', 38.06, 'Accessory', 39),
                    ('P0007', 'P', 'Brother HL-L2350DW', 355.68, 'Printer', 16),
                    ('P0008', 'P', 'Canon Pixma', 377.38, 'Printer', 25),
                    ('P0009', 'P', 'Canon Pixma', 309.21, 'Printer', 27),
                    ('P0010', 'L', 'HP Pavilion', 1183.20, 'Laptop', 14),
                    ('P0011', 'P', 'Epson EcoTank', 249.30, 'Printer', 23),
                    ('P0012', 'M', 'Laptop Stand', 13.20, 'Accessory', 27),
                    ('P0013', 'L', 'HP Pavilion', 964.01, 'Laptop', 5),
                    ('P0014', 'M', 'Laptop Stand', 44.15, 'Accessory', 22),
                    ('P0015', 'L', 'Lenovo Yoga', 1138.57, 'Laptop', 6),
                    ('P0016', 'C', 'CyberPowerPC', 1167.26, 'Gaming Desktop', 13),
                    ('P0017', 'C', 'CyberPowerPC', 1417.38, 'Gaming Desktop', 14),
                    ('P0018', 'L', 'HP Pavilion', 931.16, 'Laptop', 5),
                    ('P0019', 'P', 'Canon Pixma', 344.01, 'Printer', 10),
                    ('P0020', 'M', 'Laptop Stand', 29.65, 'Accessory', 69),
                    ('P0021', 'L', 'Lenovo Yoga', 1258.65, 'Laptop', 8),
                    ('P0022', 'C', 'HP Omen', 1132.11, 'Gaming Desktop', 15),
                    ('P0023', 'P', 'Brother HL-L2350DW', 258.25, 'Printer', 15),
                    ('P0024', 'M', 'Wireless Mouse', 38.82, 'Accessory', 78),
                    ('P0025', 'P', 'Epson EcoTank', 366.83, 'Printer', 25),
                    ('P0026', 'L', 'Lenovo Yoga', 713.46, 'Laptop', 7),
                    ('P0027', 'L', 'Asus ZenBook', 1093.97, 'Laptop', 6),
                    ('P0028', 'P', 'Canon Pixma', 158.48, 'Printer', 25),
                    ('P0029', 'P', 'Canon Pixma', 358.95, 'Printer', 26),
                    ('P0030', 'M', 'Laptop Stand', 22.76, 'Accessory', 54);
                    """

    COMPUTER_DATA = """INSERT INTO COMPUTER (PID, CPUTYPE) 
                    VALUES
                    ('P0001', 'Intel Core i7 Processor'),
                    ('P0016', 'AMD Ryzen 5'),
                    ('P0017', 'AMD Ryzen 7'),
                    ('P0022', 'Intel Core i5');
                    """
    
    PRINTER_DATA = """INSERT INTO PRINTER (PID, PRINTERTYPE, RESOLUTION)
                    VALUES
                    ('P0003', 'laser', '1200dpi'),
                    ('P0007', 'inkjet', '1200dpi'),
                    ('P0008', 'inkjet', '600dpi'),
                    ('P0009', 'laser', '600dpi'),
                    ('P0011', 'laser', '1200dpi'),
                    ('P0019', 'laser', '600dpi'),
                    ('P0023', 'color', '600dpi'),
                    ('P0025', 'color', '600dpi'),
                    ('P0028', 'color', '1200dpi'),
                    ('P0029', 'laser', '600dpi');
                    """

                    
    LAPTOP_DATA = """INSERT INTO LAPTOP(PID, BTYPE, WEIGHT)
                    VALUES
                    ('P0003', 'MacBook', 3),
                    ('P0005', 'Dell XPS', 4),
                    ('P0010', 'MacBook', 3),
                    ('P0013', 'Lenovo', 4),
                    ('P0015', 'Dell', 3),
                    ('P0018', 'MacBook', 2),
                    ('P0021', 'MacBook', 4),
                    ('P0026', 'MacBook', 4),
                    ('P0027', 'MacBook', 5);
                    """
    
    APPEARS_IN_DATA = """INSERT INTO APPEARS_IN (BID, PID, QUANTITY, PRICESOLD)
                    VALUES
                    ('B0001', 'P0001', 3, 1009.88),
                    ('B0002', 'P0012', 1, 607.68),
                    ('B0003', 'P0030', 2, 151.05),
                    ('B0004', 'P0014', 1, 1104.06),
                    ('B0005', 'P0024', 3, 991.82),
                    ('B0006', 'P0026', 3, 442.94),
                    ('B0007', 'P0020', 2, 1014.39),
                    ('B0008', 'P0029', 1, 386.79),
                    ('B0009', 'P0012', 1, 817.73),
                    ('B0010', 'P0027', 2, 484.41),
                    ('B0011', 'P0011', 1, 868.50),
                    ('B0012', 'P0010', 1, 1271.96),
                    ('B0013', 'P0003', 3, 748.89),
                    ('B0014', 'P0013', 1, 1202.70),
                    ('B0015', 'P0012', 3, 862.38),
                    ('B0016', 'P0012', 3, 17.23),
                    ('B0017', 'P0003', 2, 734.49),
                    ('B0018', 'P0014', 1, 1137.48),
                    ('B0019', 'P0028', 1, 242.23),
                    ('B0020', 'P0009', 3, 48.65),
                    ('B0021', 'P0017', 1, 1124.80),
                    ('B0022', 'P0027', 1, 893.48),
                    ('B0023', 'P0019', 3, 517.57),
                    ('B0024', 'P0021', 2, 272.47),
                    ('B0025', 'P0028', 3, 945.42),
                    ('B0026', 'P0016', 1, 146.40),
                    ('B0027', 'P0006', 1, 712.81),
                    ('B0028', 'P0029', 3, 1272.73),
                    ('B0029', 'P0030', 3, 773.83),
                    ('B0030', 'P0023', 1, 1000.33);
                    """
    
    OFFER_PRODUCT_DATA = """INSERT INTO OFFER_PRODUCT (PID, OFFERPRICE) 
                    VALUES
                    ('P0001', 1199.99),
                    ('P0002', 899.99),
                    ('P0003', 249.99),
                    ('P0004', 14.99),
                    ('P0005', 1099.99),
                    ('P0006', 35.30),
                    ('P0007', 317.20),
                    ('P0008', 322.11),
                    ('P0009', 277.68),
                    ('P0010', 1120.70),
                    ('P0011', 215.36),
                    ('P0012', 12.39),
                    ('P0013', 836.41),
                    ('P0014', 38.75),
                    ('P0015', 1037.29),
                    ('P0016', 1049.49),
                    ('P0017', 1326.34),
                    ('P0018', 835.76),
                    ('P0019', 321.11),
                    ('P0020', 25.76),
                    ('P0021', 1138.20),
                    ('P0022', 1022.60),
                    ('P0023', 224.72),
                    ('P0024', 34.19),
                    ('P0025', 337.12),
                    ('P0026', 619.04),
                    ('P0027', 947.66),
                    ('P0028', 147.32),
                    ('P0029', 331.75),
                    ('P0030', 19.53);
                    """

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
                    ORDER BY TOTAL_SPENT DESC
                    LIMIT 10;"""
    
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

