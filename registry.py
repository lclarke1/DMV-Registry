###############################################################################
# Author: Logan Clarke
# Program: registry.py
# Purpose: The program is command line imitation of a DMV Registry program.
# It uses python and SQLite to create a database with all relevant entries
# and supports multiple functionalities to Update that database. There are
# two user type, registry agent and police officer. The functionalities
# displayed are dependent on the login used.
#
# Registry Agent Login             Police Officer Login
# Username: lclarke1               Username: wdisney
# Password: password               Password: password
#
# Registry Agent Operations
#
# a - Register Birth               g - View all database users
# b - Register Marriage            h - View all database persons
# c - Renew Vehicle Registration   i - View Births
# d - Process a bill of Sale       j - View Marriages
# e - Process a ticket payment     k - View Vehicle Registrations
# f - Get a drivers abstract       l - View Ticket Payments
#
# Police Officer Operations
#
# a - Issue a ticket               g - View all tickets
# b - Find a car owner             h - View all registrations
#
#################################################################################


import sqlite3
import datetime
from datetime import date
import time
import re

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()

    return


def drop_tables():
    global connection, cursor

    drop_demeritNotices = "DROP TABLE IF EXISTS demeritNotices; "
    drop_tickets = "DROP TABLE IF EXISTS tickets; "
    drop_registrations = "DROP TABLE IF EXISTS registrations; "
    drop_vehicles = "DROP TABLE IF EXISTS vehicles; "
    drop_marriages = "DROP TABLE IF EXISTS marriages; "
    drop_births = "DROP TABLE IF EXISTS births; "
    drop_persons = "DROP TABLE IF EXISTS persons; "
    drop_payments = "DROP TABLE IF EXISTS payments; "
    drop_users = "DROP TABLE IF EXISTS users; "

    cursor.execute(drop_demeritNotices)
    cursor.execute(drop_payments)
    cursor.execute(drop_tickets)
    cursor.execute(drop_registrations)
    cursor.execute(drop_vehicles)
    cursor.execute(drop_marriages)
    cursor.execute(drop_births)
    cursor.execute(drop_users)
    cursor.execute(drop_persons)

    return


def define_tables():

    persons_query = ''' 
    create table persons (
    fname		char(12),
    lname		char(12),
    bdate		date,
    bplace	char(20), 
    address	char(30),
    phone		char(12),
    primary key (fname, lname)
    );
   '''

    payments_query = '''
  create table payments (
  tno           int,
  pdate         date,
  amount        real,
  primary key   (tno,pdate),
  foreign key   (tno) references tickets
  );
  '''

    users_query = '''
  create table users (
  uid            char(12),
  pwd            char(12),
  utype          char(12),
  fname          char(12),
  lname          char(12),
  city           char(20),
  primary key    (uid),
  foreign key    (fname,lname) references persons
  );
  '''

    births_query = '''
 
  create table births (
  regno		int,
  fname		char(12),
  lname		char(12),
  regdate	date,
  regplace	char(20),
  gender	char(1),
  f_fname	char(12),
  f_lname	char(12),
  m_fname	char(12),
  m_lname	char(12),
  primary key (regno),
  foreign key (fname,lname) references persons,
  foreign key (f_fname,f_lname) references persons,
  foreign key (m_fname,m_lname) references persons
  );
 
  '''

    marriages_query = '''
  create table marriages (
  regno		int,
  regdate	date,
  regplace	char(20),
  p1_fname	char(12),
  p1_lname	char(12),
  p2_fname	char(12),
  p2_lname	char(12),
  primary key (regno),
  foreign key (p1_fname,p1_lname) references persons,
  foreign key (p2_fname,p2_lname) references persons
  );

  '''

    vehicles_query = '''
  
  create table vehicles (
  vin		char(5),
  make		char(10),
  model		char(10),
  year		int,
  color		char(10),
  primary key (vin)
  );

  '''

    registrations_query = ''' 

  create table registrations (
  regno		int,
  regdate	date,
  expiry	date,
  plate		char(7),
  vin		  char(5), 
  fname		char(12),
  lname		char(12),
  primary key (regno),
  foreign key (vin) references vehicles,
  foreign key (fname,lname) references persons
  );

  '''

    tickets_query = '''
  
  create table tickets (
  tno		int,
  regno		int,
  fine		int,
  violation	text,
  vdate		date,
  primary key (tno),
  foreign key (regno) references registrations
  );

  '''

    demeritNotices_query = '''
  create table demeritNotices (
  ddate		date, 
  fname		char(12), 
  lname		char(12), 
  points	int, 
  desc		text,
  primary key (ddate,fname,lname),
  foreign key (fname,lname) references persons
  );

  '''

    cursor.execute(demeritNotices_query)
    cursor.execute(tickets_query)
    cursor.execute(registrations_query)
    cursor.execute(vehicles_query)
    cursor.execute(marriages_query)
    cursor.execute(births_query)
    cursor.execute(users_query)
    cursor.execute(payments_query)
    cursor.execute(persons_query)

    return


