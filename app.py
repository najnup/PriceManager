#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from nord_pool_module import local_time, pool_prices, get_price, get_average
from flask import Flask,render_template,request

### Flag that sets where and how app will run
development = False

"""
Description:
Author:
Date: 
"""
### Define dictionary preparation function
def prepare_dict(prices_data, local_time):
    ### Funcrtion prepares dictionary of the price values that will be displayed on webpage.
    ### variable returning certain number of items in dictionary, has to be uneven
    number = 5

    if number%2 == 0:
        print('Please, select odd number!')
        return None

    ### Offset values for dictionaries
    offset = -(number-1)/2
    ### Define dictionary
    prices_dict = []

    for i in range(number):
        current = i + offset
        current_price = get_price(prices_data, local_time + timedelta(hours=current))
        prices_dict.append({'hour':current, 'price':float(current_price.replace(',','.'))})
    return prices_dict

print('Starting app', str(local_time(1)))
### Pool prices
prices_data = pool_prices(local_time())
print(prepare_dict(prices_data,local_time(1)))

app = Flask(__name__)
### Will have one page where current price is shown and it is red if the price is above average and green in case price falls below average price
### That is all for this site.
### do an adjustment for LV time

@app.route('/')
def home():
    global prices_data
    LOCAL_TIME = local_time()
    print('Page loaded at: ', str(local_time(1)))
    if get_price(prices_data, LOCAL_TIME) == '0':
        ### If this condition is met then prices_data has to be renewed
        print('Have to renew prices!')
        prices_data = pool_prices(LOCAL_TIME)
    
    ### List of prices
    prices_dict = prepare_dict(prices_data, LOCAL_TIME)
    average_price = get_average(prices_data)
    title_date = LOCAL_TIME.strftime('%d-%m-%Y')

    return render_template('index.html', date = title_date, prices_dict = prices_dict, average_price = average_price)

### This is for development
if development: 
    app.run(host='0.0.0.0', port='8080')

### Roadmap ###

# In place where is now add current time
# Gradual coloring for prices
# DONE - Make fit good when looked upon mobile device. Asdjust procentages
# DONE - Find where to host the site (Will be hosted on digital ocean)
# DONE - Create that prices are not obtained all the time (request is not made every time site is accessed)
# DONE - Add -2h and +2h redo all that in list... so it is adjusting to input. Have a legend and price value.
# DONE - Adding of a coloring, when for example price is lower that average
