from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as npy
import matplotlib.pyplot as plt
import datetime
from datetime import date
import plotly
import plotly.graph_objects as go
import plotly.express as px
#from data_collection import *


st.set_page_config(page_title="Coffee list",page_icon="chart_with_upwards_trend",layout="wide")

"""
# Welcome to our coffee list!

In order to submit a coffee break, you need to be logged in with your username and password. Pauses are then automatically generated for you.
"""
   
def log_in(user, user_pw):
    if user != "":
         st.write("Attempted login: ",user)
    #st.write(user_pw)
    #start.disabled = False
    
st.sidebar.header("Sign in:")
user = st.sidebar.text_input(label="", placeholder="Username")
user_pw = st.sidebar.text_input(label="", type="password", placeholder="Password")
login = st.sidebar.button("Log In", help="Log in with your username and password", on_click=log_in(user, user_pw))
st.sidebar.title("Available diagrams:")

monthly_coffees_total=[75,25,59,88,163,196,197,150,127,206,184,144,163,103,32]
monthly_coffees1=[]
monthly_coffees=[[19, 9, 16, 19, 29, 31, 32, 30, 14, 41, 39, 34, 37, 24, 10], [15, 6, 6, 20, 29, 20, 24, 25, 29, 22, 32, 30, 35, 18, 12], [13, 6, 12, 16, 25, 35, 28, 37, 31, 27, 36, 30, 22, 14, 0], [10, 3, 7, 12, 27, 36, 37, 15, 22, 44, 10, 6, 4, 7, 1], [18, 1, 18, 21, 34, 35, 35, 26, 21, 43, 43, 27, 36, 22, 9], [0, 0, 0, 0, 19, 27, 23, 9, 5, 16, 22, 17, 26, 17, 0], [0, 0, 0, 0, 0, 12, 18, 8, 5, 13, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0]]
monthly_ratios=[[25.33,36.0,27.12,21.59,17.9,14.8,16.24,20.0,10.94,19.9,21.31,23.33,23.13,23.0,100],[20.0,24.0,10.17,22.73,17.28,10.2,12.18,16.67,22.66,10.68,17.49,22.67,21.88,18.0,0],[17.33,24.0,20.34,18.18,15.43,17.86,14.21,24.67,24.22,13.11,19.67,18.67,13.13,13.0,0],[13.33,12.0,11.86,13.64,16.67,18.88,18.78,10.0,17.19,21.36,5.46,4.0,3.13,7.0,0],[24.0,4.0,30.51,23.86,20.99,17.86,17.77,17.33,16.41,20.87,22.95,20.0,22.5,22.0,0],[0.0,0.0,0.0,0.0,11.73,14.29,11.68,6.0,4.69,7.77,12.02,11.33,16.25,17.0,0],[0.0,0.0,0.0,0.0,0.0,6.12,9.14,5.33,3.91,6.31,1.09,0.0,0.0,0.0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0]]
total_coffees=[372, 314, 328, 242, 382, 183, 58, 1, 3]
corr_abs=[[0,229,90,123,248,124,37,0,0],[229,1,75,89,205,83,31,0,0],[90,75,160,64,94,64,22,0,0],[123,89,64,21,133,83,40,0,0],[248,205,94,133,20,130,35,0,0],[124,83,64,83,130,25,18,0,0],[37,31,22,40,35,18,11,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
names=['TK','PB','NV','DB','FLG','SHK','TB','TT','RS']
months=["Nov '20","Dec '20", "Jan '21", "Feb '21", "Mar '21", "Apr '21", "May '21", "Jun '21", "Jul '21", "Aug '21", "Sep '21", "Oct '21", "Nov '21", "Dec '21", "Jan '22"]
cumulated_coffees1=[]
cumulated_coffees=[[19,28,44,63,92,121,153,183,197,238,277,312,349,372,372],[15,21,27,47,75,95,119,144,173,195,227,261,296,314,314],[13,19,31,47,72,107,135,172,203,230,266,294,315,328,328],[10,13,20,32,59,96,133,148,170,214,224,230,235,242,242],[18,19,37,58,92,127,162,188,209,252,294,324,360,382,382],[0,0,0,0,19,47,70,79,85,101,123,140,166,183,183],[0,0,0,0,0,12,30,38,43,56,58,58,58,58,58],[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3]]

for i in range(15):
    temp=[]
    for j in range(len(monthly_coffees)):
        temp.append(monthly_coffees[j][i])
    monthly_coffees1.append(temp)

for i in range(15):
    temp=[]
    for j in range(len(cumulated_coffees)):
        temp.append(cumulated_coffees[j][i])
    cumulated_coffees1.append(temp)

#col1, buff1, col2, buff2, col3 = st.columns([2,1,2,1,1])
#user = col1.text_input(label="", placeholder="User")
#user_pw = col2.text_input(label="", type="password", placeholder="pw")
#col3.write("")
#col3.write("")
#login = col3.button("Log In", help="Log in with your username and password", on_click=log_in(user, user_pw))


#-------------------------------------------------------------------------------------------------------------- monthly coffees, per person + total (line + bar chart)
coffees_monthly = st.sidebar.checkbox("Coffees per month")
if coffees_monthly:
    st.header("Coffees per month")                           
    df = pd.DataFrame(monthly_coffees1, columns=names, index=months)    #coffees per month per person
    fig1 = px.line(df, title="Number of coffees per month per person", labels={"variable":"drinkers", "index":"", "value":"Number of coffees"})
    st.plotly_chart(fig1, use_container_width=True)
    
    temp1=[]
    for i in range(len(months)):
         temp=[]
         temp.append(months[i])
         temp.append(monthly_coffees_total[i])
         temp1.append(temp)
    
    df = pd.DataFrame(temp1, columns={"months","total"})              #total coffees per month)
    fig2 = px.bar(df, x="total", y="months", title="Total number of coffees per month", labels={"months":"Number of coffees", "total":""}, text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    
col1, col2 = st.columns([1,1])                        #setting up two columns for narrower charts   


#-------------------------------------------------------------------------------------------------------------- total coffees (pie chart)
coffees_total = st.sidebar.checkbox("Total coffees")
if coffees_total:
    col1.header("Total coffees")

    temp=[]
    for i in range(len(total_coffees)):
        temp1=[]
        temp1.append(names[i])
        temp1.append(total_coffees[i])
        temp.append(temp1)
    df = pd.DataFrame(temp, columns={"names","total"}, index=names)              #total coffees pie chart
    fig3 = go.Figure(go.Pie(labels = names, values = total_coffees, sort=False, hole=.4))
    col1.plotly_chart(fig3, use_container_width=True)



#-------------------------------------------------------------------------------------------------------------- monthly ratios (stacked bar chart)
ratio_monthly = st.sidebar.checkbox("Monthly ratios")
if ratio_monthly:                                                          #with inverted months (top: Nov '20, bottom: now)
   col2.header("Monthly ratios")
   
   months_inv=[]
   temp=[]
   for i in range(len(months)):
      months_inv.append(months[len(months)-i-1])
      temp1=[]
      temp1.append(months[len(months)-i-1])
      for j in range(len(names)):
         temp1.append(monthly_ratios[j][len(months)-i-1])
      temp.append(temp1)
   temp2=[]
   temp2.append("months")
   for i in range(len(names)):
      temp2.append(names[i])
   
   df_stack=pd.DataFrame(temp, columns = temp2, index = months_inv)
   fig4 = px.bar(df_stack, x=names, y = months_inv, barmode = 'relative', labels={"y":"", "value":"Percentage", "variable":"drinkers"})#, text='value', text_auto=True)
   col2.plotly_chart(fig4, use_container_width=True)
#if ratio_monthly:                                                          #with non-inverted months (top: now, bottom: Nov '20)
#   col2.header("Monthly ratios")
#   
#   temp=[]
#   for i in range(len(months)):
#      temp1=[]
#      temp1.append(months[i])
#      for j in range(len(names)):
#         temp1.append(monthly_ratios[j][i])
#      temp.append(temp1)
#   temp2=[]
#   temp2.append("months")
#   for i in range(len(names)):
#      temp2.append(names[i])
#   
#   df_stack=pd.DataFrame(temp, columns = temp2, index = months)
#   fig4 = px.bar(df_stack, x=names, y = months, barmode = 'relative', labels={"y":"", "value":"Percentage", "variable":"drinkers"})#, text='value', text_auto=True)
#   col2.plotly_chart(fig4, use_container_width=True)


#-------------------------------------------------------------------------------------------------------------- absolute correlation (bubble chart)
correlation_abs = st.sidebar.checkbox("Absolute correlation")
if correlation_abs:
   col1.header("Absolute correlation")
   
   temp=[]
   temp1=[]
   for i in range(len(names)):
       temp1.append(i+1)
   for j in range(len(names)):
       temp.append(temp1)
   
   temp1=[]
   for i in range(len(corr_abs)):
      #for j in range(len(corr_abs[i])):
      #   temp1.append(corr_abs[i][j])
      temp1.append(corr_abs[i][0])
   
   df = pd.DataFrame(temp, columns=temp1, index=temp1)
   col2.dataframe(df)
   fig5 = px.scatter(df, size=temp1, x=df.index, y=names)
   fig5.update_layout(showlegend=False)
   col1.plotly_chart(fig5, use_container_width=True)

   
#-------------------------------------------------------------------------------------------------------------- cumulated coffees monthly (line chart)
coffees_cumulated = st.sidebar.checkbox("Cumulated coffees")
if coffees_cumulated:
    st.header("Cumulated coffees")
    
    df = pd.DataFrame(cumulated_coffees1, columns=names, index=months)
    fig10 = px.line(df, title="Number of coffees per month per person", labels={"variable":"drinkers", "index":"", "value":"Number of coffees"})
    st.plotly_chart(fig10, use_container_width=True)


      

      
      
      
    
#total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#test=st.slider("Test", "08.03.2021", "11.01.2022")

#Point = namedtuple('Point', 'x y')
#data = []

#points_per_turn = total_points / num_turns

#or curr_point_num in range(total_points):
#   curr_turn, i = divmod(curr_point_num, points_per_turn)
#   angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#   radius = curr_point_num / total_points
#   x = radius * math.cos(angle)
#   y = radius * math.sin(angle)
#   data.append(Point(x, y))

#t.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#   .mark_circle(color='#0068c9', opacity=0.5)
#   .encode(x='x:Q', y='y:Q'))
