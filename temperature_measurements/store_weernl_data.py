import time
import datetime
import requests
import json

# Use the weernl API to get the whole status
def get_current_weer_status():
        url_houten = 'http://weerlive.nl/api/json-data-10min.php?key=9031ec6a73&locatie=Houten'
        r = requests.get(url_houten, timeout=10, verify=False)
        content = r.content.decode("utf8")
        js = json.loads(content)
        return js['liveweer'][0]


# Add the date so we know when we asked for it and dump it
def store_stuff():
    status = get_current_weer_status()
    datetime_obj = datetime.datetime.now()
    status['date'] = datetime_obj.strftime("%Y-%m-%d|%H:%M:%S")
    serialized_dict = json.dumps(status)
    with open('/home/pi/data/weernl_data.json', 'a') as f:
        f.write(serialized_dict)


if __name__ == "__main__":
    while True:
        time.sleep(3)
        store_stuff()