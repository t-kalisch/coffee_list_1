import streamlit as st
import math
import re
#import sqlite3
import mysql.connector as mysql
import csv
from tkinter import *
import matplotlib
import numpy
import matplotlib.pyplot as plt
import datetime
from datetime import date
import pandas as pd
from plotly import *
import plotly.express as px

def calc():
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    cursor.execute("create table if not exists total_coffees (id int auto_increment, name VARCHAR(20), coffees int, primary key(id))")      #total coffees per person

    cursor.execute("select id_ext, persons, coffees from drinkers order by id desc limit 1")        #takes last break in database table drinkers
    temp=cursor.fetchall()
    temp=list(temp[0])                                                                              #converesion to id_ext & persons/coffees lists
    id_ext=temp[0]
    persons=temp[1].split("-")
    coffees=list(map(int, temp[2].split("-")))

    for i in range(len(persons)):
        cursor.execute("select coffees from total_coffees where name='"+persons[i]+"'")
        coffee_pP=cursor.fetchone()
        if coffee_pP==None:
            coffee_pP=0
        else:
            coffee_pP=list(coffee_pP)
            coffee_pP=int(coffee_pP[0])
        if not coffee_pP:
            coffee_pP=0
        
        coffee_pP=coffee_pP+int(coffees[i])


        cursor.execute("select name from total_coffees where name='"+persons[i]+"'")
        if not list(cursor.fetchall()):
            cursor.execute("insert total_coffees (name, coffees) values ('"+persons[i]+"', "+str(coffee_pP)+")")
        else:
            cursor.execute("update total_coffees set name='"+persons[i]+"', coffees="+str(coffee_pP)+" where name='"+persons[i-1]+"'")
    cursor.execute("select name, coffees from total_coffees")
    
    db.commit()
    databases=cursor.fetchall()
    for row in databases:
        print(row)
    print("--------------------")
    db.close()

#-------------------------- Plot for total coffees pie chart ------------------------
def total_coffees():
    names = get_members()
    total_coffees = get_total_coffees(names)

    temp=[]
    columns_total=["names","total"]
    
    df = pd.DataFrame(total_coffees, columns=columns_total, index=names)              #total coffees pie chart
    fig3 = px.pie(df, names = 'names', values = 'total', hole=.4)

    #fig3.update_layout(showlegend=True, title_font_size=24)
    fig3.show()


def cumulated_coffees_p_m():
    plt.style.use('seaborn-whitegrid')
    line1=plt.figure()
    ax=plt.axes()

    names = get_members()                                   #getting all members

    month_info = get_months(datetime.date(2020,11,1))       #getting months from 11 2020 to now
    months = month_info[0]
    month_id = month_info[1]

    all_coffees=get_monthly_coffees(names, month_id)         #getting monthly coffees
    
    for i in range(len(names)):
        coffees=[]
        for j in range(len(month_id)):
            if j > 0:
                coffees.append(coffees[j-1]+all_coffees[i][j])  #adding up monthly coffees
            else:
                coffees.append(all_coffees[i][j])
        plt.plot(months, coffees)                           #plotting cumulated monthly coffees

    line1.set_figwidth(12)
    line1.legend(names, title="drinkers", loc="center left", bbox_to_anchor=(0.92, 0, 0.5, 1))
    line1.suptitle("Cumulated coffees per month")
    plt.ylabel('number of coffees')
    plt.show()


#------------------------- plot for coffees per month ----------------------------------
def coffees_p_month():
    plt.style.use('seaborn-whitegrid')
    line1=plt.figure()
    ax=plt.axes()

    names = get_members()                                   #getting all members

    month_info = get_months(datetime.date(2020,11,1))       #getting months from 11 2020 to now
    months = month_info[0]
    month_id = month_info[1]

    all_coffees = get_monthly_coffees(names, month_id)       #getting monthly coffeees
    
    for i in range(len(names)):
        plt.plot(months, all_coffees[i])                    #plotting monthly coffees
    
    line1.set_figwidth(12)
    line1.legend(names, title="drinkers", loc="center left", bbox_to_anchor=(0.92, 0, 0.5, 1))
    line1.suptitle("Coffees per month")
    plt.ylabel('number of coffees')
    plt.show()

