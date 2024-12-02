import streamlit as st
import pandas as pd
from pymongo import MongoClient
from lightweight_charts.widgets import StreamlitChart
from datetime import timedelta
import json


mongo = MongoClient('mongodb://localhost:27017')
st.set_page_config(layout = 'wide')

indices = ['nifty50','niftyNext50','niftyFno','nifty500']
timeFrames = ['5m','15m','1D']

index = st.sidebar.selectbox('Index',indices)

if index == 'nifty50': 
    scripts = json.load(open('nifty50.json','r'))['name']
elif index == 'niftyNext50': 
    scripts = json.load(open('niftyNext50.json','r'))['name']
elif index == 'niftyFno': 
    scripts = json.load(open('niftyFno.json','r'))['name']
elif index == 'nifty500': 
    scripts = json.load(open('nifty500.json','r'))['name']
    timeFrames = ['1D']

script = st.sidebar.selectbox('Script',scripts)
timeFrame = st.sidebar.selectbox('TimeFrame',timeFrames)

chart = StreamlitChart(width=1425, height=800)  
chart.time_scale(right_offset = 10)
chart.legend(visible = True, ohlc = True, percent = True, color_based_on_candle = True, font_size = 15, lines = True)

if timeFrame == '5m':
    db_timeFrame = '5MinuteContinous'
elif timeFrame == '15m':
    db_timeFrame = '15Minute'
elif timeFrame == '1D':
    db_timeFrame = 'Daily'


df = pd.DataFrame(list(mongo[script][db_timeFrame].find()))
df.drop(columns = ['_id'], inplace = True)
df['time'] = pd.to_datetime(df['time'], unit = 's')
df['time'] = df['time'] + timedelta(hours = 5.5)
chart.set(df)

chart.load()

