import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup

def get_local_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def parse_content(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    text_parsed = soup.get_text().strip().split('\n')
    temp_str, temp_value, temp_unit, humid_str, humid_value, humid_unit = text_parsed
    temp_float = float(temp_value.strip())
    humid_float = float(humid_value.strip())
    return temp_float, humid_float


def write_pandas(temperature_value, humidity_value, ddest):
    # Create a DataFrame with the current row
    time_value = time.time()
    data = pd.DataFrame({"time": [time_value],
                         "temperature": [temperature_value],
                         "humidity": [humidity_value]})
    # Append the row to the existing CSV file
    if os.path.isfile(ddest):
        data.to_csv(ddest, mode='a', header=False, index=False)
    else:
        data.to_csv(ddest, mode='w', header=True, index=False)


if __name__ == "__main__":
    # Usage
    local_ip = "192.168.1.148"  # Replace with your local IP address
    local_ip2 = "192.168.1.225"  # Replace with your local IP address
    ddest = os.path.expanduser('~/Documents/data/arduino/remote_sensor.csv')
    ddest2 = os.path.expanduser('~/Documents/data/arduino/remote_sensor2.csv')
    url = f"http://{local_ip}/"
    url2 = f"http://{local_ip2}/"
    page_content = get_local_page_content(url)
    page_content2 = get_local_page_content(url2)
    if page_content:
        temp_value, humid_value = parse_content(page_content)
        write_pandas(temp_value, humid_value, ddest=ddest)
    if page_content2:
        temp_value, humid_value = parse_content(page_content2)
        write_pandas(temp_value, humid_value, ddest=ddest2)
