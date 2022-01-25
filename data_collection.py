import streamlit as st
import math
import re
#import sqlite3
import mysql.connector as mysql
#import pandas as pd
import csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#from calculations import *
#import matplotlib
#matplotlib.use('Agg')
status=""

#------------------------------------------------ reading input file -----------------------------------------------------------

#read date, write into date_break


#cnx = mysql.connector.connect(user='PBTK', password='akstr!admin2',
#                              host='131.220.66.200',
#                              database='coffee_list')
#cnx.close()

#--------------------------- main function to call from different script
def write_break(coffee_break,breaklen):
    id_ext=""
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
                              host='127.0.0.1',
                              database='coffee_list')
    cursor=db.cursor(buffered=True)
    
    cursor.execute("use coffee_list")

    cursor.execute("create table if not exists breaks (id int auto_increment, id_ext char(10), day int, month int, year int,  primary key(id), unique key(id_ext))")                 #creatingbreaks table
    cursor.execute("create table if not exists drinkers (id int auto_increment, id_ext char(10), persons varchar(30), coffees varchar(30), primary key(id), CONSTRAINT fk_drinkers_break_ID_ext FOREIGN KEY(id_ext) REFERENCES breaks(id_ext) ON DELETE CASCADE)")   #creating drinkers table
    cursor.execute("create table if not exists members (id int auto_increment, name varchar(3), password varchar(20), primary key(id))")
    cursor.execute("create table if not exists update_status (id int auto_increment, object varchar(5), id_ext int, content varchar(1000), primary key(id))")
    
       #---------------------- creating the extended id -----------------------
    id_ext=""
    date_break=coffee_break[0]
    day_break=str(date_break[0])
    month_break=str(date_break[1])
    if(len(month_break)==1):          #adding "0" if month has 1 digit
        month_break="0"+str(date_break[1])
    if(len(day_break)==1):            #adding "0" if day has 1 digit
        day_break="0"+str(date_break[0])
    id_ext=str(date_break[2])+month_break+day_break
    
    total=0
    cursor.execute("SELECT id_ext FROM breaks WHERE id_ext like '"+id_ext+"%'")    #searching for breaks of the same day as enterd break
    ids=cursor.fetchall()
    ids=list(ids)
    for i in range(len(ids)):
        ids[i]=int(ids[i][0])
    if len(ids)==0:
        id_ext=id_ext+"01"
    else:
        id_ext=str(max(ids)+1)

    temp1=""                                    #converting coffee_break into a list of strings for instertion into database
    temp2=""
    coffee_break_str=[]
    coffee_break_str.append(date_break)

    for i in range(len(coffee_break[1])):
        temp1=temp1+str(coffee_break[1][i])
        temp2=temp2+str(coffee_break[2][i])
        if i<(len(coffee_break[1])-1):
            temp1=temp1+"-"
            temp2=temp2+"-"
    coffee_break_str.append(temp1)
    coffee_break_str.append(temp2)
    
    cursor.execute("INSERT INTO breaks (id_ext, day, month, year) VALUES ("+id_ext+","+str(date_break[0])+","+str(date_break[1])+","+str(date_break[2])+")")
    cursor.execute("INSERT INTO drinkers (id_ext, persons, coffees) VALUES ("+id_ext+",'"+str(coffee_break_str[1])+"','"+str(coffee_break_str[2])+"')")
    #cursor.execute("select * from drinkers")
    #temp=cursor.fetchall()
    #for row in temp:
    #    print(row)
    print("Coffee break saved!")
    print(id_ext+", "+str(coffee_break_str[1])+", "+str(coffee_break_str[2]))

    #--------------------- writing into each person's list -------------------
    persons=coffee_break[1]
    coffees=coffee_break[2]

    for i in range(len(persons)):
        cursor.execute("create table if not exists mbr_"+persons[i]+" (id_ext char(10), n_coffees int, primary key(id_ext), CONSTRAINT fk_member_"+persons[i]+"_break_ID_ext FOREIGN KEY(id_ext) REFERENCES breaks(id_ext) ON DELETE CASCADE)")     #creating a table for each individual person
        cursor.execute("insert into mbr_"+persons[i]+" (id_ext, n_coffees) values (%s, %s)", (id_ext, coffees[i]))              #writes break id and coffees into personal table
        cursor.execute("select count(*) from members where name='"+persons[i]+"'")                                                #checks if person is already written in members table
        temp=cursor.fetchone()
        temp=int(temp[0])
        if temp==0:
            cursor.execute("insert into members (name) values ('"+str(persons[i])+"')")                                           #writes person into members table
                           

    #---------------------- writing break length table ------------------------
    cursor.execute("create table if not exists break_lengths (id int auto_increment, id_ext char(10), length time(6), primary key(id), CONSTRAINT fk_breaklen_break_ID_ext FOREIGN KEY(id_ext) REFERENCES breaks(id_ext) ON DELETE CASCADE)")
    cursor.execute("insert into break_lengths (id_ext, length) values (%s, %s)",(id_ext,breaklen))

    #writing update_status table
    cursor.execute("select max(id_ext) from breaks")
    tmp = cursor.fetchall()
    cursor.execute("update update_status set id_ext = "+str(tmp[0][0])+" where object = 'database'")
    
    
    db.commit()
    #cursor.execute("select * from drinkers")
    #databases=cursor.fetchall()
    #for row in databases:
    #    print(row)
    #print("--------------------")
    db.close()


    #---------------------- checking for user and password --------------------