#--------------------------- plot for total coffees per month --------------------------
def total_coffees_p_month():
    plt.style.use('seaborn-whitegrid')
    bar1=plt.figure(figsize=(12,4.8))
    #ax=bar1.add_axes([0,0,1,1])

    names = get_members()                                   #getting all members

    month_info = get_months(datetime.date(2020,11,1))       #getting months from 11 2020 to now
    months = month_info[0]
    month_id = month_info[1]

    coffees = get_total_monthly_coffees(names, month_id)       #getting total monthly coffeees
    
    plt.bar(months, coffees)                             #plotting total monthly coffees
    
    for i,v in enumerate(coffees):
        plt.text(i -.24, v - 10, str(v), color='white', fontweight='bold')
    plt.ylabel("number of coffees")
    plt.title("Total coffees per month")
    plt.show()

#------------------------- plot for monthly ratio of coffees ---------------------------------
def ratio_monthly():
    fig, ax = plt.subplots()
    plt.style.use('seaborn-whitegrid')
    #plt.figure(figsize=(12,4.8))

    names = get_members()                                   #getting all members

    month_info = get_months(datetime.date(2020,11,1))       #getting months from 11 2020 to now
    months = month_info[0]
    month_id = month_info[1]

    ratios = get_monthly_ratio(names, month_id)       #getting monthly ratios




    for i in range(len(names)):
            ax.bar(months, ratios[i], 0.35, label=names[i])
    
    ax.set_ylabel('Ratio')
    ax.set_title('Monthly ratios')
    ax.legend()

    plt.show()
    
    #plt.bar(months, ratios)                             #plotting monthly ratios
    
    #for i,v in enumerate(ratios):
    #    plt.text(i -.24, v - 10, str(v), color='white', fontweight='bold')
    #plt.ylabel("number of coffees")
    #plt.title("Total coffees per month")
    #plt.show()


#-------------------------------------------------------------- plot for absolute and relative correlation ---------------------------------------
def correlation():
    names=get_members()
    
    corr_tot = get_correlation(names)
    corr_abs_raw=corr_tot[0]
    corr_rel_raw=corr_tot[1]

    temp1=[]
    temp2_abs=[]
    temp2_rel=[]
    tickval_num=[]
    for i in range(len(names)):
        tickval_num.append(i+1)
        for j in range(len(names)):
            temp_abs=[]
            temp_rel=[]
            temp_abs.append(i+1)
            temp_rel.append(i+1)
            temp_abs.append(j+1)
            temp_rel.append(j+1)
            temp_abs.append(corr_abs_raw[i][j])      #calculates absolute correlation
            temp_rel.append(corr_rel_raw[i][j])      #calculates relative correlation
            temp2_abs.append(temp_abs)
            temp2_rel.append(temp_rel)
    
    columns_corr=['x-values','y-values','size']
    
    df = pd.DataFrame(temp2_abs, columns=columns_corr)
    fig_corr_abs = px.scatter(df, x='x-values', y='y-values', size='size', labels={"x-values":"", "y-values":""}, title="Absolute correlation", color='size')#, text='size')
    #fig5.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names))

    df = pd.DataFrame(temp2_rel, columns=columns_corr)
    fig_corr_rel = px.scatter(df, x='x-values', y='y-values', size='size', labels={"x-values":"", "y-values":""}, title="Relative correlation", color='size')#, text='size')
    #fig5.update_layout(title_font_size=24, showlegend=False, xaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names), yaxis=dict(tickmode = 'array', tickvals = tickval_num, ticktext = names))
    fig_corr_abs.show()
    fig_corr_rel.show()


#---------------------------------- percentage of total breaks per month and in total -------------------------------------------
def perc_breaks():
    names=get_members()

    month_info = get_months(datetime.date(2021,3,8))       #getting months from 03 2021 to now
    months = month_info[0]
    month_id = month_info[1]

    
    percentage = get_perc_breaks(names, month_id)

    df = pd.DataFrame(percentage, columns=names, index=months)              #percentage per month

    fig2 = px.line(df, title="Percentage of breaks per month", labels={"variable":"drinkers", "index":"", "value":"Percentage"})
    fig2.update_layout(title_font_size=24)
    fig2.show()

