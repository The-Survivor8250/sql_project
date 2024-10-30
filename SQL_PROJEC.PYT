

# RAILWAY MANAGEMENT SYSTEM
# Importing Modules
import psycopg2 as sql  # Using psycopg2 for PostgreSQL
from random import randint

# Establishment of connection to PostgreSQL Server
print("Enter the details of your PostgreSQL Server:")
x = input("Hostname: ")
y = input("User: ")
z = input("Password: ")
dbname = input("Database Name: ")
con = sql.connect(host=x,
                  user=y,
                  password=z,
                  dbname=dbname)
con.autocommit = True
cur = con.cursor()
# Creation of Database and subsequent Tables
# PostgreSQL requires the database to be already created before connection
# Assuming the database exists, we create tables only
s = """CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        pass VARCHAR(16),
        name VARCHAR(100),
        sex CHAR(1),
        age VARCHAR(3),
        dob DATE,
        ph_no CHAR(10)
    );"""
cur.execute(s)

s = """CREATE TABLE IF NOT EXISTS tickets (
        id INT,
        PNR INT,
        train VARCHAR(25),
        doj DATE,
        tfr VARCHAR(100),
        tto VARCHAR(100),
        PRIMARY KEY (PNR)
    );"""
cur.execute(s)
# Login Menu
def login_menu():
    print("WELCOME TO THE IRCTC PORTAL")
    print("1. Create New Account \n"
          "2. Log In \n"
          "3. Exit")
    opt = int(input("Enter your choice: "))
    if opt == 1:
        create_acc()
    elif opt == 2:
        login()
    else:
        e = input("Exit the portal? (Y/N) ")
        if e in "Nn":
            login_menu()