def insert_data():
    global connection, cursor

    #users(uid, pwd, utype, fname, lname, city)
    insert_users = '''
                      INSERT INTO users(uid, pwd, utype, fname, lname, city) VALUES
                          ('jwick', 'password', 'a','John', 'Wick','Edmonton'),             
                          ('wdisney', 'password','o','Walt','Disney','Edmonton');
                 '''

    #persons(fname, lname, bdate, bplace, address, phone)
    insert_persons = '''
                          INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES
                                  ('John', 'Wick', '1998-02-19', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545'),                            
                                  ('Micky', 'Mouse', '1958-12-11', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545'),
                                  ('Minnie', 'Mouse', '1958-03-11', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545'),                                
                                  ('Donald', 'Duck', '1958-02-19', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545'),
                                  ('Daisy', 'Duck', '1958-05-29', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545'),
                                  ('Walt', 'Disney', '1958-09-10', 'Edmonton, CA', 'Edmonton, CA', '312-555-5545');
                          '''
    #births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
    insert_births = '''
                    INSERT INTO  births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname) VALUES
                          (1,'Micky', 'Mouse', '1958-04-14', 'Edmonton, CA', 'M', 'Walt', 'Disney', 'Walt', 'Disney'),
                          (2,'Minnie', 'Mouse', '1958-02-20', 'Edmonton, CA', 'F', 'Walt', 'Disney', 'Walt', 'Disney');
                    '''
    #marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
    insert_marriages = '''
                      INSERT INTO marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname) VALUES
                        (1,'1978-04-19','Edmonton, CA','Micky','Mouse','Minnie','Mouse')

                      '''
    # vehicles(vin,make,model,year,color)
    insert_vehicles = ''' 
                    INSERT INTO vehicles(vin,make,model,year,color) VALUES
                    ('210', 'Tesla', 'Model 3', 2019, 'black'),
                    ('220', 'Tesla', 'Model 3', 2019, 'red'),
                    ('230', 'Mercedes', 'Benz', 2016, 'black'),
                    ('240', 'Mercedes', 'Benz', 2018, 'black');
  
                    '''
    #registrations(regno, regdate, expiry, plate, vin, fname, lname)
    insert_registrations = '''
                         INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES
                         ('300', '2016-01-01', '2016-12-19', 'jko127', '230', 'Donald', 'Duck'),
                         ('301', '2019-04-28', '2019-10-19', 'hje782', '210', 'Donald', 'Duck'),
                         ('302', '2019-04-28', '2019-11-03', 'hje782', '220', 'Daisy', 'Duck'),
                         ('303', '2019-01-01', '2019-12-19', 'jko128', '230', 'Micky', 'Mouse'),
                         ('304', '2019-01-01', '2019-12-03', 'jko129', '240', 'Minnie', 'Mouse');
                          
                          '''
    # tickets(tno,regno,fine,violation,vdate)
    insert_tickets = '''
                      INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES
                      ('110', '302', 300, 'ran a red light', '2019-04-29'),      
                      ('112', '304', 100, 'speeding', '2019-09-09');
                    '''

    #payments(tno, pdate, amount)
    insert_payments = ''' 
                    INSERT INTO payments(tno, pdate, amount) VALUES
                    ('110','2019-03-21',100),                
                    ('112','2019-09-29',50);
                    '''

    #demeritNotices(ddate, fname, lname, points, desc)
    insert_demerits = ''' 
                  INSERT INTO demeritNotices(ddate, fname, lname, points, desc) VALUES
                  ('2018-12-22', 'Daisy', 'Duck', 2, 'ran a red light'),
                  ('2017-12-12', 'Minnie', 'Mouse', 5, 'speeding');

                  '''

    cursor.execute(insert_persons)
    cursor.execute(insert_users)
    cursor.execute(insert_births)
    cursor.execute(insert_marriages)
    cursor.execute(insert_vehicles)
    cursor.execute(insert_registrations)
    cursor.execute(insert_tickets)
    cursor.execute(insert_payments)
    cursor.execute(insert_demerits)
    connection.commit()
    return


