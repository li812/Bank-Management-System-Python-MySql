import math
import json
import os
from queue import Empty
import random
from datetime import datetime
from datetime import date
from os.path import exists
import mysql.connector
import pyfiglet
import random
from tabulate import tabulate
import pandas as pd
import warnings
warnings.filterwarnings('ignore')




mydb=mysql.connector.connect(host ="localhost",user="root",password="")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists bms")
mycursor.execute("use bms")
mycursor.execute("create table if not exists usertype(type_id INT NOT NULL AUTO_INCREMENT, type VARCHAR(10) NOT NULL , PRIMARY KEY (type_id))")
mycursor.execute("INSERT IGNORE INTO usertype(type_id, type) VALUES ('1', 'admin'), ('2', 'staff'), ('3', 'customer')")
mycursor.execute("create table if not exists login(login_id INT NOT NULL AUTO_INCREMENT, type_id INT NOT NULL , username VARCHAR(20) NOT NULL , password VARCHAR(20) NOT NULL , PRIMARY KEY (login_id), FOREIGN KEY (type_id) REFERENCES usertype(type_id))")
mycursor.execute("INSERT IGNORE INTO login(login_id, type_id, username, password) VALUES ('1', '1', 'admin', 'admin')")
mycursor.execute("create table if not exists customer(cus_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL , account_number varchar(20) not null ,balance int, f_name VARCHAR(50) NOT NULL , l_name VARCHAR(50) NOT NULL , email VARCHAR(50) NOT NULL ,phone_no VARCHAR(50) NOT NULL , address VARCHAR(150) NOT NULL ,city VARCHAR(50) NOT NULL,country VARCHAR(50) NOT NULL , date varchar(12), PRIMARY KEY (cus_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists staff(staff_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL , f_name VARCHAR(50) NOT NULL , l_name VARCHAR(50) NOT NULL , email VARCHAR(50) NOT NULL ,phone_no VARCHAR(50) NOT NULL , address VARCHAR(150) NOT NULL ,city VARCHAR(50) NOT NULL, salary int, PRIMARY KEY (staff_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists freezed(f_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL, date varchar(12), PRIMARY KEY (f_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists transactions(trans_id int not null auto_increment, cus_id int not null, account_number varchar(20),balance int, date varchar(12), time varchar(12), PRIMARY KEY (trans_id), FOREIGN KEY (cus_id) REFERENCES customer(cus_id))")
mydb.commit()

# sql_query = pd.read_sql_query(''' 
#                               select * from customer
#                               '''
#                               ,mydb)
# df = pd.DataFrame(sql_query)
# filenm=input("Enter file name:")
# file = filenm+".csv"
# df.to_csv (file, index = False)

ascii_banner = pyfiglet.figlet_format("BANK MANGEMENT SYSTEM")
print("_________________________________________________________________")
print(ascii_banner)
print("_________________________________________________________________\n")

today = date.today()
stoday = str(today)
print("Today's date:", stoday)


now = datetime.now()
current_time = now.strftime("%H:%M:%S")
stime=str(current_time)
print("Current Time =", stime)

def main():
    print("\n\n")
    while True:
        try:
            print("1 : SignUp\n2 : LogIn\n3 : Quit")
            print("Press 1 to SignUp, Press 2 to LogIn and Press 3 to quit():")
            ch=int(input("====>>> "))
        except:
            main()
#start of sign_up
        if ch==1:
            def signup():
                account_number = str(random.randint(1200000000000000,1999999999999999))
                f_name = input("First Name :")
                l_name =  input("Last Name :")
                email = input("Email :")
                username = input("Username :")
                password= input("Password :")
                balance = int(0)
                phone_no = input("Phone Number :")
                address = input("Address :")
                city = input("City :")
                country = input("Country :")
                today = date.today()
                mycursor.execute("insert into login(type_id,username,password) values('3','"+username+"','"+password+"')")
                mydb.commit()
                getid1="SELECT login_id FROM login WHERE username='"
                getid2="';"
                get_login_id = getid1+username+getid2
                mycursor.execute(get_login_id)
                data = mycursor.fetchone()
                login_id = str(data[0])
                sql = "INSERT INTO customer (login_id,f_name,l_name,email,phone_no,address,city,country,account_number,date,balance) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s)"
                val = (login_id,f_name,l_name,email,phone_no,address,city,country,account_number,today,balance)
                mycursor.execute(sql,val)
                try:
                    mydb.commit()
                    print("\nAccount created successfully\n")
                except:
                    print("Failed to create new")
                    mycursor.execute("delete from login where login_id='"+login_id+"'")
                    mydb.commit()
            signup()
