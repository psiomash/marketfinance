
# ANNUALIZED VOLATILITY CALCULATOR  ------------------------------------------

# This program computes the annualized volatility of a stock using historical data from
# Yahoo Finance API. It retrieves daily opening and closing prices for a specific period
# and computes daily price variation and then calculates the standard deviation of these
# variation. It is then annualized by multiplying it by the square root of 252 (number of
# trading days in a year) providing a measure of the stock's price volatility over a period
# of time.


# Informations to give are the following -------------------------------------

import yfinance as yf
from pymathematics import sqrt

ticker = 'AAPL'                 # Ticker de l'entreprise
start_period = '2023-1-1'       # Période de début
end_period = '2023-12-31'       # Période de fin


# Beginning of the code ------------------------------------------------------


# Information recovery from Yahoo Finance via API

def data_recovery(ticker, start_period, end_period):
    data = yf.Ticker(ticker)
    dataDF = data.history(period='1d', start=start_period, end=end_period)
    dictionnaire = dataDF.to_dict(orient='list')
    return (dictionnaire['Open'], dictionnaire['Close'])

data_recovery = data_recovery(ticker, start_period, end_period)
open_price = data_recovery[0]
close_price = data_recovery[1]

# Annualized volatility calculation

def volatility_calculation(open_price, close_price):
    # Retrieving % variations from a list
    variation = []
    for i in range(len(open_price)):
        var = ((close_price[i]-open_price[i])/open_price[i])*100
        variation.append(var)
    # Count the number of variations equivalent to the length of the list
    variation_number = len(variation)
    # Calculating the average variation
    variation_sum = 0.0
    for number in variation:
        variation_sum = variation_sum + number
    variation_mean = variation_sum / variation_number
    numerator = 0.0
    for i in range(len(variation)):
        num = (variation[i] - variation_mean) ** 2
        numerator = numerator + num
    # Calculating the standard deviation of variations
    std_dev = sqrt(numerator / variation_number)
    # Returns annualized volatility
    return round(std_dev * sqrt(252),2)


# Function execution ---------------------------------------------------------

volatility = volatility_calculation(open_price, close_price)

ticker_name = yf.Ticker(ticker)
company_name = ticker_name.info['longName']
print(f"The annualized volatility of {company_name} is {volatility} %")