def get_username_from_user():
    username = input("Enter Username: ")
    return username


def get_password_from_user():
    password = input("Enter Password: ")
    return password


def database_login():

    login = "y"

    while login != "n":
        login = input("Login? (y= Yes, n = No): ")
        if login == "n":
            break
        elif login == "y":
            username = get_username_from_user()
            password = get_password_from_user()
            if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
                cursor.execute(
                    'SELECT * FROM users WHERE uid=? and pwd=?;', (username, password))
                result = cursor.fetchone()
                if result is not None:
                    print("\n************* Login Success! *************")
                    if result[2] == "a":
                        agent_menu(result)
                        continue
                    elif result[2] == "o":
                        officer_menu(result)
                        continue
                    break
                else:
                    print("\nInvalid Login Credentials! ")
    return


def officer_menu(result):

    command = "z"
    while command != "x":
        print("\nIssue a ticket = a , Find a car owner = b , View tickets = c , View registrations = d\n")
        command = input("Enter a command or x to exit: ")
        if command == "a":
            issue_ticket()
            print("\n************* Ticket has now been issued *************")
        elif command == "b":
            find_owner()
            print("\n************* Car Owner has been found *************")
        elif command == "c":
            cursor.execute('SELECT * from tickets;')
            print("\n", cursor.fetchall())
        elif command == "d":
            cursor.execute('SELECT * from registrations;')
            print("\n", cursor.fetchall())

    return


def issue_ticket():

    while True:
        inp = input("Enter Registration Num(Type 'exit' to exit): ")
        if type(inp) == str:
            if inp.lower() == 'exit':
                break
        regnum = inp
        cursor.execute(
            'SELECT vin,fname,lname FROM registrations WHERE regno=?', (regnum,))
        out = cursor.fetchone()
        if out == None:
            print("Invalid Registration Num")
            continue
        vin = out[0]
        cursor.execute(
            'SELECT make,model,year,color FROM vehicles WHERE vin=?', (vin,))
        out2 = cursor.fetchone()
        out = out + out2
        print(out)
        inp1 = input(
            "Enter violation date(yyyy-mm-dd)[for today as date, enter nothing]: ")
        if inp1 == '':
            inp1 = date.today()
        else:
            try:
                datetime.datetime.strptime(inp1, '%Y-%m-%d')
            except ValueError:
                print("Incorrect date format, should be yyyy-mm-dd")
                continue
        inp2 = input("Enter violation Description: ")
        inp3 = input("Fine amount: ")
        try:
            int(inp3)
        except Exception:
            print("Fine amount needs to be a number")
            continue
        cursor.execute('SELECT max(tno) FROM tickets')
        tno = cursor.fetchone()
        tno = tno[0] + 1
        cursor.execute("INSERT INTO tickets VALUES (?,?,?,?,?)",
                       (tno, regnum, inp3, inp2, inp1))
        connection.commit()

    return


