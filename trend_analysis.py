import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import pandas_ta as ta
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")

today = date.today()
yesterday = today - timedelta(days = 1)

st.set_page_config(layout="wide")
# Streamlit app title
st.title("Stock Trend Analysis")

# User input for stock symbol
ticker_symbol = st.text_input("Enter NSE/BSE stock symbol:")

# Check if the user has entered a stock symbol
if ticker_symbol:
    # Download stock data
    ticker_symbol = ticker_symbol.strip().upper()+".NS"
    stock_data = yf.download(ticker_symbol, start="2022-01-01", end=yesterday)

    # Define parameters
    ci_period = 14
    st_period = 7
    st_multiplier = 3

    # Calculate Choppiness Index (CI)
    ci = ta.chop(stock_data['High'], stock_data['Low'], stock_data['Close'], window=ci_period)

    # Calculate SuperTrend (supertrend)
    supertrend = ta.supertrend(stock_data['High'], stock_data['Low'], stock_data['Close'], st_period, st_multiplier)
        
    # Create a DataFrame for trend analysis
    trend_data = pd.DataFrame({'Close': stock_data['Close'], 'Choppiness Index': ci, 'SuperTrend': supertrend['SUPERT_'+str(st_period)+'_'+str(st_multiplier)+'.0']})

    # Define a function to get trend status
    def get_trend_status(row):
        if row['Choppiness Index'] > 60:
            return 'Consolidation'
        elif row['SuperTrend'] < row['Close']:
            return 'Upward Trend'
        elif row['SuperTrend'] > row['Close']:
            return 'Downward Trend'

    # Apply the trend status function
    trend_data['Trend'] = trend_data.apply(get_trend_status, axis=1)
    trend_data.reset_index(inplace=True)
    

    # Create a Plotly Express scatter plot
    fig = px.scatter(trend_data, x='Date', y='Close', color='Trend',
                     color_discrete_map={'Downward Trend': 'red', 'Upward Trend': 'green', 'Consolidation': 'yellow'},
                     title=f'{ticker_symbol[:-3]} : Trend plot',
                     width=1000, height=600)

    # Display the plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please enter a valid stock symbol to analyze.")