# Account Creation
def create_acc():
    print("Enter the details to create your account:")
    p = input("Enter your password: ")
    n = input("Enter your name: ")
    sex = input("Enter your gender (M/F/O): ")
    age = input("Enter your age: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    ph = input("Enter your contact number: ")
    s1 = """INSERT INTO accounts (pass, name, sex, age, dob, ph_no) 
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
    cur.execute(s1, (p, n, sex.upper(), age, dob, ph))
    i = cur.fetchone()[0]
    print(f"Your generated ID is: {i}")
    print("Now you may log in with your newly created account!")
    login()
# Log in to Account
def login():
    global a
    try:
        a = int(input("Enter your ID: "))
        b = input("Enter your password: ")
        s2 = "SELECT name FROM accounts WHERE id = %s AND pass = %s;"
        cur.execute(s2, (a, b))
        j = cur.fetchone()
        if j:
            print(f"Welcome back {j[0]}!")
            main_menu()
        else:
            raise ValueError
    except:
        print("Your account was not found!")
        print("You can: \n"
              "1. Try logging in again \n"
              "2. Create a new account")
        ch = input("Enter your choice: ")
        if ch == "1":
            login()
        elif ch == "2":
            create_acc()
        else:
            print("Invalid choice!")
            x1 = input("Exit the portal? (Y/N) ")
            if x1 in "Nn":
                login_menu()
# Main Menu
def main_menu():
    print("ou like to do today? \n"
          "1. Purchase a Ticket \n"
          "2. Check Ticket Status \n"
          "3. Request a refund \n"
          "4. Account SeWhat would yttings \n"
          "5. Logout \n"
          "6. Exit")
    ch1 = int(input("Enter your choice: "))
    if ch1 == 1:
        buy_ticket()
    elif ch1 == 2:
        show_ticket()
    elif ch1 == 3:
        cancel_ticket()
    elif ch1 == 4:
        account()
    elif ch1 == 5:
        login_menu()
    else:
        exit_prompt()
# Exit Prompt
def exit_prompt():
    x2 = input("Would you like to exit? (Y/N) ")
    if x2.upper() == "N":
        main_menu()
# Back to Main Menu
def back_to_main_menu():
    x3 = input("Return to the Main Menu? (Y/N) ")
    if x3.upper() == "Y":
        print("Returning to Main Menu...")
        main_menu()
# Ticket Creation
def buy_ticket():
    print("Enter details for your journey: ")
    i = a
    pnr = randint(100000, 1000000)
    print(f"Your PNR is {pnr}")
    train = input("Enter the name of the train: ")
    doj = input("Enter the date of your journey (YYYY-MM-DD): ")
    fr = input("Enter the Departing Station: ")
    to = input("Enter the Destination Station: ")
    s4 = """INSERT INTO tickets (id, PNR, train, doj, tfr, tto) 
            VALUES (%s, %s, %s, %s, %s, %s);"""
    cur.execute(s4, (i, pnr, train, doj, fr, to))
    back_to_main_menu()


# Ticket Checking
def show_ticket():
    try:
        pnr = int(input("Enter your PNR: "))
        s5 = "SELECT * FROM tickets WHERE PNR = %s;"
        cur.execute(s5, (pnr,))
        j = cur.fetchone()
        if j and j[0] == a:
            print(f"Train: {j[2]} \n"
                  f"Date of Journey: {j[3]} \n"
                  f"From: {j[4]} \n"
                  f"To: {j[5]}")
            back_to_main_menu()
        else:
            print("Unauthorized! \n"
                  "Your ID does not match the PNR of the ticket.")
            back_to_main_menu()
    except:
        ticket_not_found()
# Ask for a refund
def cancel_ticket():
    try:
        pnr = int(input("Enter the PNR number of the ticket: "))
        s2 = "SELECT id, PNR, train FROM tickets WHERE PNR = %s;"
        cur.execute(s2, (pnr,))
        j = cur.fetchone()
        if j and j[0] == a:
            print(f"PNR: {j[1]} \n"
                  f"Train: {j[2]}")
            x4 = input("Do you really want to cancel this ticket? (Y/N) ")
            if x4.upper() == "Y":
                s3 = "DELETE FROM tickets WHERE PNR = %s;"
                cur.execute(s3, (pnr,))
                print("You will be refunded shortly!")
                back_to_main_menu()
            else:
                back_to_main_menu()
        else:
            print("Unauthorized! \n"
                  "Your ID does not match the PNR of the ticket.")
            back_to_main_menu()
    except:
        ticket_not_found()
# If ticket is not found
def ticket_not_found():
    print("Ticket not found!")
    print("You can: \n"
          "1. Try entering your PNR number again \n"
          "2. Purchase a ticket \n"
          "3. Return to Main Menu \n"
          "4. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        show_ticket()
    elif ch == 2:
        buy_ticket()
    elif ch == 3:
        print("Returning to Main Menu...")
        main_menu()
    else:
        exit_prompt()
# Account settings
def account():
    print("Do you want to: \n"
          "1. Show Account details \n"
          "2. Delete Account")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        s4 = "SELECT * FROM accounts WHERE id = %s;"
        cur.execute(s4, (a,))
        j = cur.fetchone()
        print(f"ID: {j[0]} \n"
              f"Name: {j[2]} \n"
              f"Gender: {j[3]} \n"
              f"Age: {j[4]} \n"
              f"DOB: {j[5]} \n"
              f"Phone Number: {j[6]}")
        back_to_main_menu()
    elif ch == 2:
        x6 = input("Do you want to request for refund(s) for your ticket(s) too? (Y/N) ")
        if x6.upper() == "Y":
            s5 = "DELETE FROM tickets WHERE id = %s;"
            cur.execute(s5, (a,))
            print("You will be refunded shortly!")
        s6 = "DELETE FROM accounts WHERE id = %s;"
        cur.execute(s6, (a,))
        print("Account Successfully Deleted!")
        login_menu()
    else:
        back_to_main_menu()
# Calling the first function, hence starting the program
if __name__ == "__main__":
    login_menu()