def weekly_coffees_breaks():
    names=get_members()

    month_id=[]
    columns=['Weekly breaks','Weekly coffees']
    weekly_data = get_weekly_coffees_breaks(names)

    weeks=[]
    weekly_br_c=[]
    
    for i in range(len(weekly_data)):
        temp=[]
        weeks.append(weekly_data[i][0])
        temp.append(weekly_data[i][1])
        temp.append(weekly_data[i][2])
        weekly_br_c.append(temp)

    df = pd.DataFrame(weekly_br_c, columns=columns, index=weeks)              #weekly coffees/breaks

    fig2 = px.line(df, title="Weekly coffee breaks and coffees", labels={"variable":"", "index":"", "value":"e"})
    fig2.update_layout(title_font_size=24, hovermode="x unified")
    fig2.show()

#------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------        calculating functions         --------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------- getting all members from database ---------------------------------------
def get_members():
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    names=[]

    cursor.execute("select name from members")              #getting all members tables
    mbrs=cursor.fetchall()
    mbrs=list(mbrs)
    for i in range(len(mbrs)):
        names.append(mbrs[i][0])
    db.close()
    return names

#----------------------------------------- extracting monthly coffees from database --------------------------------------
def get_monthly_coffees(names, month_id):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)
    all_coffees=[]

    cursor.execute("select id_ext from update_status where object = 'database' or object = 'monthly'")            #getting update status of graph
    current_id=cursor.fetchall()
    if current_id[0][0] == current_id[1][0]:
        cursor.execute("select content from update_status where object = 'monthly'")              #getting data from update_status if up to date
        tmp = cursor.fetchall()
        temp = tmp[0][0]

        temp1 = temp[2:-2].split("], [")
        for i in range(len(temp1)):
            temp2 = temp1[i].split(", ")
            for j in range(len(temp2)):
                temp2[j] = int(temp2[j])        #converting str to int
            all_coffees.append(temp2)
            
        print("old values taken")
    else:
        for i in range(len(names)):                                              #writing total cofees per month into coffees
            coffees=[]
            for j in range(len(month_id)):
                total=0

                cursor.execute("select n_coffees from mbr_"+names[i].lower()+" where id_ext like '"+str(month_id[j])+"%'")
                tmp=cursor.fetchall()
                tmp=list(tmp)
            
                for k in range(len(tmp)):
                    total=total+tmp[k][0]
                coffees.append(total)
                if i < 6:                                                       #input from old breaks
                    if j < 5:
                        cursor.execute("select "+names[i].upper()+" from old_breaks where id_ext like'"+str(month_id[j])+"%'")
                        old_coffees=cursor.fetchall()
                        old_coffees=list(old_coffees)
                        coffees[j]=coffees[j]+old_coffees[0][0]
            all_coffees.append(coffees)
        
        print("new values taken")
        cursor.execute("update update_status set id_ext = "+str(current_id[0][0])+", content = '"+str(all_coffees)+"' where object = 'monthly'")
        db.commit()
    db.close()
    return all_coffees


#----------------------------------- extracting total monthly coffees from database -----------------------------
def get_total_monthly_coffees(names, month_id):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)
    total_coffees_monthly=[]
    
    cursor.execute("select id_ext from update_status where object = 'database' or object = 'tot_m'")            #getting update status of graph
    current_id=cursor.fetchall()
    
    if current_id[0][0] == current_id[1][0]:
        cursor.execute("select content from update_status where object = 'tot_m'")              #getting data from update_status if up to date
        tmp = cursor.fetchall()
        temp = tmp[0][0]
        
        total_coffees_monthly = temp[1:-1].split(", ")
        for i in range(len(total_coffees_monthly)):     #converting str to int
            total_coffees_monthly[i] = int(total_coffees_monthly[i])
        print("old values taken")
    else:
        
        for i in range(len(month_id)):
            coffees=[]
            total=0
            for j in range(len(names)):
            

                cursor.execute("select n_coffees from mbr_"+names[j].lower()+" where id_ext like '"+str(month_id[i])+"%'")      #getting new data if update_status not up to date
                tmp=cursor.fetchall()
                tmp=list(tmp)
            
                for k in range(len(tmp)):
                    total=total+tmp[k][0]

            if i < 5:                                                           #input from old breaks
                cursor.execute("select TK,PB,NV,DB,FLG,SHK from old_breaks where id_ext like'"+str(month_id[i])+"%'")
                old_coffees=cursor.fetchall()
            
                for j in range(6):
                    total=total+old_coffees[0][j]
            total_coffees_monthly.append(total)
        cursor.execute("update update_status set id_ext = "+str(current_id[0][0])+", content = '"+str(total_coffees_monthly)+"' where object = 'tot_m'")
        db.commit()
        print("new values taken")

    db.close()
    return total_coffees_monthly

