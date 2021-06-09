from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import yaml
import json
import os
import re


# https://degitalization.hatenablog.jp/entry/2021/03/13/102805 pdf印刷について
# headlessで保存は現状無理そう
def printSetUp(save_dir):
    ch_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [
            {
                "account": "",
                "id": "Save as PDF",
                "origin": "local",
                "displayName": "Save as PDF",
            }
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }
    prefs = {
        "profile.default_content_setting_values.automatic_downloads": 1,
        "plugins.plugins_disabled": "Chrome PDF Viewer",
        "download_restrictions": 0,
        "download.default_directory": save_dir,
        # Need this for HTML files
        "savefile": {
            "default_directory": save_dir,
            "type": 1,  # Complete HTML
        },
        "download.prompt_for_download": False,
        "printing.default_destination_selection_rules": json.dumps(
            {
                "kind": "local",
                "idPattern": ".*",
                "namePattern": "Save as PDF",
            }
        ),
        "printing.print_preview_sticky_settings": {
            "appState": json.dumps(settings)
        },
        "use_system_default_printer": False,
    }
    # ch_options.add_argument("--headless")
    ch_options.add_argument("--kiosk")
    ch_options.add_argument("--kiosk-printing")
    ch_options.add_experimental_option('prefs', prefs)

    return ch_options


def main(config):
    save_dir = config.get('DMM').get('save_dir')
    ch_options = printSetUp(save_dir)
    driver = webdriver.Chrome(chrome_options=ch_options)
    driver.get('https://accounts.dmm.com/service/login/password/=/path=DRVESRUMTh1dDFpZWkEHGQUIWxhTVgkWAxJHSUcWUkIWTlRUCxsNXV8MXxdQVwpbAwRVXQ9KEFgWBwoDA1JUU1xQUxRVBFhUFVEIDwYbBARXAxtVAghTXFZQDlZTVlM_')
    actions = ActionChains(driver)
    # login page
    driver.find_element_by_name('login_id').send_keys(config.get('DMM').get('email'))
    driver.find_element_by_name('password').send_keys(config.get('DMM').get('password'))
    driver.find_elements_by_xpath('//*[@id="loginbutton_script_on"]/span/input')[0].click()
    time.sleep(5)
    # main画面
    actions.move_to_element(driver.find_element_by_xpath('/html/body/header/div[2]/div[2]/span')).perform() # 右上の人マーク
    driver.find_elements_by_xpath('/html/body/header/div[2]/div[2]/div/div[2]/div[2]/div[1]/ul/li/a/span[1]')[0].click() # アカウント情報クリック
    time.sleep(5)
    # アカウント情報画面
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/ul/li[1]/a').click() # 購入履歴クリック
    time.sleep(5)
    # 購入履歴画面
    date = driver.find_element_by_xpath('//*[@id="main-history-purchase"]/div[2]/div/table/tbody/tr/td[1]').text # 日付取得
    month = re.match(r'\d{4}/(\d{1,2})/\d{1,2}', date).group(1)
    driver.find_element_by_xpath('//*[@id="main-history-purchase"]/div[2]/div/table/tbody/tr/td[5]/a').click()
    # 領収証の発行画面
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="receipt_name"]').send_keys(config.get('DMM').get('receipt_name'))
    driver.find_element_by_id('confirm').click()
    driver.find_element_by_xpath('//*[@id="issue"]/div[2]/span[2]/input').click()
    driver.find_element_by_xpath('//*[@id="print"]').click()
    # driver.execute_script('return window.print()')
    time.sleep(10) # save待ち
    os.rename(f'{save_dir}/領収書の発行 - DMM.com.pdf', f'{save_dir}/{month}月分領収証.pdf')
    driver.quit()



if __name__ == "__main__":
    with open('../config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    main(config)