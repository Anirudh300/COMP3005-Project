from datetime import date
import mysql.connector as con

# Database Connection
db = con.connect(host="localhost", user="root", password="rohitsharma", database="book_store")
cmd = db.cursor()

# Global variable to track current user other than ADMIN
cur_user = ""


# Function that checks if the code (especially Primary Key)  is valid and does exist in a given function
def is_valid(tbl_name, fld_name, chk_val):
    # Query to check if the said code (field value) is avaiable in the given table or not
    cmd.execute("SELECT COUNT(" + fld_name + ") FROM " + tbl_name + " WHERE " + fld_name + "=" + str(chk_val))
    records = cmd.fetchall()
    if len(records) > 0:  # If record found
        return True
    else:
        return False


# Function (like utility tool) that gives values of a field which is a string based on the value of
# another field which is an integer
# For example by supplying book_code (which is an int) to Books table we can get book_name (which is string)
def get_str(req_fld, tbl_name, where_fld, where_val):
    cmd.execute("SELECT " + req_fld + " FROM " + tbl_name + " WHERE " + where_fld + "=" + str(where_val))
    records = cmd.fetchall()
    if len(records) > 0:
        r = records[0]
        return str(r[0])
    else:
        return ""


# This function returns a value of a numeric field based on a value of a string field
def get_code(req_fld, tbl_name, where_fld, where_val):
    cmd.execute("SELECT " + req_fld + " FROM " + tbl_name + " WHERE " + where_fld + "='" + where_val + "'")
    records = cmd.fetchall()
    if len(records) > 0:
        r = records[0]
        return int(str(r[0]))
    else:
        return 0


# Getting Maximum value of any numeric field in any table
# It helps us to avoid duplicate Primary Key
def get_maximum(fld_name, tbl_name):
    cmd.execute("SELECT MAX(" + fld_name + ") FROM " + tbl_name)  # Used MAX() aggregate function to find miximum
    records = cmd.fetchall()
    r = records[0]
    if r[0] == None:  # If the table is empty then it returns 0
        return 0
    else:
        return r[0]  # Desired value otherwise


# Verifying admin credentials
def check_admin(upw):
    if upw == "admin":  # Considering the password of the super user (here it is ADMIN is admin)
        return True
    else:
        return False


# Verifying customer credentials
def check_customer(uid, upw):
    # Query to find if the user does exist
    cmd.execute("SELECT user_pw FROM Customer WHERE user_id='" + uid + "'")
    records = cmd.fetchall()
    if len(records) > 0:  # If user found then
        row = records[0]
        if row[0] == upw:  # Validates password
            return True
        else:
            return False
    else:
        print("Customer not found!")
        return False


# It displays list of records with any two desired fields of any table
# It helps us to display the valid options available
def list_fields(tbl_name, pk_field, desc_field, title):
    print(title)
    cmd.execute("SELECT " + pk_field + ", " + desc_field + " FROM " + tbl_name)
    records = cmd.fetchall()
    for row in records:
        print(str(row[0]) + ", " + row[1])


# Function to add a book (admin)
def add_book():
    print("")
    print("**** ADDINg NEW BOOK ****")
    # Generating Primary Key (Maximum plus 1)
    b_code = int(str(get_maximum("book_code", "books"))) + 1

    # Entering other required values
    b_title = input(str("Enter Book Titile: "))
    b_author = input(str("Enter author(s): "))
    b_isbn = input(str("Book ISBN: "))
    list_fields("publisher", "pub_code", "pub_name", "Publisher List...")
    b_pub_code = int(input(str("Enter a valid publisher code (list above): ")))
    list_fields("genre", "gen_code", "gen_type", "Genre List...")
    b_gen_code = int(input(str("Enter Genre Code (List above): ")))
    b_cost = int(input(str("Enter Cost: ")))

    b_pages = int(input(str("Enter Pages: ")))
    # inserts a record to Boks table
    cmd.execute(
        "INSERT INTO Books (book_code, title, author, isbn, pub_code, gen_code, cost, page_count) VALUES(" + str(
            b_code) + ", '" + b_title + "', '" + b_author + "', '" + b_isbn + "', " + str(b_pub_code) + ", " + str(
            b_gen_code) + ", " + str(b_cost) + ", " + str(b_pages) + ")")
    db.commit()
    s_no = int(str(get_maximum("stock_no", "bookstock"))) + 1

    # Also creates a corresponding stock record
    cmd.execute(
        "INSERT INTO BookStock (stock_no, book_code, stock_in_hand, min_stock) VALUES (" + str(s_no) + ", " + str(
            b_code) + ", 0, 10 )")
    db.commit()
    print("New Book Added!")


