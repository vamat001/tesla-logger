import teslapy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
from PIL import Image
from os import path
from multiprocessing import Process
import time

def custom_auth(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    with webdriver.Chrome(chrome_options=options, executable_path="./chromedriver") as browser:
        browser.get(url)
        WebDriverWait(browser, 300).until(EC.url_contains('void/callback'))
        return browser.current_url

def write_json(data):
    if data["shift_state"] != "D":
        print("parked")
        return
    print(data)
    if not path.isfile('streaming_data.json'):
        file = open('streaming_data.json','w')
        json.dump({"data":[]},file,indent=4)
        file.close()
    with open('streaming_data.json','r+') as f:
        try:
            file_data = json.load(f)
        except:
            print("file read exception")
            exit(1)
        file_data["data"].append(data)
        f.seek(0)
        json.dump(file_data,f,indent=4)

def main():
    tesla = teslapy.Tesla("elon@tesla.com",cache_file="cache.json",authenticator=custom_auth)
    # tesla oauth2/v3
    try:
        if not tesla.authorized:
            print("redirecting to tesla sso for first time login...")
            tesla.fetch_token()
            # print(tesla.vehicle_list()[0])
        else:
            print("getting cached token...")
            # print(tesla.vehicle_list()[0])
    except:
        print("there was a problem logging in please try again later")
    
    vehicle = tesla.vehicle_list()[0]
    # vehicle.sync_wake_up()
    print(vehicle["display_name"] + ' last seen ' + vehicle.last_seen()+ " at " + str(vehicle['charge_state']['battery_level']) + '% SoC')
    # img_hex = vehicle.compose_image()
    if vehicle.available():
        vehicle.stream(write_json,indefinitely=True)
    else:
        print("vehicle offline")

if __name__ == "__main__":
    main()
