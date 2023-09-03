![alt text](https://github.com/algerza/flask_prophet_web_app/blob/main/cover.jpg?raw=true)

# Predict NASDAQ future stock price

### What is this project about?

The purpose of this project is to demonstrate how to build an interactive web application powered my Machine Learning algorithms.
Disclaimer: It should not be used as the sole basis for making investment decisions.

### How does it work?

Select on the drop down menu the company name, the number of days you want to predict, and then click submit to reload the page an obtain your results.

You will find a first chart with the latest days' stock close price and the price prediction for the selected days. On the second chart you will find the time serie for the past 100 days with the actual stock close price and the model parameters, so you can observe how well the model fit the data.

<h3 align="center"><img src="https://github.com/algerza/flask_prophet_web_app/blob/main/flask_nasdaq.gif?raw=true"/></h3>

### How was it built and why?

The prediction model used in this project is based on the Yahoo Finance Python library, which allows us to obtain the latest data for each company on request.

This data is then fed into the Prophet model, an open-source software developed by Facebook's Core Data Science team. Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. This makes it well suited for time series data that has strong seasonal effects and several seasons of historical data.

Therefore, Prophet is not the best choice for accurate results, but it is very simple to implement and showcase this example.

## Development

### Docker

Build the Docker container:

```bash
docker build --tag nasdaq_stock_prediction .
```

Run the container locally on port 8080:

```bash
docker run -d -p 8080:5000 nasdaq_stock_prediction
```