def find_owner():

    def check_value(inp, string, type):
        if inp != '':
            string += f' and {type}="{inp}"'
        return string
    command = 'SELECT count(distinct vin) FROM vehicles WHERE 1=1'
    make = input("Input Make(can enter nothing): ")
    command = check_value(make, command, 'make')
    model = input("Input Model: ")
    command = check_value(model, command, 'model')
    year = input("Input Year(yyyy-mm-dd): ")
    command = check_value(year, command, 'year')
    colour = input("Input Colour: ")
    command = check_value(colour, command, 'color')
    plate = input("Input Plate: ")
    command = check_value(plate, command, 'plate')
    print(command)
    cursor.execute(command)
    count = cursor.fetchone()
    if count[0] >= 4:
        command = 'SELECT make,model,year,color,vin FROM vehicles WHERE 1=1'
        command = check_value(make, command, 'make')
        command = check_value(model, command, 'model')
        command = check_value(year, command, 'year')
        command = check_value(colour, command, 'color')
        cursor.execute(command)
        out = cursor.fetchall()
        command2 = 'select r.plate from registrations r where r.vin in (' + \
            command + ')'
        print(command2)
        cursor.execute(command2)
        plate = cursor.fetchall
        for i, e in enumerate(plate):
            out[i] = out[i] + e
        print(out)
        for i, element in enumerate(out, start=1):
            print(
                f'Car{i}; Make:{element[0]} Model:{element[1]} Year:{element[2]} Color:{element[3]}')
    else:
        pass

    return


def print_agent_menu():

    print("\nRegister birth = a , Register marriage = b , Renew vehicle registration = c")
    print("Process bill of sale = d, Process payment = e , Get a driver abstract= f")
    print("\nView users = g, View persons = h , View births= i, View marriages =j")
    print("View vehicle registrations = k , View tickets = l , View Payments = m \n")
    return


def agent_menu(result):

    command = "z"

    while command != "x":

        print_agent_menu()
        command = input("Enter a command or x to exit: ")

        if command == "a":
            register_birth(result)
            print("\n************* Birth has now been registered *************")
        elif command == "b":
            register_marriage(result)
            print("\n************* Mariage has now been registered *************")
        elif command == "c":
            c1 = renew_vehicle()
            if c1 == 1:
                print(
                    "\n************* Vehicle registrations has now been renewed *************")
            elif c1 == -1:
                print("\n************* Registration Number not found *************")
        elif command == "d":
            d1 = process_bill()
            if d1 == 1:
                print("\n************* Bill of sale has been processed *************")
            elif d1 == -1:
                print(
                    "\n************* Bill of sale has NOT been processed *************")
        elif command == "e":
            e1 = process_payment()
            if e1 == 1:
                print(
                    "\n************* Ticket payment has now been procesed *************")
            elif e1 == -1:
                print(
                    "\n************* Ticket payment has NOT been procesed *************")
        elif command == "f":
            f1 = get_driver_abstract()
            if f1 == 1:
                print(
                    "\n************* Drivers abstract has now been returned *************")
            elif f1 == -1:
                print("\n************* Driver not found or Clean Record *************")
        elif command == "g":
            cursor.execute('SELECT * from users;')
            print("\n", cursor.fetchall())
        elif command == "h":
            cursor.execute('SELECT * from persons;')
            print("\n", cursor.fetchall())
        elif command == "i":
            cursor.execute('SELECT * from births;')
            print("\n", cursor.fetchall())
        elif command == "j":
            cursor.execute('SELECT * from marriages;')
            print("\n", cursor.fetchall())
        elif command == "k":
            cursor.execute('SELECT * from registrations;')
            print("\n", cursor.fetchall())
        elif command == "l":
            cursor.execute('SELECT * from tickets;')
            print("\n", cursor.fetchall())
        elif command == "m":
            cursor.execute('SELECT * from payments;')
            print("\n", cursor.fetchall())
        elif command != "x":
            print("\n************* Command not found *************")

    return