#-------------------------- getting total coffees from database
def get_total_coffees(names):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    cursor.execute("select id_ext from update_status where object = 'database' or object = 'tot_c'")
    tmp=cursor.fetchall()

    
    coffees=[]
    if tmp[0][0] == tmp[1][0]:
        cursor.execute("select content from update_status where object = 'tot_c'")      #getting old data from update_status if up to date
        tmp = cursor.fetchall()

        temp = tmp[0][0]
        tot_coffees = temp[1:-1].split(", ")
        for i in range(len(tot_coffees)):           #converting str to int
            tot_coffees[i] = int(tot_coffees[i])
        
        for i in range(len(names)):
            temp=[]
            temp.append(names[i])
            temp.append(tot_coffees[i])
            coffees.append(temp)
        print("old values taken")
        
    else:
        percentage=[]
        content_input=[]
        total=0
        for i in range(len(names)):
            temp1=[]
            temp1.append(names[i])
            cursor.execute("select n_coffees from mbr_"+names[i])       #getting new data if update status not up to date
            temp=cursor.fetchall()
            total=0
            for j in range(len(temp)):
                total=total+temp[j][0]
            temp1.append(total)
            content_input.append(total)
            coffees.append(temp1)
        
        for i in range(5):                                      #inserting old coffees from before March 8, 2021
            for j in range(6):
                cursor.execute("select "+names[j]+" from old_breaks where id = "+str(i+1))
                temp=cursor.fetchall()
                coffees[j][1]=coffees[j][1]+temp[0][0]
        print("new values calculated")
        cursor.execute("drop table if exists total_coffees")            #delete total_coffees table
        cursor.execute("create table if not exists total_coffees (id int auto_increment, name VARCHAR(20), coffees int, primary key(id))")      #total coffees per person
        for i in range(len(names)):
            cursor.execute("insert into total_coffees (name, coffees) values (%s,%s)",(str(coffees[i][0]), coffees[i][1]))

        #writing update_status table
        cursor.execute("select max(id_ext) from breaks")
        tmp = cursor.fetchall()
        cursor.execute("update update_status set id_ext = "+str(tmp[0][0])+" where object = 'tot_c'")
        cursor.execute("update update_status set content = '"+str(content_input)+"' where object = 'tot_c'")
        
        db.commit()
    db.close()
    return coffees


#--------------------------- calculating monthly ratios from database -----------------------------
def get_monthly_ratio(names, month_id):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)
    
    monthly_ratio=[]
    total_coffees = get_total_monthly_coffees(names, month_id)
    monthly_coffees = get_monthly_coffees(names, month_id)
    
    for i in range(len(names)):
        temp=[]
        for j in range(len(month_id)):
            ratio=100*monthly_coffees[i][j]/total_coffees[j]
            temp.append(ratio)
        monthly_ratio.append(temp)
    print(monthly_ratio)
    return monthly_ratio