#end of sign_up

#start of log_in
        elif ch==2:
            def login():
                username=input("USERNAME:")
                mycursor.execute("select username from login where username='"+username+"'")
                usn=mycursor.fetchone()
                if usn is not None:
                    print("\n=========VALID USERNAME..!=========\n")
                elif usn is None:
                    print("\n=========INVALID USERNAME..!=========\n")
                    main()
                mycursor.execute("select login_id from login where username='"+username+"'")
                lix=mycursor.fetchone()
                li = str(lix[0])
                mycursor.execute("select f_id from freezed where login_id='"+li+"'")
                ft=mycursor.fetchone()
                if ft is not None:
                    print("\nYour account has been freezed please contact bank for more information.\n")
                    main()
                pwi=input("PASSWORD:")
                mycursor.execute("select password from login where username='"+username+"'")
                pws=mycursor.fetchone()
                password=str(pws[0])
                if password==pwi:
                    mycursor.execute("select type_id from login where password='"+pwi+"'")
                    type=mycursor.fetchone()
                    usertype = type[0]
                    
################################################################################################

###########################################
###########################################
########### Functions of admin ###########
                    def create_staff():
                        f_name = input("First Name :")
                        l_name =  input("Last Name :")
                        email = input("Email :")
                        username = input("Username :")
                        password= input("Password :")
                        phone_no = input("Phone Number :")
                        address = input("Address :")
                        city = input("City :")
                        today = date.today()
                        salary = input("Salary :")
                        mycursor.execute("insert into login(type_id,username,password) values('2','"+username+"','"+password+"')")
                        mydb.commit()
                        getid1="SELECT login_id FROM login WHERE username='"
                        getid2="';"
                        get_login_id = getid1+username+getid2
                        mycursor.execute(get_login_id)
                        data = mycursor.fetchone()
                        login_id = str(data[0])
                        sql = "INSERT INTO staff (login_id,f_name,l_name,email,phone_no,address,city,salary) VALUES (%s, %s, %s,%s, %s,%s, %s,%s)"
                        val = (login_id,f_name,l_name,email,phone_no,address,city,salary)
                        mycursor.execute(sql,val)
                        mydb.commit() 
                        admin()  

                    def manage_staff():

                        def show_staff():
                            mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary FROM staff;")
                            data = mycursor.fetchall()
                            h = ['Staff ID','First Name','Last Name','Phone Number','Salary']
                            print(tabulate(data,headers=h,tablefmt='psql'))
                            manage_staff()
 
                        def delete_staff():
                            mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary FROM staff;")
                            data = mycursor.fetchall()
                            h = ['Staff ID','First Name','Last Name','Phone Number','Salary']
                            print(tabulate(data,headers=h,tablefmt='psql'))
                            kill = input("Enter the Staff ID: ")
                            
                            mycursor.execute("select login_id from staff where staff_id='"+kill+"'")
                            data = mycursor.fetchone()
                            kill_id = str(data[0])
                            mycursor.execute("delete from staff where staff_id='"+kill+"'")
                            mydb.commit()
                            mycursor.execute("delete from login where login_id='"+kill_id+"'")
                            mydb.commit()
                            print("\nAccount deleted successfully")
                            mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary FROM staff;")
                            data = mycursor.fetchall()
                            h = ['Staff ID','First Name','Last Name','Phone Number','Salary']
                            print(tabulate(data,headers=h,tablefmt='psql'))
                            manage_staff()

                        print("\nWelcome to Staff Management\n")
                        print("1 > Show Staffs")
                        print("2 > Delete Staffs")

                        print("4 > Go Back\n")
                        ach = int(input("Enter your command :"))
                    
                        if ach == 1:
                            show_staff()
                        if ach == 2:
                            delete_staff()

                        

                        
                        admin()  


