![alt text](https://github.com/algerza/flask_prophet_web_app/blob/main/cover.jpg?raw=true)

# Predict NASDAQ future stock price

### What is this project about?

The purpose of this project is to demonstrate how to build an interactive web application powered my Machine Learning algorithms.
Disclaimer: It should not be used as the sole basis for making investment decisions.

### How does it work?

Select on the drop down menu the company name, the number of days you want to predict, and then click submit to reload the page an obtain your results.

You will find a first chart with the latest days' stock close price and the price prediction for the selected days. On the second chart you will find the time serie for the past 100 days with the actual stock close price and the model parameters, so you can observe how well the model fit the data.


<p align="center">
  <img src="https://github.com/algerza/flask_prophet_web_app/raw/main/flask_nasdaq.gif" alt="Alt Text">
</p>



### How was it built and why?

The prediction model used in this project is based on the Yahoo Finance Python library, which allows us to obtain the latest data for each company on request.

This data is then fed into the Prophet model, an open-source software developed by Facebook's Core Data Science team. Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. This makes it well suited for time series data that has strong seasonal effects and several seasons of historical data.

Therefore, Prophet is not the best choice for accurate results, but it is very simple to implement and showcase this example.

## How to use it?

Open the terminal and follow these commands (installing Docker is a pre-requisite):

Build the Docker container:

```bash
docker build --tag nasdaq_stock_prediction .
```

Run the container locally on port 8080:

```bash
docker run -d -p 8080:5000 nasdaq_stock_prediction
```

Access the website created inside Docker:

```bash
http://127.0.0.1:8080/chart
```

In order to avoid errors, please make sure there is no conflict with the process using port 8080


