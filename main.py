# -*- coding: utf-8 -*-

# STDLIB
import io
import base64
from flask import Flask, request, render_template, jsonify

# THIRDPARTY
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
import plotly.express as px
from prophet import Prophet
import yfinance as yf



app = Flask(__name__)

def select_company(company_name):
    '''Obtain the data from Yahoo Finance'''
    # Set the ticker we want    
    yfin = yf.Ticker(company_name)

    # Select all the available data for the selected ticker     
    df = yfin.history(period="max")

    # Clean the dataframe and select only those values we need    
    df.reset_index(level=0, inplace=True)
    df = df[['Date', 'Close']]
    df['Date'] = df['Date'].dt.date

    # Select last 100 periods (only weekday are available) 
    df = df.tail(100).reset_index().drop('index', axis=1)

    return df


def run_model(company_name, period_to_predict):
    df = select_company(company_name)
    df = df.rename(columns = {"Date":"ds","Close":"y"})
    m = Prophet(daily_seasonality = True)
    m.fit(df)
    future = m.make_future_dataframe(periods=period_to_predict)
    prediction = m.predict(future)
    return prediction


def chart1(period_to_predict):
    x_axis_chart1 = prediction.ds.dt.strftime('%Y-%m-%d').tail(period_to_predict).to_list()
    close_values_chart1 = round(prediction.yhat,2.tail(period_to_predict)).to_list()
    trend_values_chart1 = round(prediction.trend,2).tail(period_to_predict).to_list()
    return x_axis_chart1, close_values_chart1, trend_values_chart1


company_name = 'MSFT'
period_to_predict = 9

prediction = run_model(company_name, period_to_predict)

df = select_company(company_name)
last_10_days_values = round(df.Close, 2).tail(20).to_list()P
last_10_days_dates = round(df.Date.astype(str), 2).tail(20).to_list()P

# testing
# zeros_time_series = [0] * 20

x_axis_chart1, close_values_chart1, trend_values_chart1 = chart1(period_to_predict)


x_axis_chart1 = x_axis_chart1
close_values_chart1 = close_values_chart1
trend_values_chart1 = trend_values_chart1


@app.route('/chart')
def chart1():
    # Create a sample dataframe
    return render_template('chart.html', x_axis_chart1=x_axis_chart1, close_values_chart1=close_values_chart1, trend_values_chart1=trend_values_chart1)

if __name__ == '__main__':
    app.run()





# @app.route('/', methods=['GET', 'POST'])
#     def plot():
#         if request.method == 'POST':
#             company_name = request.form['company_name']
#             period_to_predict = int(request.form['period_to_predict'])
#             string1 = chart1(company_name, period_to_predict)
#             string2 = chart2(company_name, period_to_predict)
#             else:
#                 string1 = ""
#                 string2 = ""
                
#             return render_template('plot.html', chart1=string1, chart2=string2)