#######End of Functions of admin ###########
###########################################
###########################################



###########################################
###########################################
########## Functions of customer ##########

#cus_view_account_number
                    def cus_view_account_number():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        mycursor.execute("select account_number from customer where login_id='"+li+"'")
                        anx=mycursor.fetchone()
                        an = str(anx[0])
                        if an=="None":
                            print("\nYour account number is not available right now. Please try again.\n")                        
                        else:
                            print("\nYour account number is ",an,"\n")
                        customer()

#cus_check_balance
                    def cus_check_balance():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        mycursor.execute("select balance from customer where login_id='"+li+"'")
                        bax=mycursor.fetchone()
                        ba = str(bax[0])
                        if ba=="None":
                            print("\nYour account balance is zero not available\n")                        
                        else:
                            print("\nYour account balance is ",ba,"\n")
                        customer()


#cus_manage_account
                    def cus_manage_account():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        
                        #username = username
                        #login_id = li

#cus_change_password                       
                        def cus_change_password():
                            print("\nChange Password.\n")
                            mycursor.execute("select password from login where login_id='"+li+"'")
                            opassx = mycursor.fetchone()
                            opass = str(opassx[0])
                            #print(opass)
                            cpass = input("Enter old password :")
                            
                            if cpass == opass:
                                #print("w")
                                npass = input("Enter new password :")
                                ncpass = input("Please enter the new password again :")
                                
                                if npass == ncpass:
                                    mycursor.execute("UPDATE login SET password = '"+npass+"' where login_id='"+li+"'")
                                    mydb.commit()
                                    print("Password updated successfully, please login again.")
                                    main()
                                    
                                else:
                                    print("Password not updated successfully, please check the password you entered.")
                                cus_manage_account()
                                
                            else:
                                print("Password incorrect")
                            cus_manage_account()

#cus_delete_account                            
                        def cus_delete_account():
                            print("\nWelcome to account closing section. Your are about to close your account.\n")
                            mycursor.execute("select password from login where login_id='"+li+"'")
                            passx = mycursor.fetchone()
                            opass = str(passx[0])
                            #print(opass)
                            mycursor.execute("select cus_id from customer where login_id='"+li+"'")
                            cusidx = mycursor.fetchone()
                            cusid = str(cusidx[0])
                            
                            npass = input("Enter your password :")
                            
                            if npass == opass:
                                ncpass = input("Please enter your password again :")
                                
                                if opass == ncpass:
                                    mycursor.execute("delete from customer where cus_id='"+cusid+"'")
                                    mydb.commit()
                    
                                    mycursor.execute("delete from login where login_id='"+li+"'")
                                    mydb.commit()
                    
                                    print("\nAccount deleted successfully, please login again.")
                                    main()
                                    
                                else:
                                    print("\nPassword not matching, please check the password you entered.")
                                    cus_manage_account()
                        
                    
                            cus_manage_account()

#cus_freeze_account                    
                        def cus_freeze_account():
                            print("\nWelcome to account freezing section. Your are about to freeze your account.\n")
                            mycursor.execute("select password from login where login_id='"+li+"'")
                            opassx = mycursor.fetchone()
                            opass = str(opassx[0])
                            #print(opass)
                            cpass = input("Enter password :")
                    
                            if cpass == opass:
                                sql = "INSERT INTO freezed (login_id,date) VALUES (%s,%s)"
                                val = (li,stoday)
                    
                                mycursor.execute(sql,val)
                                mydb.commit()
                                print("Account freezing successfully.")
                                main()
                                
                            else:
                                print("Account freezing failed, please check the password you entered.")
                                cus_manage_account()
                        
                    
                            cus_manage_account()
                    
                        
                        print("\nWelcome to Account Management\n")
                        print("1 > Change Password")
                        print("2 > Freeze Account")
                        print("3 > Close Account")
                        print("4 > Go Back\n")
                        ach = int(input("Enter your command :"))
                    
                        if ach == 1:
                            cus_change_password()
                    
                        elif ach == 2:
                            cus_freeze_account()
                    
                        elif ach == 3:
                            cus_delete_account()
                        
                        elif ach == 4:
                            customer()
                    
                        customer()


