# STDLIBimport ioimport base64from flask import Flask, request, render_template, jsonify
# THIRDPARTYimport matplotlib.pyplot as pltimport matplotlibimport matplotlib.dates as mdatesimport pandas as pdimport plotly.express as px                                                  from prophet import Prophetimport yfinance as yf

# RENDER IN BACKEND# Agg a non-interactive backend that can only write to files# matplotlib.use('Agg')
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

    # Select last 365 days    
    df = df.tail(365).reset_index().drop('index', axis=1)

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
    x_axis_chart1 = prediction.ds.dt.strftime('%Y-%m-%d').to_list()
    close_values_chart1 = round(prediction.yhat,2).to_list()
    return x_axis_chart1; close_values_chart1
    
trend_values_chart1 = round(prediction.trend,2).to_list()






















def plot1(company_name, period_to_predict):
    plt.figure()
    df = select_company(company_name)
    df = df.rename(columns = {"Date":"ds","Close":"y"})
    m = Prophet(daily_seasonality = True)
    m.fit(df)
    future = m.make_future_dataframe(periods=period_to_predict) 

    #we need to specify the number of days in future
    prediction = m.predict(future)
    prediction_plot_df = prediction[['ds', 'yhat_lower', 'yhat', 'yhat_upper']].tail(7).reset_index().drop('index', axis=1)

    # Create the line plot
    plt.plot(prediction_plot_df.ds, prediction_plot_df.yhat, label='Stock Price Prediction')
    # Fill the area between the max and min values
    plt.fill_between(prediction_plot_df.ds, prediction_plot_df.yhat_lower, prediction_plot_df.yhat_upper, color='gray', alpha=0.1)
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($)")
    plt.xticks(rotation=30)

    return None

def plot2(company_name, period_to_predict):
    plt.figure()
    df = select_company(company_name)
    df = df.rename(columns = {"Date":"ds","Close":"y"}) 

    #renaming the columns of the datas
    m = Prophet(daily_seasonality = True)
    m.fit(df)
    future = m.make_future_dataframe(periods=period_to_predict)

    #we need to specify the number of days in future
    prediction = m.predict(future)
    m.plot(prediction)
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($)")
    plt.xticks(rotation=30)

    return None



@app.route('/', methods=['GET', 'POST'])
    def plot():
        if request.method == 'POST':
            company_name = request.form['company_name']
            period_to_predict = int(request.form['period_to_predict'])
            string1 = chart1(company_name, period_to_predict)
            string2 = chart2(company_name, period_to_predict)
            else:
                string1 = ""
                string2 = ""
                
            return render_template('plot.html', chart1=string1, chart2=string2)


def chart1(company_name, period_to_predict):
    # fig = plot1('AAPL')    
    fig = plot1(company_name, period_to_predict)

    # convert the chart to a png image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string1 = base64.b64encode(buf.read()).decode()
    
    return string1

def chart2(company_name, period_to_predict):
    # fig = plot2('AAPL')
    fig = plot2(company_name, period_to_predict)
    
    # convert the chart to a png image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string2 = base64.b64encode(buf.read()).decode()
    return string2


@app.route('/chart')
def chart():
    # Create a sample dataframe
    return render_template('chart.html')



if __name__ == '__main__':
    app.run()




















#-------- OBTAIN DATA FROM YAHOO FINANCE --------#
# Set the ticker we want# yfin = yf.Ticker('AAPL')
# # Select all the available data for the selected ticker # df = yfin.history(period="max")
# # Clean the dataframe and select only those values we need# df.reset_index(level=0, inplace=True)# df = df[['Date', 'Close']]# df['Date'] = df['Date'].dt.date
# df = df.loc[10300:]# df_stock_history = df.copy()
#-------- SET UP THE MODEL AND PARAMETERS --------## df = df.rename(columns = {"Date":"ds","Close":"y"}) #renaming the columns of the datas# m = Prophet(daily_seasonality = True) # the Prophet class (model)# m.fit(df) # fit the model using all data
#-------- PREDICTION AND PLOTTING --------## future = m.make_future_dataframe(periods=7) #we need to specify the number of days in future# prediction = m.predict(future)# m.plot(prediction)# plt.title("Prediction of the Tesla Stock Price using the Prophet")# plt.xlabel("Date")# plt.ylabel("Close Stock Price")# plt.show()


