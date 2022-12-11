/* Create a database called book_store for our application */
CREATE database book_store;

/* Use database we created */
USE book_store;

/* Create a table "Books" which store all the books added */
CREATE TABLE Books (book_code INT NOT NULL,  title VARCHAR(50), author VARCHAR(100), isbn VARCHAR(15), pub_code INT, gen_code INT, cost INT, page_count INT, CONSTRAINT books_pk PRIMARY KEY (book_code));
/* Insert books in the table "Books" */
INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES (1001, 'History of Clovania', 'Michel Stoke', '2136AAZ88', 103, 104, 56, 750);
INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES (1002, 'C Programming', 'Vladimir Medvedek', 'S7A88689', 102, 105, 16, 336);
INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES (1003, 'The Mighty King', 'Robert Black', '88AL23ZSC', 104, 105, 66, 1150);
INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES (1004, 'Python made Easy', 'Singer John', '923P767P', 104, 104, 36, 456);
INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES (1005, 'Inside Web technology', 'Steve Ruthford', '2136AAZ88', 104, 101, 15, 368);

/* Create a table "Genre" which store the Genre of a book */
CREATE TABLE Genre (gen_code INT NOT NULL, gen_type VARCHAR(20), CONSTRAINT genre_pk PRIMARY KEY (gen_code));
/* Insert genre in the table "Genre" */
INSERT INTO Genre (gen_code, gen_type) VALUES (101, 'Fiction');
INSERT INTO Genre (gen_code, gen_type) VALUES (102, 'Education');
INSERT INTO Genre (gen_code, gen_type) VALUES (103, 'Science');
INSERT INTO Genre (gen_code, gen_type) VALUES (104, 'Technology');
INSERT INTO Genre (gen_code, gen_type) VALUES (105, 'Politics');

/* Create a table "Publisher" which stores all the publishers */
CREATE TABLE Publisher (pub_code INT NOT NULL, pub_name VARCHAR(50), address VARCHAR(100), phone VARCHAR(10), email VARCHAR(50), CONSTRAINT pub_pk PRIMARY KEY (pub_code));
/* Insert publishers in the table "Publisher" */
INSERT INTO Publisher (pub_code, pub_name, address, phone, email) VALUES (101, 'Olympia Publisher', '10880 Wilshire Blvd, Los Angeles,California, 90024', '324786897', 'olympia_usa@hotmail.com');
INSERT INTO Publisher (pub_code, pub_name, address, phone, email) VALUES (102, 'Penguin Random House', '320 Front Street West, Suite 1400, Toronto, ON M5V3B6', '888523929', 'penguin@gmail.com');
INSERT INTO Publisher (pub_code, pub_name, address, phone, email) VALUES (103, 'Nelson Education', '1120 Birchmount Road,Toronto,Canada,M1K 5G4', '46998555', 'newlson_pub@yahoo.com');
INSERT INTO Publisher (pub_code, pub_name, address, phone, email) VALUES (104, 'McGraw Hill', '145 King St West, Suite 1501 Toronto, ON, Canada M5H 1J8', '388954646', 'mcgrawhill@gmail.com');

/* Create a table "Customer" which stores all the customers/users */
CREATE TABLE Customer (cust_code INT, user_id VARCHAR(10), user_pw VARCHAR(15), name VARCHAR(50), address VARCHAR(100), city VARCHAR(20), state VARCHAR(2), zip VARCHAR(5), phone VARCHAR(10), email VARCHAR(50), CONSTRAINT cust_pk PRIMARY KEY (cust_code));
/* Insert customer in the table "Customer" */
INSERT INTO Customer (cust_code, user_id, user_pw, name, address, city, state, zip, phone, email) VALUES (1000, 'ADMIN', 'admin', 'Anirudh Jagganath', '2387 Queen Avenue', 'Toronto', 'ON', '34879', '7866888989', 'ani_ru@gmail.com');

/* Create a table "BookStock" which stores the number of books */
CREATE TABLE BookStock (stock_no INT, book_code INT, stock_in_hand INT, min_stock INT, PRIMARY KEY (stock_no));
/* Insert no of books of a book in the table "BookStock" */
INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES(1, 1001, 20, 10);
INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES(2, 1002, 0, 10);
INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES(3, 1003, 0, 10);
INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES(5, 1005, 0, 10);
INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES(4, 1004, 0, 10);

/* Create a table "PublisherBankAc" which stores bank details of a publisher */
CREATE TABLE PublisherBankAc (pub_code INT, BankAc VARCHAR(20), PRIMARY KEY (pub_code));

/* Create a table "Bookbasket" which stores the details of a book */
CREATE TABLE BookBasket (entry_code INT, book_code INT, no_copies INT, unit_price INT, tot_cost INT);

/* Create a table "OrderMaster" which stores the deatils of the order to be placed */
CREATE TABLE OrderMaster (order_no INT, user_id VARCHAR(10), order_date DATE, number_of_items INT, tot_amount INT, ship_address VARCHAR(100), ship_city vARCHAR(50), ship_state VARCHAR(30), ship_zip VARCHAR(10), ship_contact VARCHAR(12), order_status INT, PRIMARY KEY (order_no));

/* Create a table "OrderDetail" which stores the deatils of the order placed */
CREATE TABLE OrderDetail (ent_no INT, order_no INT, item_no INT, book_code INT, no_of_copies INT, unit_price INT, tot_cost INT, PRIMARY KEY (ent_no));
