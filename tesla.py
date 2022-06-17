import teslapy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import binascii
from PIL import Image
import io


def custom_auth(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    with webdriver.Chrome(chrome_options=options, executable_path="./chromedriver") as browser:
        browser.get(url)
        WebDriverWait(browser, 300).until(EC.url_contains('void/callback'))
        return browser.current_url

def get_cached_token():
    with open("cache.json") as cache:
        return json.load(cache)["auth_token"]

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
    # print(vehicle.get_charge_history())
    # print(vehicle.get_latest_vehicle_data())
    # img_hex = vehicle.compose_image()
    # img_bytes = binascii.unhexlify(img_hex)
    # img_stream = io.BytesIO(img_bytes)
    # img = Image.open(img_hex)
    print(vehicle)

if __name__ == "__main__":
    main()