#withdraw
                    def withdraw():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])

                        mycursor.execute("select cus_id from customer where login_id='"+li+"'")
                        cus_idx=mycursor.fetchone()
                        cus_id = str(cus_idx[0])
                        
                        mycursor.execute("select account_number from customer where login_id='"+li+"'")
                        anx=mycursor.fetchone()
                        an = str(anx[0])
                        
                        mycursor.execute("select balance from customer where login_id='"+li+"'")
                        bax=mycursor.fetchone()
                        ba = str(bax[0])
                        ba=int(ba)
                        print("\nYour current account balance is ",ba,"\n")
                        withdraw_amount = int(input("Enter the amount you wish to withdraw :"))
                        if withdraw_amount<=ba:
                            if withdraw_amount<=100000:
                                newba = ba - withdraw_amount
                                snewba=str(newba)
                                print("\nYour new account balance is",newba)
                                mycursor.execute("UPDATE customer SET balance = '"+snewba+"' where login_id='"+li+"'")
                                mydb.commit()
                                sql = "INSERT INTO transactions (cus_id,account_number,balance,date,time) VALUES (%s, %s, %s, %s, %s)"
                                val = (cus_id,an,ba,stoday,stime)
                                mycursor.execute(sql,val)
                                mydb.commit()
                                customer()
                            else:
                                print("\nSorry, the maximum withdrawal limit is 100000.")
                                withdraw()
                        else:
                            print("\nInsufficient Balance")
                            customer()


#deposit
                    def deposit():
                        
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        
                        mycursor.execute("select cus_id from customer where login_id='"+li+"'")
                        cus_idx=mycursor.fetchone()
                        cus_id = str(cus_idx[0])
                        
                        mycursor.execute("select account_number from customer where login_id='"+li+"'")
                        anx=mycursor.fetchone()
                        an = str(anx[0])
                        
                        mycursor.execute("select balance from customer where login_id='"+li+"'")
                        bax=mycursor.fetchone()
                        ba = str(bax[0])
                        ba=int(ba)
                        
                        print("\nYour current account balance is ",ba,"\n")
                        withdraw_amount = int(input("Enter the amount you wish to deposit :"))
                        newba = ba + withdraw_amount
                        snewba=str(newba)
                        print("\nYour new account balance is",newba)
                        mycursor.execute("UPDATE customer SET balance = '"+snewba+"' where login_id='"+li+"'")
                        mydb.commit()
                        sql = "INSERT INTO transactions (cus_id,account_number,balance,date,time) VALUES (%s, %s, %s, %s, %s)"
                        val = (cus_id,an,ba,stoday,stime)
                        mycursor.execute(sql,val)
                        mydb.commit()
                        customer()