def get_newborn_info():
    # n=[fname,lname,gender,birthdate,birthplace,f_fname,f_lname,m_fname,m_lname]
    n = []
    while True:
        fname = input("\nPlease enter newborn's first name: ")
        if re.match("^[A-Za-z_']*$", fname):
            fname = fname.lower()
            fname = fname.capitalize()
            n.append(fname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        lname = input("\nPlease enter newborn's last name: ")
        if re.match("^[A-Za-z_']*$", lname):
            lname = lname.lower()
            lname = lname.capitalize()
            n.append(lname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        gender = input(
            "\nPlease enter newborn's gender ( M= Male , F=Female ): ")
        if gender == "M" or gender == "F":
            n.append(gender)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        bdate = input(
            "\nPlease enter newborn's birth date(format like yyyy-mm-dd): ")
        try:
            datetime.datetime.strptime(bdate, '%Y-%m-%d')
            n.append(bdate)
            break
        except ValueError:
            print("Incorrect date format, should be yyyy-mm-dd")
            continue

    while True:
        bplace = input("\nPlease enter newborn's city of birth place: ")
        if re.match("^[A-Za-z_ ,]*$", bplace):
            n.append(bplace)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        f_fname = input("\nPlease enter newborn's father's first name: ")
        if re.match("^[A-Za-z_]*$", f_fname):
            f_fname = f_fname.lower()
            f_fname = f_fname.capitalize()
            n.append(f_fname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        f_lname = input("\nPlease enter newborn's father's last name: ")
        if re.match("^[A-Za-z_]*$", f_lname):
            f_lname = f_lname.lower()
            f_lname = f_lname.capitalize()
            n.append(f_lname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        m_fname = input("\nPlease enter newborn's mother's first name: ")
        if re.match("^[A-Za-z_]*$", m_fname):
            m_fname = m_fname.lower()
            m_fname = m_fname.capitalize()
            n.append(m_fname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        m_lname = input("\nPlease enter newborn's Mother's last name: ")
        if re.match("^[A-Za-z_]*$", m_lname):
            m_lname = m_lname.lower()
            m_lname = m_lname.capitalize()
            n.append(m_lname)
            break
        else:
            print("\nInvalid Input! ")

    return n


def get_person_info():
    p = []
    while True:
        bdate = input("\nPlease enter birth date(format like yyyy-mm-dd): ")
        try:
            datetime.datetime.strptime(bdate, '%Y-%m-%d')
            p.append(bdate)
            break
        except ValueError:
            print("Incorrect date format, should be yyyy-mm-dd")
            continue

    while True:
        bplace = input("\nPlease enter birth place: ")
        if re.match("^[A-Za-z_ ,]*$", bplace):
            p.append(bplace)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        address = input("\nPlease enter address: ")
        if re.match("^[A-Za-z_ ,]*$", address):
            p.append(address)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        phone = input("\nPlease enter phone(format like ###-###-####): ")
        if re.match("^[0-9-]*$", phone):
            p.append(phone)
            break
        else:
            print("\nInvalid Input! ")

    return p


def get_names():
    name = []
    while True:
        fname = input("\nFirst name: ")
        if re.match("^[A-Za-z_']*$", fname):
            fname = fname.lower()
            fname = fname.capitalize()
            name.append(fname)
            break
        else:
            print("\nInvalid Input! ")

    while True:
        lname = input("\nLast name: ")
        if re.match("^[A-Za-z_']*$", lname):
            lname = lname.lower()
            lname = lname.capitalize()
            name.append(lname)
            break
        else:
            print("\nInvalid Input! ")

    return name


def register_birth(result):

    cursor.execute('Select count(*) from births;')
    count = cursor.fetchone()
    regno = count[0]+1
    regdate = time.strftime("%Y-%m-%d")
    regplace = result[5]

    n = get_newborn_info()

    cursor.execute(
        'SELECT * FROM persons WHERE fname=? and lname=?;', (n[7], n[8]))
    mother = cursor.fetchone()
    if mother is not None:
        address = mother[4]
        phone = mother[5]
    else:
        print("\nPlease enter additional information for the newborn's mother")
        p1 = get_person_info()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (n[7], n[8], p1[0], p1[1], p1[2], p1[3]))
        address = p1[2]
        phone = p1[3]

    cursor.execute(
        'SELECT * FROM persons WHERE fname=? and lname=?;', (n[5], n[6]))
    father = cursor.fetchone()
    if father is None:
        print("\nPlease enter additional information for the newborn's father")
        p2 = get_person_info()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (n[5], n[6], p2[0], p2[1], p2[2], p2[3]))

    cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                   (n[0], n[1], n[3], n[4], address, phone))

    cursor.execute("INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (regno, n[0], n[1], regdate, regplace, n[2], n[5], n[6], n[7], n[8]))

    connection.commit()

    return


def register_marriage(result):
    cursor.execute('Select max(regno) from marriages;')
    m_count = cursor.fetchone()
    m_regno = m_count[0]+1
    m_regdate = time.strftime("%Y-%m-%d")
    m_regplace = result[5]
    print("\nPlease enter the name for partner 1")
    name1 = get_names()
    print("\nPlease enter the name for partner 2")
    name2 = get_names()

    cursor.execute(
        'SELECT * FROM persons WHERE fname=? and lname=?;', (name1[0], name1[1]))
    partner1 = cursor.fetchone()
    if partner1 is None:
        print("\nPlease enter additional information for partner 1 ")
        p1 = get_person_info()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (name1[0], name1[1], p1[0], p1[1], p1[2], p1[3]))

    cursor.execute(
        'SELECT * FROM persons WHERE fname=? and lname=?;', (name2[0], name2[1]))
    partner2 = cursor.fetchone()
    if partner2 is None:
        print("\nPlease enter additional information for partner 2 ")
        p2 = get_person_info()
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?)",
                       (name2[0], name2[1], p2[0], p2[1], p2[2], p2[3]))

    cursor.execute("INSERT INTO marriages VALUES(?,?,?,?,?,?,?)", (m_regno,
                   m_regdate, m_regplace, name1[0], name1[1], name2[0], name2[1]))
    connection.commit()
    return