def safety_check(command):
    status=command
    sfycheck_fld = Tk()
    sfycheck_fld.geometry("400x100")
    sfycheck_fld.title("Safety Check")
    frame_sfycheck = LabelFrame(sfycheck_fld, width= 400, height=200, bd = 0)
    frame_sfycheck.place (x=0, y= 10)
    header_sfycheck=Label(frame_sfycheck, text="Please enter your user name and password:", fg="red", font=("Helvetica", 14))
    header_sfycheck.place(x=20, y = 0)
    user_inp=ttk.Entry(frame_sfycheck, text="", width=4)
    user_inp.place(x=120, y = 30)
    pw_inp=ttk.Entry(frame_sfycheck, show="*", text="", width=8)
    pw_inp.place(x=161, y = 30)
    conf_sfycheck=ttk.Button(frame_sfycheck, text="Delete this break", command=lambda: user_pw_database_search(sfycheck_fld,user_inp,pw_inp,status) )
    conf_sfycheck.place(x=119, y= 60)
    sfycheck_fld.bind('<Return>', (lambda event: user_pw_database_search(sfycheck_fld,user_inp,pw_inp,status)))

def user_pw_database_search(sfycheck_fld,user_inp,pw_inp,status):
    user_inp=str(user_inp.get()).upper()
    pw_inp=str(pw_inp.get())
    
    #print(user_inp, pw_inp)

    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
                              host='127.0.0.1',
                              database='coffee_list')
    cursor=db.cursor(buffered=True)
    
    cursor.execute("use coffee_list")
    cursor.execute("SELECT * FROM members WHERE name='"+user_inp+"'")
    user_data=""
    user_data=cursor.fetchall()
    #print(user_data)
    if user_data==[]:
        sfycheck_fld.destroy()
        messagebox.showinfo("Log-In status", "No such User!")
        
    else:
        user_data_check=list(user_data[0])
    
        #print(user_data)
        #print(pw_inp)     
        
        if user_data_check[2]==pw_inp:
            sfycheck_fld.destroy()

            if status=="delete_one":                            # to delete one break
                clear_ONE_break()
            elif status=="delete_db":                           # to clear the whole database
                if user_data_check[3]==1:
                    answer = messagebox.askokcancel("Confirmation", "Are you REALLY sure to clear the database?",icon="warning")
                    if answer:
                        answer = messagebox.askokcancel("Confirmation", "Final warning!",icon="warning")
                        if answer:
                            #clear_database()
                            messagebox.showinfo("Deletion status", "The database has successfully been cleared.")
                else:
                    messagebox.showerror("Access denied", "You do not have admin rights. Please contact your system administrator.")
        else:
            sfycheck_fld.destroy()
            messagebox.showinfo("Log-In status", "Wrong Password!")

        return
            
    #---------------------- deleting a break by knowing id_ext ----------------
def clear_ONE_break():
    input_fld = Tk()
    input_fld.geometry("600x100")
    input_fld.title("Deleting a break from the databank")
    frame_ifld = LabelFrame(input_fld, width= 600, height=100, bd = 0)
    frame_ifld.place (x=0, y= 30)
    header_ifld=Label(input_fld, text="Please enter the coffee break ID you want to delete:", fg="red", font=("Helvetica", 14))
    header_ifld.place(x=70, y = 10)
    id_inp=ttk.Entry(frame_ifld, text="", width=20)
    id_inp.place(x=220, y = 30)
    conf_delete_break=ttk.Button(frame_ifld, text="Delete this break", command=lambda: conf_break_delete(input_fld,id_inp) )
    conf_delete_break.place(x=350, y=28)
    input_fld.bind('<Return>', (lambda event: conf_break_delete(input_fld,id_inp)))
        