# Function to add a publisher (admin)
def add_publisher():
    print("")
    print("**** ADDING PUBLISHER ****")
    p_code = int(str(get_maximum("pub_code", "publisher"))) + 1
    p_name = input(str("Enter Publisher Name: "))
    p_address = input(str("Enter Address: "))
    p_phone = input(str("Enter Phone: "))
    p_emial = input(str("Enter Email: "))
    cmd.execute("INSERT INTO Publisher (pub_code, pub_name, address, phone, email) VALUES (" + str(
        p_code) + ", '" + p_name + "', '" + p_address + "', '" + p_phone + "', '" + p_email + "')")
    db.commit()
    print("Publisher Added!")


# Function to add a genre (admin)
def add_genre():
    print("")
    g_code = int(str(get_maximum("gen_code", "genre"))) + 1
    g_type = input(str("Enter Genre type: "))
    cmd.execute("INSERT INTO genre (gen_code, gen_type) VALUES (" + str(g_code) + ",'" + g_type + "')")
    db.commit()
    print("Genre Added!")


# Function to remove book (admin)
def remove_book():
    print("")
    print("**** REMOVE BOOK ****")
    print("1. Use Book Code")
    print("2. Use ISBN")
    opt = input(str("How would you remove the book? Enter your choice: "))
    if opt == "1":
        r_code = input(str("Enter Book Code: "))
        cmd.execute("DELETE FROM Books WHERE book_code=" + r_code)
        db.commit()
        cmd.execute("DELETE FROM BookStock WHERE book_code=" + r_code)
        db.commit()
    elif opt == "2":
        r_code = input(str("Enter ISBN: "))
        b_code = get_code("book_code", "books", "isbn", r_code)
        cmd.execute("DELETE FROM Books WHERE isbn='" + r_code + "'")
        db.commit()
        cmd.execute("DELETE FROM BookStock WHERE book_code =" + b_code)
        db.commit()
    else:
        print("Deletion aborted due to invalid code")


# Function to get current stock of a book (admin)
def get_stock(b_code):
    cmd.execute("SELECT stock_in_hand FROM bookstock WHERE book_code=" + str(b_code))
    records = cmd.fetchall()
    if len(records) > 0:
        r = records[0]
        return int(str(r[0]))
    else:
        return -1


# Function to get the price of a book
def get_price(b_code):
    cmd.execute("SELECT cost FROM books WHERE book_code=" + str(b_code))

    records = cmd.fetchall()
    if len(records) > 0:
        r = records[0]
        return int(str(r[0]))
    else:
        return -1


# Updating the stock of a book
def update_stock():
    print("")
    print("**** UPDATE STOCK ****")
    print("1. Use Book Code")
    print("2. Use ISBN")
    opt = input(str("How would you update the book? Enter your choice: "))
    if opt == "1":
        u_code = input(str("Enter Book Code: "))
        u_new_stock = int(input(str("Enter new arrivals count: ")))
        u_cur_stock = int(get_stock(u_code))
        u_new_stock = u_cur_stock + u_new_stock
        cmd.execute("UPDATE BookStock SET stock_in_hand=" + str(u_new_stock) + " WHERE book_code=" + u_code)
        db.commit()
        print("Stock Updated!")
    elif opt == "2":
        r_code = input(str("Enter ISBN: "))
        b_code = get_code("book_code", "books", "isbn", r_code)
        u_cur_stock = int(get_stock(b_code))
        u_new_stock = u_cur_stock + u_new_stock
        cmd.execute("UPDATE BookStock SET stock_in_hand=" + str(u_new_stock) + " WHERE book_code=" + b_code)

        db.commit()
        print("Stock Updated!")
    else:
        print("Deletion aborted due to invalid code")


