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

    # Select last 100 days    
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


@app.route('/chart', methods=['GET', 'POST'])
def generate_charts():
    x_axis_chart1 = []
    close_values_chart1 = []
    trend_values_chart1 = []
    x_axis_chart2 = []
    close_values_chart2 = []
    trend_values_chart2 = []
    max_trend_values_chart2 = []
    min_trend_values_chart2 = []


    if request.method == 'POST':
        company_name = request.form['company_name']
        period_to_predict = int(request.form['period_to_predict'])

        prediction = run_model(company_name, period_to_predict)
        df = select_company(company_name)
        last_20_days_values = round(df.Close,2).tail(20).to_list()
        last_20_days_dates = df.Date.astype(str).tail(20).to_list()
        
        x_axis_chart1 = prediction.ds.dt.strftime('%Y-%m-%d').tail(period_to_predict + 20).to_list()
        close_values_chart1 = round(prediction.yhat,2).tail(period_to_predict).to_list()
        close_values_chart1 = [0]*20 + close_values_chart1
        trend_values_chart1 = last_20_days_values

        x_axis_chart2 = df.Date.astype(str).tail(100).to_list()
        close_values_chart2 = round(df.Close,2).tail(100).to_list()

        max_trend_values_chart2 = round(run_model(company_name, 100).yhat_upper.tail(100),2).to_list()
        trend_values_chart2 = round(run_model(company_name, 100).yhat.tail(100),2).to_list()
        min_trend_values_chart2 = round(run_model(company_name, 100).yhat_lower.tail(100),2).to_list()

        
    return render_template('chart.html', x_axis_chart1=x_axis_chart1, close_values_chart1=close_values_chart1, trend_values_chart1=trend_values_chart1, 
    x_axis_chart2=x_axis_chart2, close_values_chart2=close_values_chart2, trend_values_chart2=trend_values_chart2, max_trend_values_chart2 = max_trend_values_chart2, min_trend_values_chart2 = min_trend_values_chart2)



if __name__ == '__main__':
    app.run()