#--------------------------- getting correlations between drinkers ------------------------------------
def get_correlation(names):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    corr_all=[]
    tot_coffees=[]
    temp = get_total_coffees(names)
    for i in range(len(names)):
        tot_coffees.append(temp[i][1])
    corr_abs=[]
    corr_rel=[]
    for i in range(len(names)):
        temp_abs=[]
        temp_rel=[]
        cursor.execute("select id_ext from mbr_"+names[i])
        all_breaks=cursor.fetchall()
        for j in range(len(names)):
            
            temp=[]
            if i==j:
                
                cursor.execute("SELECT coffees from drinkers where persons = '"+names[j]+"'")               #for self-correlation in the sense of lonely breaks
                tmp=cursor.fetchall()
                
                for k in range(len(tmp)):
                    temp.append(int(tmp[k][0]))
                
            else:
                for k in range(len(all_breaks)):
                    cursor.execute("SELECT n_coffees from mbr_"+str(names[j])+" where id_ext = "+all_breaks[k][0])  #for correlation with other people
                    tmp=cursor.fetchall()
                    if len(tmp)>0:
                        temp.append(tmp[0][0])
            temp1=0
            for l in range(len(temp)):
                temp1=temp1+temp[l]
            temp_abs.append(temp1)
            temp_rel.append(round(100*temp1/tot_coffees[i],1))                                               #calculating relative correlation
        corr_abs.append(temp_abs)
        corr_rel.append(temp_rel)
    corr_all.append(corr_abs)
    corr_all.append(corr_rel)
    #for i in range(len(corr_abs)):
    #    print(str(corr_abs[i][0])+"\t"+str(corr_abs[i][1])+"\t"+str(corr_abs[i][2])+"\t"+str(corr_abs[i][3])+"\t"+str(corr_abs[i][4])+"\t"+str(corr_abs[i][5])+"\t"+str(corr_abs[i][6])+"\t"+str(corr_abs[i][7])+"\t"+str(corr_abs[i][8]))
    return corr_all

#----------------------------- getting the percentage of total breaks per month and in total per person ------------------------
def get_perc_breaks(names, month_id):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    tot_breaks = get_tot_br_p_m(month_id)

    percentage = []
    for i in range(len(month_id)):  #writing total cofees per month into coffees
        temp=[]
        for j in range(len(names)):
            cursor.execute("select count(id_ext) from mbr_"+names[j].lower()+" where id_ext like '"+str(month_id[i])+"%'")
            tmp=cursor.fetchall()
            temp.append(100*tmp[0][0]/tot_breaks[i])
        percentage.append(temp)
    #print(percentage)
    db.close()
    return percentage

def get_tot_br_p_m(month_id):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    total_breaks=[]
    for i in range(len(month_id)):
        cursor.execute("select count(id_ext) from breaks where id_ext like '"+str(month_id[i])+"%'")
        tmp = cursor.fetchall()

        for j in range(len(tmp)):
            total_breaks.append(tmp[j][0])
    #print(total_breaks)
    return total_breaks