# Declaring order status
def status_string(arg):
    return_as = {
        0: "Order Placed",
        1: "Shipped",
        2: "On The way",
        3: "Out For Delivery",
        4: "Delivered",
        5: "Undelivered",
    }
    return return_as.get(arg, "")


# Updating order status
def update_order_status():
    print("")
    print("**** UPDATE ORDER STATUS ****")

    print("")

    cmd.execute(
        "SELECT order_no, order_date, number_of_items, tot_amount, order_status FROM OrderMaster WHERE order_status <= 5")
    records = cmd.fetchall()

    if len(records) > 0:
        print("List of all pending orders: ")
        print("")

        for row in records:
            print(str(row[0]) + " - " + str(row[1]) + " :: " + str(row[2]) + " ( $ " + str(
                row[3]) + " ) - [ " + status_string(int(row[4])) + " ]")

        o_no = input(str("Enter Order Number: "))

        cmd.execute(
            "SELECT order_no, order_date, number_of_items, tot_amount, order_status FROM OrderMaster WHERE order_no=" + o_no)
        records = cmd.fetchall()
        if len(records) > 0:
            row = records[0]
            print("")
            print("Order Detail: ")
            print("")
            print(str(row[0]) + " - " + str(row[1]) + " :: " + str(row[2]) + " ( $ " + str(
                row[3]) + " ) - [ " + status_string(int(row[4])) + " ]")
            print("")
            if int(row[4]) <= 4:
                opt = input(str("Do you want to  improve status to next level? [Y-Yes, N-No] "))
                if opt == "Y":
                    cmd.execute("UPDATE OrderMaster SET order_status = (order_status + 1) WHERE order_no=" + o_no)
                    db.commit()
            else:
                print("It reached final status")
        else:
            print("You have typed wrong order number")
    else:
        print("No Pending order for now!");


# Admin interface
def admin_module():
    print("***Admin Module***")
    while 1:
        print("")
        print("1. Add book")
        print("2. Add Publisher")
        print("3. Add Genre")
        print("4. Delete Book")
        print("5. Update Stock")
        print("6. Update Order Status")
        print("7. Quit")
        opt = input(str("Enter your choice: "))
        if opt == "1":
            add_book()
        elif opt == "2":
            add_publisher()
        elif opt == "3":
            add_genre()
        elif opt == "4":
            remove_book()
        elif opt == "5":
            update_stock()
        elif opt == "6":
            update_order_status()
        elif opt == "7":
            return
        else:
            print("Invalid choice!")