#send money
                    def send_money():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        mycursor.execute("select balance from customer where login_id='"+li+"'")
                        bax=mycursor.fetchone()
                        ba = str(bax[0])
                        ba=int(ba)
                        print("\nYour current account balance is ",ba,"\n")
                        d_an = input("Enter the account number you want to send the money : ")

                        mycursor.execute("select account_number from customer where login_id='"+li+"'")
                        sanx=mycursor.fetchone()
                        san = str(sanx[0])

 #receiver login_id
                        mycursor.execute("select login_id from customer where account_number='"+d_an+"'")
                        dlix=mycursor.fetchone()
                        dli = str(dlix[0]) 
                        
                        mycursor.execute("select cus_id from customer where login_id='"+li+"'")
                        cus_id=mycursor.fetchone()
                        cus_id = str(cus_id[0])  
                        
                        mycursor.execute("select cus_id from customer where login_id='"+dli+"'")
                        dcus_id=mycursor.fetchone()
                        dcus_id = str(dcus_id[0])                                                                       #r login id --  dli
                                                                                                                    #s login id --  li
                        
                        mycursor.execute("select f_id from freezed where login_id='"+dli+"'")
                        ft=mycursor.fetchone()
                        if ft is not None:
                            print("\nYour account has been freezed please contact bank for more information.\n")
                            send_money()
                        else:
                            try:
                                mycursor.execute("select balance from customer where account_number='"+d_an+"'")
                                dbax=mycursor.fetchone()
                                dba = str(dbax[0])
                                
                                idba = int(dba)
                            except:
                                print("\nInvalid account number!\nPlease check the account number")
                                customer()
                            send_amount = int(input("Enter the amount you wish to deposit : "))
                            if send_amount<=ba:
                                if send_amount<=50000:
                                    dnewba = idba + send_amount
                                    sdnewba=str(dnewba)
                                    #print("\ndestination new account balance is",dnewba)
                                    mycursor.execute("UPDATE customer SET balance = '"+sdnewba+"' where account_number='"+d_an+"'")
                                    sql = "INSERT INTO transactions (cus_id,account_number,balance,date,time) VALUES (%s, %s, %s, %s, %s)"
                                    val = (dcus_id,d_an,sdnewba,stoday,stime)
                                    mycursor.execute(sql,val)
                                    mydb.commit()
                                    newba = ba - send_amount
                                    snewba=str(newba)
                                    print("\nYour new account balance is",newba)
                                    mycursor.execute("UPDATE customer SET balance = '"+snewba+"' where login_id='"+li+"'")
                                    mydb.commit()
                                    sql = "INSERT INTO transactions (cus_id,account_number,balance,date,time) VALUES (%s, %s, %s, %s, %s)"
                                    val = (cus_id,san,snewba,stoday,stime)
                                    mycursor.execute(sql,val)
                                    mydb.commit()
                                    customer()
                                else:
                                    print("Sorry the maximum sending limit is 50000.")
                                    send_money()
                            else:
                                print("\nInsufficient Balance")
                                customer()

#show statement
                    def show_statement():
                        mycursor.execute("select login_id from login where username='"+username+"'")
                        lix=mycursor.fetchone()
                        li = str(lix[0])
                        mycursor.execute("select cus_id from customer where login_id='"+li+"'")
                        cus_idx=mycursor.fetchone()
                        cus_id = str(cus_idx[0])
                        print("\n")
                        mycursor.execute("SELECT trans_id,date,time,balance FROM transactions where cus_id='"+cus_id+"'")
                        data = mycursor.fetchall()
                        h = ['Transaction ID','Date','Time','Balance']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        print("1 > To export csv")
                        print("2 > To go back")
                        pr = int(input("-->"))
                        if pr == 1:
                            sq="SELECT * FROM transactions where cus_id='"+cus_id+"'"
                            
                            sql_query = pd.read_sql_query(sq,mydb)
                            df = pd.DataFrame(sql_query)
                            filenm=input("Enter file name:")
                            csvfile = filenm+".csv"
                            df.to_csv (csvfile, index = False)
                            customer()
                        if pr == 2:
                            customer()
                            
                        customer()


######End of Functions of customer ########
###########################################
###########################################



                        
                        



