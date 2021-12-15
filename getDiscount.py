from selenium import webdriver
import time
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import os
from consts import *



cwd = os.getcwd()
PATH = cwd + '/chromedriver'


opt = webdriver.ChromeOptions()
opt.add_extension('./metamask.crx')
driver = webdriver.Chrome(chrome_options=opt)
time.sleep(0.9)

current_window = driver.current_window_handle

chwd = driver.window_handles

for w in chwd:
    if w != current_window:
        driver.switch_to.window(w)
    break

time.sleep(0.9)

driver.find_element_by_xpath('//button[text()="Get Started"]').click()
driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
driver.find_element_by_xpath('//button[text()="No Thanks"]').click()

time.sleep(0.9)

inputs = driver.find_elements_by_xpath('//input')
inputs[0].send_keys(mnemonic)
inputs[1].send_keys('thisisthetest')
inputs[2].send_keys('thisisthetest')
driver.find_element_by_css_selector('.first-time-flow__terms').click()

time.sleep(0.9)

driver.find_element_by_xpath('//button[text()="Import"]').click()

time.sleep(5)

driver.find_element_by_xpath('//button[text()="All Done"]').click()
driver.get('https://pro.olympusdao.finance/#/bond')
driver.find_element_by_class_name('wallet-menu').click()

time.sleep(0.9)

driver.find_element_by_class_name('sc-eCApGN').click()

time.sleep(0.9)

chwd = driver.window_handles

driver.switch_to.window(chwd[2])

time.sleep(0.9)
driver.find_element_by_xpath('//button[text()="Next"]').click()
time.sleep(0.9)
driver.find_element_by_xpath('//button[text()="Connect"]').click()
time.sleep(40)

driver.switch_to.window(chwd[0])

container_rows = driver.find_elements_by_class_name('bond-grid-data-row')

client = influxdb_client.InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)
result = []
for row in container_rows:
    obj = {
        'bond': '',
        'token': '',
        'roi': ''
    }
    data = row.text.split('\n')
    obj['bond'] = data[0]
    if len(data) == 8:
        obj["token"] = data[2]
        obj["roi"] = data[5]
    elif len(data) == 9:
        obj["token"] = data[3]
        obj["roi"] = data[6]
    else:
        continue
    result.append(obj)
    try:
        p = influxdb_client.Point(data[0]).field("discount", float(obj['roi'][:-1]))
        write_api.write(bucket=bucket, org=org, record=p)
    except:
        print('Influx Error!')




