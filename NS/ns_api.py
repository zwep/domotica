# encoding: utf-8

"""
Here we are going to analyze the costs that I have made with the NS
"""

from datetime import datetime
import numpy as np
import api_secrets
import requests
import pandas as pd
import os
import json


# Define several functions that are going to help
def check_rush_hour(x):
    """
    Input should be a datetime object

    :param x:
    :return:
    """
    rush_hour = False
    if rush_hour_ochtend_1 < x.time() <= rush_hour_ochtend_2:
        # print('Spits', x)
        rush_hour = True
    if rush_hour_avond_1 < x.time() <= rush_hour_avond_2:
        # print('Spits', x)
        rush_hour = True
    return rush_hour


def get_data_row(x):
    """
    Input should be a row from the NS travel history csv
    :param x:
    :return:
    """
    date = x['Datum']
    check_in = x['Check in']
    check_in_iso = datetime.strptime(date + check_in, "%d-%m-%y%H:%M").astimezone()
    check_in_iso_str = str(check_in_iso).replace(' ', 'T')
    get_data = {'fromStation': x['Vertrek'], 'toStation': x['Bestemming'], 'plannedFromTime': check_in_iso_str}

    # With the given incheck date, check rush hour
    rush_hour_ind = check_rush_hour(check_in_iso)
    return get_data, rush_hour_ind


def get_cost_travel(travel_obj, rush_hour=False):

    cost_c = 0
    if rush_hour:
        sel_discountType = 'NO_DISCOUNT'
    else:
        sel_discountType = 'DISCOUNT_40_PERCENT'

    for i_obj in travel_obj['fares']:
        ns_travel_product = [i_obj['product'], i_obj['travelClass'], i_obj['discountType']]
        my_travel_product = [sel_product, sel_travelClass, sel_discountType]
        if ns_travel_product == my_travel_product:
            cost_c = i_obj['priceInCents']

    return cost_c


# Import travel history. Obtained via www.ns.nl
file_name = 'reistransacties-3528010491264178.csv'
file_dir = r'C:\Users\20184098\Documents\data\NS'
file_path = os.path.join(file_dir, file_name)

travel_list = pd.read_csv(file_path, encoding='latin', sep=';')
travel_list['date'] = pd.to_datetime(travel_list['Datum'], format='%d-%m-%y')
travel_list['yearmonth'] = travel_list['date'].map(lambda x: str(x.year) + str(x.month))
travel_list['cost'] = 0

# Define authorization object
auth_obj = {'username': api_secrets.NS_username, 'x-api-key': api_secrets.NS_API_KEY}
headers_browser = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
auth_obj.update(headers_browser)

# Basic API urls
basis_price_url = "https://ns-api.nl/reisinfo/api/v2/price"
basis_station_url = "https://ns-api.nl/reisinfo/api/v2/stations"
basis_trips_url = "https://ns-api.nl/reisinfo/api/v3/trips"

# List of stations with abbrevations and code
json_station = json.loads(requests.get(basis_station_url, headers=auth_obj).text)
dict_station = dict(json_station)['payload']
station_code = {x['namen']['lang']: x['code'] for x in dict_station}

# Rush hour times. Between these times, we calculate no discount method
rush_hour_ochtend_1 = datetime.time(datetime.strptime("6:30", "%H:%M"))
rush_hour_ochtend_2 = datetime.time(datetime.strptime("9:00", "%H:%M"))
rush_hour_avond_1 = datetime.time(datetime.strptime("16:00", "%H:%M"))
rush_hour_avond_2 = datetime.time(datetime.strptime("18:30", "%H:%M"))

# Product specifications
sel_travelClass = 'SECOND_CLASS'
sel_product = 'OVCHIPKAART_ENKELE_REIS'


def main(travel_list):
    """
    Runs the main part...
    :param travel_list:
    :return:
    """

    for i, i_row in travel_list.iterrows():
        if i_row['Vertrek'] is not np.nan:
            get_data, rush_hour_ind = get_data_row(i_row)
            res = requests.get(basis_trips_url, params=get_data, headers=auth_obj)

            if res.status_code == 200:
                # There is no difference between the different 'trips' elements
                travel_obj = dict(res.json())['trips'][0]
                travel_cost = get_cost_travel(travel_obj, rush_hour_ind)
                travel_cost /= 100  # Convert from cents to euros
                travel_list.at[i, 'cost'] = travel_cost
            else:
                print('Encounterd error ', res.status_code)
                print('Content json', res.json())
        else:
            continue

        return travel_list


if __name__ == "__main__":
    travel_list = main(travel_list)
    # Process to count per month spending..
    print(travel_list.groupby('yearmonth')['cost'].sum())