###########################################
###########################################
########## Functions of Staff ###########
                    def search_cus():
                        print("1 > Search by Account Number")
                        print("2 > Search by Name")
                        print("3 > go back")
                        ss = int(input("---> "))

                        if ss == 1:
                            an = input("Enter the account_number :")
                            mycursor.execute("SELECT * FROM customer where account_number='"+an+"'")
                            data = mycursor.fetchall()
                            number_of_elements = len(data)
                            if number_of_elements > 0:
                                h = ['cus_id','login_id','account_number','balance','first name','last name','email','phone_no','address','city','country','date']
                                print(tabulate(data,headers=h,tablefmt='psql'))
                                print("\n1 > To export csv")
                                print("2 > To go back")
                                pr = int(input("-->"))
                                if pr == 1:
                                    sq="SELECT * FROM customer where account_number='"+an+"'"
                                    print(sq)
                                    sql_query = pd.read_sql_query(sq,mydb)
                                    df = pd.DataFrame(sql_query)
                                    filenm=input("Enter file name:")
                                    csvfile = filenm+".csv"
                                    df.to_csv (csvfile, index = False)
                                    search_cus()
                                if pr == 2:
                                    search_cus()
                            else:
                                print("Account not found")
                                search_cus()
                        if ss == 2:
                            nm = input("Enter the name of the customer")
                            mycursor.execute("SELECT * FROM customer where f_name='"+nm+"' or l_name='"+nm+"'")
                            data = mycursor.fetchall()
                            number_of_elements = len(data)
                            if number_of_elements > 0:
                                h = ['cus_id','login_id','account_number','balance','first name','last name','email','phone_no','address','city','country','date']
                                print(tabulate(data,headers=h,tablefmt='psql'))
                                print("\n1 > To export csv")
                                print("2 > To go back")
                                pr = int(input("-->"))
                                if pr == 1:
                                    sq="SELECT * FROM customer where f_name='"+nm+"' or l_name='"+nm+"'"
                                    
                                    sql_query = pd.read_sql_query(sq,mydb)
                                    df = pd.DataFrame(sql_query)
                                    filenm=input("Enter file name:")
                                    csvfile = filenm+".csv"
                                    df.to_csv (csvfile, index = False)
                                    search_cus()
                                if pr == 2:
                                    search_cus()
                                search_cus()
                            else:
                                print("Account not found")
                                search_cus()
                        if ss == 3:
                            staff()
                        else:
                            staff()

                    def manage_freezed():
                        print("1 > Show freezed account")
                        print("2 > Break Freeze")
                        print("3 > Freeze account")
                        print("4 > go back")
                        ss = int(input("---> "))

                        if ss == 1:
                            mycursor.execute("SELECT * FROM customer WHERE login_id IN (SELECT login_id FROM freezed);")
                            data = mycursor.fetchall()
                            number_of_elements = len(data)
                            if number_of_elements > 0:
                                h = ['cus_id','login_id','account_number','balance','first name','last name','email','phone_no','address','city','country','date']
                                print(tabulate(data,headers=h,tablefmt='psql'))
                                print("\n1 > To export csv")
                                print("2 > To go back")
                                pr = int(input("-->"))
                                if pr == 1:
                                    sq="SELECT * FROM customer WHERE login_id IN (SELECT login_id FROM freezed);"
                                    
                                    sql_query = pd.read_sql_query(sq,mydb)
                                    df = pd.DataFrame(sql_query)
                                    filenm=input("Enter file name:")
                                    csvfile = filenm+".csv"
                                    df.to_csv (csvfile, index = False)
                                    manage_freezed()
                                if pr == 2:
                                    manage_freezed()
                            else:
                                print("\nNo one has freezed yet.\n")
                                manage_freezed()

                        elif ss == 2:
                            mycursor.execute("SELECT * FROM customer WHERE login_id IN (SELECT login_id FROM freezed);")
                            data = mycursor.fetchall()
                            number_of_elements = len(data)
                            if number_of_elements > 0:
                                h = ['cus_id','login_id','account_number','balance','first name','last name','email','phone_no','address','city','country','date']
                                print(tabulate(data,headers=h,tablefmt='psql'))

                                kill_freeze = input("Enter the login_id of the customer to break freeze: ")

                                try:
                                    mycursor.execute("DELETE FROM freezed WHERE login_id = '"+kill_freeze+"'")
                                    mydb.commit()

                                except:
                                    print("Enter valid login_id!")
                                manage_freezed()
                                
                                
                            else:
                                print("\nNo one has freezed yet.\n")
                                manage_freezed()

                        elif ss == 3:
                            print("All customers.\n")
                            mycursor.execute("SELECT * FROM customer;")
                            data = mycursor.fetchall()
                            number_of_elements = len(data)
                            if number_of_elements > 0:
                                h = ['cus_id','login_id','account_number','balance','first name','last name','email','phone_no','address','city','country','date']
                                print(tabulate(data,headers=h,tablefmt='psql'))

                                freeze = input("Enter the login_id of the customer to freeze: ")
                                try:
                                    sql = "INSERT INTO freezed (login_id,date) VALUES (%s,%s)"
                                    val = (freeze,stoday)
                        
                                    mycursor.execute(sql,val)
                                    mydb.commit()
                                    print("Account freezing successfully.")

                                    manage_freezed()
                                except:
                                    print("Something went wrong!")
                                    manage_freezed()
                                
                                
                            else:
                                print("\nNo one has freezed yet.\n")
                                manage_freezed()
                        
                        elif ss == 4:
                            staff()

                        else:
                            staff()

                    def get_statements():
                        an = input("Enter the account_number :")
                        print("\n")
                        mycursor.execute("SELECT trans_id,date,time,balance FROM transactions where account_number='"+an+"'")
                        data = mycursor.fetchall()
                        h = ['Transaction ID','Date','Time','Balance']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        print("1 > To export csv")
                        print("2 > To go back")
                        pr = int(input("-->"))
                        if pr == 1:
                            sq="SELECT trans_id,date,time,balance FROM transactions where account_number='"+an+"'"
                            
                            sql_query = pd.read_sql_query(sq,mydb)
                            df = pd.DataFrame(sql_query)
                            filenm=input("Enter file name:")
                            csvfile = filenm+".csv"
                            df.to_csv (csvfile, index = False)
                            staff()
                        if pr == 2:
                            staff()
                        else:
                            staff2()