# def chart1():#     # generate a line chart using matplotlib#     #-------- PREDICTION AND PLOTTING --------##     df = df.rename(columns = {"Date":"ds","Close":"y"}) #renaming the columns of the datas#     m = Prophet(daily_seasonality = True)#     m.fit(df)#     future = m.make_future_dataframe(periods=7) #we need to specify the number of days in future#     prediction = m.predict(future)#     prediction_plot_df = prediction[['ds', 'yhat_lower', 'yhat', 'yhat_upper']].tail(7).reset_index().drop('index', axis=1)
#     # Create the line plot#     plt.plot(prediction_plot_df.ds, prediction_plot_df.yhat, label='Stock Price Prediction')
#     # Fill the area between the max and min values#     plt.fill_between(prediction_plot_df.ds, prediction_plot_df.yhat_lower, prediction_plot_df.yhat_upper, color='gray', alpha=0.1)
#     # convert the chart to a png image#     buf = io.BytesIO()#     plt.xlabel('Date')#     plt.ylabel('Stock')#     plt.legend()#     plt.savefig(buf, format='png')#     buf.seek(0)#     string1 = base64.b64encode(buf.read()).decode()
#     return string1
# def chart2():
#     df = df.rename(columns = {"Date":"ds","Close":"y"}) #renaming the columns of the datas#     m = Prophet(daily_seasonality = True)#     m.fit(df)#     future = m.make_future_dataframe(periods=7) #we need to specify the number of days in future#     prediction = m.predict(future)#     prediction_plot_df = prediction[['ds', 'yhat_lower', 'yhat', 'yhat_upper']].tail(7).reset_index().drop('index', axis=1)
#     # Create the line plot#     plt.plot(prediction_plot_df.ds, prediction_plot_df.yhat, label='Stock Price Prediction')
#     # Fill the area between the max and min values#     plt.fill_between(prediction_plot_df.ds, prediction_plot_df.yhat_lower, prediction_plot_df.yhat_upper, color='gray', alpha=0.1)
#     # convert the chart to a png image#     buf = io.BytesIO()#     plt.xlabel('Date')#     plt.ylabel('Stock')#     plt.legend()#     plt.savefig(buf, format='png')#     buf.seek(0)#     string2 = base64.b64encode(buf.read()).decode()
#     return string2

# string1 = chart1()
# string2 = chart2()



# @app.route('/')# def home():#     return render_template('home.html')
# @app.route('/plot')# def plot():#     # string1 = chart1()
#     # string2 = chart2()#     # # generate a line chart using matplotlib#     # x = [1, 2, 3, 10, 5]#     # y = [2, 10, 6, 8, 10]#     # plt.plot(x, y)
#     # # convert the chart to a png image#     # buf = io.BytesIO()#     # plt.savefig(buf, format='png')#     # buf.seek(0)#     # string2 = base64.b64encode(buf.read()).decode()
#     # render the template with the chart#     return render_template('plot.html', chart1=string1, chart2=string2)



# # @app.route('/plot')# # def plot():# #     # generate a line chart using matplotlib# #     x = [1, 2, 3, 4, 5]# #     y = [2, 4, 6, 8, 10]# #     plt.plot(x, y)
# #     # convert the chart to a png image# #     buf = io.BytesIO()# #     plt.savefig(buf, format='png')# #     buf.seek(0)# #     string = base64.b64encode(buf.read()).decode()
# #     # render the template with the chart# #     return render_template('plot.html', chart=string)
# if __name__ == '__main__':#     app.run()