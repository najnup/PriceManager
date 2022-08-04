#!/usr/bin/env python

"""
Description: Application built to folow price changes. Using python module for Nord Pool price extraction for LV region.
Author: Najnup
Date: 03.03.2022
Disclaimer: In this example NordPool price extraction is used for learning purposes not used for commercial purpose in any way. NordPool has data portal available, more details on - https://www.nordpoolgroup.com/en/services/power-market-data-services/dataportalregistration/
            All information here is used merely for educational and informational purposes. It is not intended as a substitute for professional advice. Should you decide to act upon any information here, you do so at your own risk.
"""

from datetime import datetime
from datetime import timedelta
from nord_pool_module import local_time, pool_prices, get_price, get_average
from flask import Flask,render_template,request
import logging

### Flag that sets where and how app will run
development = False
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

### Define dictionary preparation function
def prepare_dict(prices_data, local_time):
    ### Funcrtion prepares dictionary of the price values that will be displayed on webpage.
    ### variable returning certain number of items in dictionary, has to be uneven
    number = 9

    if number%2 == 0:
        logging.info('Please, select odd number!')
        return None

    ### Offset values for dictionaries
    #offset = -(number-1)/2 - used to start in the middle
    offset = -2
    
    
    ### Define dictionary
    prices_dict = []

    for i in range(number):
        current = i + offset
        current_price = get_price(prices_data, local_time + timedelta(hours=current))
        prices_dict.append({'hour':current, 'price':float(current_price.replace(',','.'))})
    return prices_dict

### Pool prices
prices_data = pool_prices(local_time())
print(prepare_dict(prices_data,local_time(1)))

app = Flask(__name__)
### Will have one page where current price is shown and it is red if the price is above average and green in case price falls below average price
### That is all for this site.
### do an adjustment for LV time

@app.route('/')
def home():
    logging.info('New page visit!')
    logging.info(request.remote_addr)
    
    global prices_data
    LOCAL_TIME = local_time()
    
    try:
        ### If successful will render the page
        if get_price(prices_data, LOCAL_TIME) == '0':
            ### If this condition is met then prices_data has to be renewed
            prices_data = pool_prices(LOCAL_TIME)
            logging.info('Prices renewed')
        
        ### List of prices
        prices_dict = prepare_dict(prices_data, LOCAL_TIME)
        average_price = get_average(prices_data)
        title_date = LOCAL_TIME.strftime('%d-%m-%Y')

        return render_template('index.html', date = title_date, prices_dict = prices_dict, average_price = average_price)
    
    except:
        ### Executigng this if page has failed.
        print('There was somethoing terribly wrong with the page.')

### This is for development
if development: 
    logging.info('App loaded in Debugging mode')
    app.run(host='0.0.0.0', port='8080')