def conf_break_delete(input_fld,id_inp):
    #print(str(id_inp.get()).upper())
    del_ID=[]
    del_ID.append(str(id_inp.get()).upper())
    del_ID=str(del_ID[0])
    print("Coffee break deleted: "+del_ID)

    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
                              host='127.0.0.1',
                              database='coffee_list')
    cursor=db.cursor(buffered=True)
    
    cursor.execute("use coffee_list")
    cursor.execute("SELECT * FROM breaks WHERE id_ext='"+del_ID+"'")
    del_break=""
    del_break=cursor.fetchall()
    #print(del_break)
    
    if del_break != []:
        cursor.execute("DELETE FROM breaks WHERE id_ext='"+del_ID+"'")

        #writing update_status table
        cursor.execute("select max(id_ext) from breaks")
        tmp = cursor.fetchall()
        cursor.execute("update update_status set id_ext = "+str(tmp[0][0])+" where object = 'database'")

        input_fld.destroy()
        messagebox.showinfo("Deletion status", "This break has successfully been deleted.")
             
    else:
        input_fld.destroy()
        messagebox.showinfo("Deletion status", "This break does not exist, therefore nothing was deleted.")

        
        
    
    db.commit()
    db.close    

    #------------------- deleting the whole database --------------------------------------
def clear_database():
    db = mysql.connect(user='PBTK', password='akstr!admin2',
                              host='127.0.0.1',
                              database='coffee_list')
    cursor=db.cursor()

    cursor.execute("use coffee_list")
    cursor.execute("SHOW tables")
    databases=cursor.fetchall()
    #print(databases)
    #print("yes")
    cursor.execute("select name from members")
    mbrs=cursor.fetchall()
    mbrs=list(mbrs)
    for i in range(len(mbrs)):
        cursor.execute("drop table if exists mbr_"+mbrs[i][0])
    
    cursor.execute("drop table if exists break_ID,breaks, drinkers, members, total_coffees, break_lengths")
    cursor.execute("SHOW tables")
    databases=cursor.fetchall()
    #print(databases)
    db.commit()
    db.close()

   
    #------------------------- reading breaks from 2021 into database ---------------------
def breaks_2021():
    db = mysql.connect(user='PBTK', password='akstr!admin2',
                              host='127.0.0.1',
                              database='coffee_list')
    cursor=db.cursor()

    cursor.execute("use coffee_list")

    inp = []
    file = open("breaks_2021.txt","r")
    lines = file.readlines()
    file.close()
    persons=['TK','PB','NV','DB','FLG','SHK','TB']
    for line in lines:
        #print(line)
        #inp.append(list(map(int,line.split())))
        inp=list(map(int,line.split()))                     #getting lines from input file
        
        cursor.execute("SELECT * FROM breaks WHERE id_ext='"+str(inp[0])+"'")   #check if break is already in database
        exists=""
        exists=cursor.fetchall()
        if exists==[]:
            #print(str(inp[0])+","+str(inp[0])[0:4]+","+str(inp[0])[4:6]+","+str(inp[0])[6:8])
            
            temp1=""
            temp2=""
            temp3=0
            temp4=0
            for j in range(7):                              #checking how many persons took part in break
                if inp[j+1]!=0:
                    temp3+=1

            cursor.execute("insert into breaks (id_ext, year, month, day) VALUES ("+str(inp[0])+","+str(inp[0])[0:4]+","+str(inp[0])[4:6]+","+str(inp[0])[6:8]+")")
            
            for j in range(7):                              #creating string for input into drinkers table
                if inp[j+1]!=0:
                    temp1+=persons[j]
                    temp2+=str(inp[j+1])
                    temp4+=1
                    if temp4 < temp3:
                        temp1+="-"
                        temp2+="-"
                    print(inp)
                    cursor.execute("create table if not exists mbr_"+persons[j]+" (id_ext char(10), n_coffees int, primary key(id_ext), CONSTRAINT fk_member_"+persons[j]+"_break_ID_ext FOREIGN KEY(id_ext) REFERENCES breaks(id_ext) ON DELETE CASCADE)")
                    cursor.execute("insert into mbr_"+persons[j]+" (id_ext, n_coffees) values (%s, %s)", (inp[0], inp[j+1]))
            
            cursor.execute("INSERT INTO drinkers (id_ext, persons, coffees) VALUES ("+str(inp[0])+",'"+temp1+"','"+temp2+"')")

    db.commit()
    db.close()