# Check out
def check_out():
    print("")
    print("**** CHECK OUT ****")
    cmd.execute("SELECT * FROM BookBasket")
    records = cmd.fetchall()
    print("")
    print("You have " + str(len(records)) + " items in the basket!")
    tot_cost = 0
    print("")
    for row in records:
        print(str(row[0]) + ". " + get_str("title", "books", "book_code", int(row[1])) + " - " + str(
            row[2]) + " copies ($ " + str(row[3]) + ")")
        tot_cost = tot_cost + int(row[4])
    item_count = len(records)
    print("")
    yn = input(str("Do you want to check out? [Y - Yes N - No] "))
    if yn == "Y":
        print("")
        print("Order Date: ", date.today())
        print("SHIPPING ADDRESS")
        s_address = input(str("Address: "))
        s_city = input(str("City: "))
        s_state = input(str("State: "))
        s_zip = input(str("ZIP: "))
        s_contact = input(str("Contact Number: "))

        o_no = int(get_maximum("order_no", "ordermaster")) + 1

        # Order status could be 0- Placed, 1- Shipped, 2- On The way, 3- Out for delivery, 4- Delivered, 5- Undelivered

        cmd.execute(
            "INSERT INTO OrderMaster (order_no, user_id, order_date, number_of_items, tot_amount, ship_address, ship_city, ship_state, ship_zip, ship_contact, order_status) VALUES (" + str(
                o_no) + ", '" + cur_user + "', '" + str(date.today()) + "', " + str(item_count) + ", " + str(
                tot_cost) + ",' " + s_address + "', '" + s_city + "', '" + s_state + "', '" + s_zip + "','" + s_contact + "', 0)")
        db.commit()

        d_no = int(get_maximum("ent_no", "orderdetail")) + 1
        i_no = 1
        for row in records:
            cmd.execute(
                "INSERT INTO OrderDetail (ent_no, order_no, item_no, book_code, no_of_copies, unit_price, tot_cost) VALUES(" + str(
                    d_no) + ", " + str(o_no) + ", " + str(i_no) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(
                    row[3]) + ", " + str(row[4]) + ")")
            db.commit()
            cmd.execute(
                "UPDATE BookStock SET stock_in_hand = (stock_in_hand - " + str(row[2]) + ") WHERE book_code=" + str(
                    row[1]))
            db.commit()
            d_no = d_no + 1
            i_no = i_no + 1
        cmd.execute("DELETE FROM BookBasket")
        db.commit()
        print("Order Placed! Your Order ID is " + str(o_no))
    else:
        print("Sorry! We will empty your basket")
        cmd.execute("DELETE FROM BookBasket")
        db.commit()
        print("Done!")


# Search a book
def book_search():
    print("")
    print("*** SEARCHING A BOOK ****")
    print("")
    print("1. By Title")
    print("2. By Author")
    print("3. By Genre")
    print("4. By ISBN")
    print("5. By Publisher")
    print("6. Move back")
    opt = input(str("Enter your choice: "))
    if opt == "1":
        sch_str = input(str("Enter Book Title: "))
        qry_str = "SELECT * FROM Books WHERE Title = '" + sch_str + "'"
    elif opt == "2":
        sch_str = input(str("Enter Author Name: "))
        qry_str = "SELECT * FROM Books WHERE author LIKE '%" + sch_str + "%'"
    elif opt == "3":
        sch_str = input(str("What Genere Type you are looking for? "))

        qry_str = "SELECT * FROM Books WHERE gen_code = (SELECT gen_code FROM genre WHERE gen_type='" + sch_str + "')"
    elif opt == "4":
        sch_str = input(str(""))
        qry_str = "SELECT * FROM Books WHERE isbn = '" + sch_str + "'"

    elif opt == "5":
        return
    else:
        print("Invalid choice")
    cmd.execute(qry_str)
    records = cmd.fetchall()
    print("")
    print("Search Result...")
    print("")
    b_code = 0
    for row in records:
        print(str(row[0]) + " : " + row[1] + "\t:\t" + row[2] + "\t:\t" + row[3] + "\t: $" + str(row[6]) + " : " + str(
            row[7]))

    opt = input(str("Type 1. Add to Basket, 2. Not interested: "))
    b_code = int(input(str("Enter book code: ")))
    cur_stock = get_stock(b_code)
    print("There are " + str(cur_stock) + " books in stock!")
    if int(str(cur_stock)) > 0:
        no_copies = int(input(str("How many copies do you want?")))
        unit_price = get_price(b_code)
        total_cost = int(unit_price) * int(no_copies)
        if opt == "1":
            e_code = int(get_maximum("entry_code", "bookbasket")) + 1
            cmd.execute("INSERT INTO bookbasket (entry_code, book_code, no_copies, unit_price, tot_cost) VALUES(" + str(
                e_code) + ", " + str(b_code) + ", " + str(no_copies) + ", " + str(unit_price) + ", " + str(
                total_cost) + ")")
            db.commit()
            print("Added to basket!")
        else:
            print("try other!")
    else:
        print("You cannot add this book!")