def renew_vehicle():

    v_regno = input("Please enter the vehicle registration number: ")
    if re.match("^[A-Za-z0-9_]*$", v_regno):
        cursor.execute(
            'SELECT * FROM registrations WHERE regno=?;', (v_regno,))
        v_result = cursor.fetchone()
        if v_result is not None:
            if v_result[2] == time.strftime("%Y-%m-%d"):
                print("\nExpring today! ")
                cursor.execute(
                    "UPDATE registrations SET expiry = date('now','+1 year') WHERE regno =?;", (v_regno,))
            elif v_result[2] < time.strftime("%Y-%m-%d"):
                print("\nExpired! ")
                cursor.execute(
                    "UPDATE registrations SET expiry = date('now','+1 year') WHERE regno =?;", (v_regno,))
            elif v_result[2] > time.strftime("%Y-%m-%d"):
                print("\nStill Valid! ")
                cursor.execute(
                    "UPDATE registrations SET expiry = date(expiry,'+1 year') WHERE regno =?;", (v_regno,))
            connection.commit()
            return 1

    return -1


def process_bill():

    b_vin = input("\nPlease enter the vehicles vin: ")
    cursor.execute('SELECT * from vehicles WHERE vin=?;', (b_vin,))
    b_result = cursor.fetchone()
    if b_result is None:
        print("\nVehicle Not Found! ")
        return -1
    else:
        print("\nPlease enter the name for current owner")
        name1 = get_names()
        print("\nPlease enter the name for new owner")
        name2 = get_names()
        cursor.execute(
            'Select * from registrations WHERE vin=? ORDER BY expiry DESC;', (b_vin,))
        r1_result = cursor.fetchone()
        cursor.execute(
            'SELECT * from persons WHERE fname=? AND lname=?', (name2[0], name2[1]))
        r2_result = cursor.fetchone()
        if r1_result is None or r2_result is None:
            print("Transfer cannot be made!")
            return -1
        elif r1_result[5] != name1[0] or r1_result[6] != name1[1]:
            print("\nTransfer cannot be made!")
            return -1
        else:
            cursor.execute('SELECT max(regno) FROM registrations')
            new_regno = 425
            print(r1_result)
            cursor.execute('''
      UPDATE registrations SET fname=? ,lname=?, regdate=date('now'), 
      expiry = date('now','+1 year'), regno=? WHERE vin=? AND expiry=?
      ''', (name2[0], name2[1], new_regno, b_vin, r1_result[2]))
            connection.commit()
    return 1


