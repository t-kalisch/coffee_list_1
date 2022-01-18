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
st.write(plotly.__version__)
   
def log_in(user, user_pw):
    st.write(user)
    st.write(user_pw)
    #start.disabled = False
    
st.sidebar.header("Sign in:")
user = st.sidebar.text_input(label="", placeholder="Username")
user_pw = st.sidebar.text_input(label="", type="password", placeholder="Password")
login = st.sidebar.button("Log In", help="Log in with your username and password", on_click=log_in(user, user_pw))
st.sidebar.title("Available diagrams:")

monthly_coffees1=[]
monthly_coffees=[[19, 9, 16, 19, 29, 31, 32, 30, 14, 41, 39, 34, 37, 24, 10], [15, 6, 6, 20, 29, 20, 24, 25, 29, 22, 32, 30, 35, 18, 12], [13, 6, 12, 16, 25, 35, 28, 37, 31, 27, 36, 30, 22, 14, 0], [10, 3, 7, 12, 27, 36, 37, 15, 22, 44, 10, 6, 4, 7, 1], [18, 1, 18, 21, 34, 35, 35, 26, 21, 43, 43, 27, 36, 22, 9], [0, 0, 0, 0, 19, 27, 23, 9, 5, 16, 22, 17, 26, 17, 0], [0, 0, 0, 0, 0, 12, 18, 8, 5, 13, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0]]
total_coffees=[372, 314, 328, 242, 382, 183, 58, 1, 3]
names=['TK','PB','NV','DB','FLG','SHK','TB','TT','RS']
months=["Nov '20","Dec '20", "Jan '21", "Feb '21", "Mar '21", "Apr '21", "May '21", "Jun '21", "Jul '21", "Aug '21", "Sep '21", "Oct '21", "Nov '21", "Dec '21", "Jan '22"]
#months=['Nov 20','Dec 20','Jan 21','Feb 21','Mar 21','Apr 21','May 21','Jun 21','Jul 21','Aug 21','Sep 21','Oct 21','Nov 21','Dec 21','Jan 22']
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

    
coffees_monthly = st.sidebar.checkbox("Coffees per month")
if coffees_monthly:
    st.header("Coffees per month per person")
    df = pd.DataFrame(monthly_coffees1, columns=names, index=months)
    st.dataframe(df)
   
    #st.write(alt.Chart(df).mark_bar().encode(x=alt.X('months', sort=None),y='monthly_coffees1',))
      
   
    st.line_chart(df, width=0, height=0, use_container_width=True)
      
      
      
    fig = px.scatter(df, index="", values="number of coffees", title="Number of coffees per month per person")
    st.plotly_chart(fig)
       
    
coffees_total = st.sidebar.checkbox("Total coffees")
if coffees_total:
    st.header("Total coffees")
    fig = go.Figure(go.Pie(labels = names,values = total_coffees,hoverinfo = "label+percent",textinfo = "value"))
    st.plotly_chart(fig)
    


coffees_cumulated = st.sidebar.checkbox("Cumulated coffees")
if coffees_cumulated:
    st.header("Cumulated coffees")
    df = pd.DataFrame(cumulated_coffees1, columns=names)
    st.line_chart(data=df, width=0, height=0, use_container_width=True)

    
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
