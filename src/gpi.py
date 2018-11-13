import json
import requests
import time

"""
Green Power Index GSI script
"""

CHECK_INTERVAL_SECONDS = 1

GSI_CHECK_URL = "http://mix.stromhaltig.de/gsi/json/idx/04109.json"
GSI_RANGE = 36
GSI_THRESHOLD = 49

HOMEMATIC_URL = "http://172.16.50.187/"
HOMEMATIC_STATECHANGE_URL = HOMEMATIC_URL + "config/xmlapi/statechange.cgi?ise_id={id}&new_value={value}"


def get_gsi_data():
    # response = requests.get(GSI_CHECK_URL)
    # s = response.text

    s = '[{"epochtime":"1531303200","eevalue":54},{"epochtime":"1531306800","eevalue":54},{"epochtime":"1531310400","eevalue":47},{"epochtime":"1531314000","eevalue":43},{"epochtime":"1531317600","eevalue":52},{"epochtime":"1531321200","eevalue":57},{"epochtime":"1531324800","eevalue":54},{"epochtime":"1531328400","eevalue":51},{"epochtime":"1531332000","eevalue":32},{"epochtime":"1531335600","eevalue":27},{"epochtime":"1531339200","eevalue":24},{"epochtime":"1531342800","eevalue":25},{"epochtime":"1531346400","eevalue":28},{"epochtime":"1531350000","eevalue":36},{"epochtime":"1531353600","eevalue":55},{"epochtime":"1531357200","eevalue":81},{"epochtime":"1531360800","eevalue":89},{"epochtime":"1531364400","eevalue":95},{"epochtime":"1531368000","eevalue":83},{"epochtime":"1531371600","eevalue":100},{"epochtime":"1531375200","eevalue":67},{"epochtime":"1531378800","eevalue":52},{"epochtime":"1531382400","eevalue":50},{"epochtime":"1531386000","eevalue":53},{"epochtime":"1531389600","eevalue":55},{"epochtime":"1531393200","eevalue":57},{"epochtime":"1531396800","eevalue":51},{"epochtime":"1531400400","eevalue":53},{"epochtime":"1531404000","eevalue":60},{"epochtime":"1531407600","eevalue":70},{"epochtime":"1531411200","eevalue":70},{"epochtime":"1531414800","eevalue":54},{"epochtime":"1531418400","eevalue":35},{"epochtime":"1531422000","eevalue":28},{"epochtime":"1531425600","eevalue":26},{"epochtime":"1531429200","eevalue":29}]'

    return json.loads(s)


parsed_json = get_gsi_data()

global_i = 0


def gsi_check(i=None):
    # There are two ways to run gsi_check
    # 1) with `i` param specified - then it'll use it as an index to gsi table
    # 2) without `i` param - then it'll use the default counter as an index to gsi table
    if i is None:
        global global_i
        i = global_i
        global_i = (global_i + 1) % GSI_RANGE

    jsondata = parsed_json[i]
    print('Current GSI: ' + str(jsondata['eevalue']))
    print('Timestamp: ' + time.ctime(int(jsondata['epochtime'])))
    if int(jsondata['eevalue']) > GSI_THRESHOLD:
        print('> Turn on')
        url = HOMEMATIC_STATECHANGE_URL.format(id='1467', value='true')
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
    else:
        print('> Turn off')
        url = HOMEMATIC_STATECHANGE_URL.format(id='1467', value='false')
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
    print('____________________________')


def run_gsi():
    while True:
        for i in range(1, GSI_RANGE):
            gsi_check(i)
            time.sleep(CHECK_INTERVAL_SECONDS)