def process_payment():
    try:
        tno = input("Enter Valid Ticket number: ")
        cursor.execute('SELECT * FROM tickets WHERE tno=?', (tno,))
        out = cursor.fetchone()
        if out == None:
            print("Invalid Ticket Number")
        else:
            print(out)
            d = date.today()
            topay = out[2]
            print("reached")
            print(f'Payment Amount : {topay}')
            paid = input("How much do you want to pay?(type exit to exit) ")
            if paid.lower() == 'exit':
                raise TypeError
            else:
                paid = int(paid)
                if paid > topay:
                    pass
                topay -= paid
                inptup = (str(topay), str(out[0]),)

                cursor.execute('UPDATE tickets SET fine=? where tno=?', inptup)
                inptup = (out[0], str(d), paid)
                cursor.execute('Insert INTO payments VALUES (?,?,?)', inptup)
                connection.commit()
    except TypeError:
        print("Invalid Input")
        return -1
    return 1


def get_driver_abstract():
    try:
        fname = input('First Name: ').lower().capitalize()
        lname = input('Last Name: ').lower().capitalize()

        # Tickets Total
        cursor.execute(
            'SELECT regno FROM registrations WHERE fname=? and lname=? COLLATE NOCASE', (fname, lname))
        out = cursor.fetchall()
        if out == None:
            raise Exception
        regnum = out[0]

        ticketsT = 0
        for element in out:
            cursor.execute(
                'select count(tno) FROM tickets WHERE regno=?', element)
            t = cursor.fetchone()
            ticketsT += t[0]

        # List Tickets full
        ans = input("Do you want comprehensive ticket report?(y,n)")
        if type(ans) != str:
            pass
        else:
            ans = ans.lower()
            outList = []
            cursor.execute(
                'select tno,violation,vdate,fine,regno FROM tickets WHERE regno=?', regnum)
            out = cursor.fetchall()
            for element in out:
                regno = str(element[4])
                cursor.execute(
                    'select vin FROM registrations WHERE regno=?', (regno,))
                vin = cursor.fetchone()
                cursor.execute(
                    'select make,model FROM vehicles WHERE vin=?', (vin[0],))
                car = cursor.fetchone()
                fullDet = element + car
                outList.append(fullDet)
            res = outList
            print(res)

        # Lifetime Demerits
        cursor.execute(
            'SELECT points FROM demeritNotices WHERE fname=? and lname=?', (fname, lname))
        out = cursor.fetchall()
        print(out)
        demerits = 0
        points = 0
        for element in out:
            points += element[0]
            demerits += 1
        print(f'{points}, {demerits}')

        # Only last two Years Demerits
        twoYrs = datetime.datetime.now() - datetime.timedelta(days=2*365)
        cursor.execute(
            'SELECT points FROM demeritNotices WHERE fname=? and lname=? and ddate>?', (fname, lname, twoYrs))
        out = cursor.fetchall()
        print(out)
        demerits = 0
        points = 0
        for element in out:
            points += element[0]
            demerits += 1
        print(f'{points}, {demerits}')
    except Exception:
        print("\nException Raised")
        return -1

    return 1


def main():
    global connection, cursor
    path = "./registry.db"

    connect(path)
    drop_tables()
    define_tables()
    insert_data()
    database_login()

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