####### End of Functions of Staff #########
###########################################
###########################################





################################################################################################
                            #Admin
################################################################################################
                    if usertype == 1:
                        def admin():
                            print("\nWelcome Admin")
                            print("1 > To create new staff account")
                            print("2 > Manage staff")
                            print("3 > Logout")
                            ach = int(input("Enter your command :"))
                            if ach == 1:
                                create_staff()

                            if ach == 2:
                                manage_staff()
                            
                            
                            if ach == 3:
                                print("\nEnding Section\n")
                                login()
                        admin()
               
################################################################################################  
                            #Customer             
################################################################################################
                    if usertype == 3:
                        def customer():
#getting customer name
                            mycursor.execute("select f_name from customer where login_id='"+li+"'")
                            f_namex=mycursor.fetchone()
                            f_name = f_namex[0]
                            mycursor.execute("select l_name from customer where login_id='"+li+"'")
                            l_namex=mycursor.fetchone()
                            l_name = l_namex[0]
                            name = f_name+" "+l_name


#end of getting name
                            


                            print("\nWelcome",name)
                            print("1 > To veiw account number")
                            print("2 > To veiw account balance")
                            print("3 > Withdraw")
                            print("4 > Deposit")
                            print("5 > Send")
                            print("6 > Show account statement")
                            print("7 > Manage your account")
                            print("8 > Logout")
                            
                            
                            ach = int(input("Enter your command :"))
                            if ach == 1:
                                cus_view_account_number()
                            
                            if ach == 2:
                                cus_check_balance()

                            if ach == 3:
                                withdraw()

                            if ach == 4:
                                deposit()

                            if ach == 5:
                                send_money()

                            if ach == 6:
                                show_statement()


                            if ach == 7:
                                cus_manage_account()

                            if ach == 8:
                                print("\nEnding Section\n")
                                login()
                        customer()

################################################################################################
                            #Staff
################################################################################################

                    if usertype == 2:
                        def staff():
#getting customer name
                            mycursor.execute("select f_name from staff where login_id='"+li+"'")
                            f_namex=mycursor.fetchone()
                            f_name = f_namex[0]
                            mycursor.execute("select l_name from staff where login_id='"+li+"'")
                            l_namex=mycursor.fetchone()
                            l_name = l_namex[0]
                            name = f_name+" "+l_name
#end of getting name                            
                            print("\nWelcome",name,"\n")
                            print("1 > Search Customer")
                            print("2 > Manage freezed account")
                            print("3 > Get statement")
                            print("4 > Logout")
                            ach = int(input("Enter your command :"))
                            if ach == 1:
                                search_cus()

                            if ach == 2:
                                manage_freezed()

                            if ach == 3:
                                get_statements()

                            if ach == 4:
                                print("\nEnding Section\n")
                                login()
                        staff()
               
################################################################################################                          
               
################################################################################################               
                if password!=pwi:
                    print("=========INVALID PASSWORD..!=========")
                    login()
            login()

        elif ch==3:
            quit()
            

#end of log_in       

main()