#----------------------------- getting all weekly breaks and weekly coffees ------------------------------
def get_weekly_coffees_breaks(names):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)

    cursor.execute("SELECT max(id_ext) FROM breaks")  #getting month names from beginning to current
    temp=cursor.fetchone()
    temp=list(temp)
    last_date=datetime.date(int(temp[0][0:4]),int(temp[0][4:6]),int(temp[0][6:8]))
    start_date=datetime.date(2021, 3, 8)

    if start_date > last_date:
        raise ValueError(f"Start date {start_date} is not before end date {end_date}")
    else:
        curr_date=start_date
        year = curr_date.year
        month = curr_date.month
        day = curr_date.day
        delta_days = (last_date-start_date).days
        weeknum_ids=[]
        breaks_daily=[]
        breaks_weekly=[]
        coffees_daily=[]
        coffees_weekly=[]
        text_weekly=[]
        weekly_data=[]

        for i in range(delta_days+1):
            id_day = str(curr_date.year)
            if curr_date.month < 10:
                id_day = id_day + "0" + str(curr_date.month)
            else:
                id_day = id_day + str(curr_date.month)
            if curr_date.day < 10:
                id_day = id_day + "0" + str(curr_date.day)
            else:
                id_day = id_day + str(curr_date.day)

            weeknum = datetime.date(curr_date.year, curr_date.month, curr_date.day).isocalendar()[1]
            
            cursor.execute("select count(id_ext) from breaks where id_ext like '"+id_day+"%'")
            tmp=cursor.fetchall()
            temp=[]
            if weeknum < 10:
                temp.append(int(str(curr_date.year)+"0"+str(weeknum)))
            else:
                if weeknum > 10 and curr_date.month == 1:                                   #avoiding new year in last week
                    temp.append(int(str(int(curr_date.year)-1)+str(weeknum)))
                else:
                    temp.append(int(str(curr_date.year)+str(weeknum)))
            temp.append(tmp[0][0])
            curr_date=curr_date+datetime.timedelta(days=1)
            breaks_daily.append(temp)
            
            total=0
            for j in range(len(names)):
                cursor.execute("select n_coffees from mbr_"+names[j]+" where id_ext like '"+id_day+"%'")
                tmp=cursor.fetchall()

                for k in range(len(tmp)):
                    total=total+tmp[k][0]
                    
            temp=[]
            if weeknum < 10:
                if int(str(curr_date.year)+"0"+str(weeknum)) not in weeknum_ids:
                    weeknum_ids.append(int(str(curr_date.year)+"0"+str(weeknum)))
                    text_weekly.append("0"+str(weeknum)+"/"+str(curr_date.year))
                temp.append(int(str(curr_date.year)+"0"+str(weeknum)))
            else:
                if weeknum > 10 and curr_date.month == 1:                                   #avoiding new year in last week
                    if int(str(int(curr_date.year)-1)+str(weeknum)) not in weeknum_ids:
                        weeknum_ids.append(int(str(int(curr_date.year)-1)+str(weeknum)))
                        text_weekly.append(str(weeknum)+"/"+str(int(curr_date.year)-1))
                    temp.append(int(str(int(curr_date.year)-1)+str(weeknum)))
                else:
                    if int(str(curr_date.year)+str(weeknum)) not in weeknum_ids:
                        weeknum_ids.append(int(str(curr_date.year)+str(weeknum)))
                        text_weekly.append(str(weeknum)+"/"+str(curr_date.year))
                    temp.append(int(str(curr_date.year)+str(weeknum)))
            temp.append(total)
            coffees_daily.append(temp)
    
    for i in range(len(weeknum_ids)):
        temp=[]
        total_breaks=0
        total_coffees=0
        for j in range(len(breaks_daily)):
            if breaks_daily[j][0] == weeknum_ids[i]:
                total_breaks=total_breaks+breaks_daily[j][1]
            if coffees_daily[j][0] == weeknum_ids[i]:
                total_coffees=total_coffees + coffees_daily[j][1]
        temp.append(text_weekly[i])
        temp.append(total_breaks)
        temp.append(total_coffees)
        weekly_data.append(temp)
        
    return weekly_data
            
#----------------------------- getting all months from start date to now ---------------------------------
def get_months(first_date):
    db = mysql.connect(user='PBTK', password='akstr!admin2', #connecting to mysql
    host='127.0.0.1',
    database='coffee_list')
    cursor=db.cursor(buffered=True)
    
    month_info=[]
    months=[]
    month_id=[]

    cursor.execute("SELECT max(id_ext) FROM breaks")  #getting month names from beginning to current
    temp=cursor.fetchone()
    temp=list(temp)

    last_date=datetime.date(int(temp[0][0:4]),int(temp[0][4:6]),int(temp[0][6:8]))
    for month in months_between(first_date,last_date):
        if(month.month<10):
            month_id.append(str(month.year)+"0"+str(month.month))
        else:
            month_id.append(str(month.year)+str(month.month))
        months.append(month.strftime("%B")[0:3]+" '"+month.strftime("%Y")[2:4])
    month_info.append(months)
    month_info.append(month_id)
    
    db.close()
    return month_info
    
    
def months_between(start_date, end_date):           #method to get months between two dates
    if start_date > end_date:
        raise ValueError(f"Start date {start_date} is not before end date {end_date}")
    else:
        year = start_date.year
        month = start_date.month

        while (year, month) <= (end_date.year, end_date.month):
            yield datetime.date(year, month, 1)
            # Move to the next month.  If we're at the end of the year, wrap around
            # to the start of the next.
            #
            # Example: Nov 2017
            #       -> Dec 2017 (month += 1)
            #       -> Jan 2018 (end of year, month = 1, year += 1)
            #
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1


    


