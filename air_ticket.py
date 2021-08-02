from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import pickle
import sys
import os
import datetime
import conf
from email_handler import sendEmail

amadeus_user_name = conf.amadeus_user_name
amadeus_user_pwd = conf.amadeus_user_pwd
amadeus_office_id = conf.amadeus_office_id

gchrome = webdriver.Chrome(executable_path=conf.chromedirver_path)
gchrome.get(conf.amadeus_url)
sleep(10)
gchrome.find_element_by_xpath('//*[@id="w0_cookieBannerAcceptButton"]/button/span/span[2]/span').click()

# login_first_time
user_name = gchrome.find_element_by_xpath('//*[@id="w2_firstInput"]/span/input')
user_name.send_keys(amadeus_user_name)
office_id = gchrome.find_element_by_xpath('//*[@id="w2_officeId"]/span/input')
office_id.send_keys(amadeus_office_id)
password = gchrome.find_element_by_xpath('//*[@id="w2_passwordInput"]/span/input')
password.send_keys(amadeus_user_pwd)
sleep(10)
sign_in = gchrome.find_element_by_xpath('//*[@id="w7"]/button/span/span[2]/span')
sign_in.click()

sleep(60)  # <<<<<<<<<<<<<<< wait OTP SMS and otp_input box

# one time pass
one_time_pass = gchrome.find_element_by_xpath('//*[@id="w2_otpInput"]/span/input')
with open(conf.otp_path, mode='rb') as f:
    otp = f.readlines()[0].strip().decode('utf-8').strip()
    one_time_pass.send_keys(otp)
password.send_keys(amadeus_user_pwd)
sign_in.click()

sleep(10)  # wait force_sign_in load
try:
    force_sign_in = gchrome.find_element_by_xpath('//*[@id="w15"]/button/span/span[2]/span')
    force_sign_in.click()
except Exception as e:
    print(f"force_sign_in click fail. {e}")
else:
    pass

sleep(50)  # wait main page load
try:
    cookie_accept = gchrome.find_element_by_xpath(
        '//*[@id="cookiebanner_cookiebanner_cookieBannerAcceptButton"]/button/span/span[2]/span')
    cookie_accept.click()
    print(f'clicked the 2nd cookie accept button')
except Exception as e:
    print(f'accept 2nd cookie meet error: {e}')
    sleep(60)  # main page not load completed, wait another 60s
    cookie_accept = gchrome.find_element_by_xpath(
        '//*[@id="cookiebanner_cookiebanner_cookieBannerAcceptButton"]/button/span/span[2]/span')
    cookie_accept.click()

# go to command/shell page
try:
    gchrome.find_element_by_xpath('//*[@id="etoolbar_toolbarSection_newcommandpagebtn_id"]/span[2]/strong').click()
    sleep(30)  # wait shell page load fully
except Exception as e:
    print(f' click command page meet error {e}')
    sleep(20)
    gchrome.find_element_by_xpath('//*[@id="etoolbar_toolbarSection_newcommandpagebtn_id"]/span[2]/strong').click()

# locate cursor
cursor = gchrome.find_element_by_xpath(
    '//*[@id="cryptics1_cmd_shellbridge_shellWindow_top_left_modeString_cmdPromptInput"]')


def query_ticket(cmd):
    cursor.send_keys(cmd, Keys.ENTER)
    sleep(2)


def parse_result():
    try:
        query_result = gchrome.find_element_by_xpath('//*[@id="e4crypticContainer"]/div/div').text
        result_lines = query_result.split('\n')
        print(f"page_result_lines --> {result_lines}")
        valid_lines = []
        for li in result_lines:
            if '728' in li:
                valid_lines.append(li)
        position_arg = valid_lines[-1].split()[4][1]
        try:
            valid_seats_num = int(position_arg)
            return valid_seats_num
        except Exception as e:
            print(f'{e}')
    except Exception as e:
        print(f'parse_result meet error: {e}')


def book_ticket(seats):
    cursor.send_keys(f'ss{seats}j1', Keys.ENTER)
    print(f'Book ticket successful')
    sleep(3)


if __name__ == '__main__':
    i = 0
    while 1:
        i += 1
        print(f' round {i} '.center(100, '*'))
        for date in ['11aug', '18aug', '25aug', '1sep', '8sep']:
            query_ticket(f"an {date}frapvg/alh")
            ret = parse_result()
            if ret is None:
                continue
            elif isinstance(ret, int):
                book_ticket(seats=ret)
                sendEmail('订到票啦', '订到票啦啦啦')
                break