# Order a book by book code
def book_order():
    print("")
    print("**** ORDER BOOK ****")
    print("")

    b_code = int(input(str("Enter book code: ")))
    cur_stock = get_stock(b_code)
    print("There are " + str(cur_stock) + " books in stock!")
    if int(str(cur_stock)) > 0:
        no_copies = int(input(str("How many copies you want?")))
        unit_price = get_price(b_code)
        total_cost = int(unit_price) * int(no_copies)

        e_code = int(get_maximum("entry_code", "bookbasket")) + 1
        cmd.execute("INSERT INTO bookbasket (entry_code, book_code, no_copies, unit_price, tot_cost) VALUES(" + str(
            e_code) + ", " + str(b_code) + ", " + str(no_copies) + ", " + str(unit_price) + ", " + str(
            total_cost) + ")")
        db.commit()
        print("Added to the basket!")
    else:
        print("You cannot add this book!")


# To track the order
def track_order():
    print("")
    print("**** TRACK YOUR ORDER ****")
    print("")
    o_no = input(str("Enter Order Number: "))
    cmd.execute("SELECT order_status FROM OrderMaster WHERE order_no=" + o_no)
    records = cmd.fetchall()
    if len(records) > 0:
        row = records[0]
        print("")
        print("Current Status:")
        print("")
        counter = 0
        while counter < int(row[0]):
            print("[ " + status_string(counter) + " ] --> ", end=" ")
            counter = counter + 1
        print("[ " + status_string(int(row[0])) + " ]")
    else:
        print("Order details are not available")


# Customer interface
def customer_module():
    print("")
    print("***Customer Module***")
    while 1:
        print("")
        print("1. Search a book")
        print("2. Order a book by book code")
        print("3. Check Out")
        print("4. Track your order")
        print("5. Quit")

        opt = input(str("Enter your choice: "))
        if opt == "1":
            book_search()
        elif opt == "2":
            book_order()
        elif opt == "3":
            check_out()
        elif opt == "4":
            track_order()
        elif opt == "5":
            return
        else:
            print("Invalid Choice")


# Register as a new Customer
def register_customer():
    print("")
    print("**** Register as a New Customer ****")
    print("")
    c_code = int(get_maximum("cust_code", "customer")) + 1
    c_uid = "C" + str(c_code)
    pwd = input(str("Please choose a password: "))
    c_name = input(str("Name: "))
    c_address = input(str("Address: "))
    c_city = input(str("City: "))
    c_state = input(str("State: "))
    c_phone = input(str("Phone Number: "))
    c_email = input(str("Email ID: "))

    print("")
    opt = input(str("Press S - Submit, C - Cancel: "))
    if opt == "S":
        cmd.execute(
            "INSERT INTO Customer (cust_code, user_id, user_pw, name, address, city, state, phone, email) VALUES(" + str(
                c_code) + ", '" + c_uid + "', '" + pwd + "', '" + c_name + "', '" + c_address + "', '" + c_city + "', '" + c_state + "', '" + c_phone + "', '" + c_email + "')")
        db.commit()
        print("Successfully Registered as " + c_uid)
    else:
        print("Sorry! We missed you!")


# Main()
def main():
    print("*****************************************")
    print("********* WELCOME TO 'LOOK INNA BOOK'  ***********")
    print("*****************************************")
    while 1:
        print("")
        print("1. Login as Admin or Customer")
        print("2. Register as a new Customer")
        print("3. Exit")
        print("")
        opt = input(str("Enter your choice: "))
        if opt == "1":
            print("")
            uid = input(str("Enter User ID: "))
            upw = input(str("Enter Password: "))
            if uid.upper() == "ADMIN":
                if check_admin(upw):
                    admin_module()
                else:
                    print("Invalid Password!")
            else:
                if check_customer(uid, upw):
                    cur_user = uid
                    customer_module()
                else:
                    print("Invalid User ID or Password")
        elif opt == "2":
            register_customer()
        elif opt == "3":
            print("Thank you for using this software!")
            return;
        else:
            print("Invalid Option")


main()
