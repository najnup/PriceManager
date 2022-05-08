#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from nord_pool_module import local_time, pool_prices, get_price, get_average
from flask import Flask,render_template,request

"""
Description:
Author:
Date: 
"""
print('Starting app', str(local_time(1)))
### Pool prices
prices_data = pool_prices(local_time())
app = Flask(__name__)

### Will have one page where current price is shown and it is red if the price is above average and green in case price falls below average price
### That is all for this site.
### do an adjustment for LV time

@app.route('/')
def home():
    global prices_data
    LOCAL_TIME = local_time()
    print('Page loaded at: ', str(local_time(1)))
    if get_price(prices_data, LOCAL_TIME) == 'None':
        ### If this condition is met then prices_data has to be renewed
        print('Have to renew prices!')
        prices_data = pool_prices(LOCAL_TIME)
        
    before_price = get_price(prices_data,LOCAL_TIME - timedelta(hours=1))
    now_price = get_price(prices_data,LOCAL_TIME)
    future_price = get_price(prices_data,LOCAL_TIME + timedelta(hours=1))
    average_price = get_average(prices_data)
    title_date = LOCAL_TIME.strftime('%d-%m-%Y')

    return render_template('index.html', date = title_date, before_price = float(before_price.replace(',','.')), now_price = float(now_price.replace(',','.')), future_price = float(future_price.replace(',','.')), average_price = average_price)

app.run(host='0.0.0.0', port='8080')

### Roadmap ###
# DONE - Find where to host the site (Will be hosted on digital ocean)
# Add -2h and +2h redo all that in list... so it is adjusting to input. Have a legend and price value.
# DONE - Create that prices are not obtained all the time (request is not made every time site is accessed)
# Perhaps: Add gradual coloring
# Adding of a coloring, when for example price is lower that average
