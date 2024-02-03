
from selenium.webdriver.chrome.service import Service
import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
import os
from webdriver_manager.chrome import ChromeDriverManager


def login():
    command = "google-chrome --user-data-dir=$HOME/insta-scraper --incognito --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222 --blink-settings=imagesEnabled=true"
    subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, close_fds=True)
    time.sleep(5)

    # home_directory = os.path.expanduser("~")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", f'127.0.0.1:{9222}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('https://instagram.com')
    time.sleep(2)
    username = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.NAME, "username"))
    username.clear()
    username.send_keys("mahdizubayer@gmail.com")
    password = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.NAME, "password"))
    password.clear()
    password.send_keys("as598249")
    submit_user = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//button[@type='submit']"))
    submit_user.click()

    do_not_save = WebDriverWait(driver, 30).until(lambda x: x.find_elements(By.CSS_SELECTOR, 'button[type="button"]'))
    do_not_save[0].click()
    time.sleep(10)
    all_cookies = driver.get_cookies()
    cookie_header = "; ".join([f'"{cookie["name"]}": "{cookie["value"]}"' for cookie in all_cookies])
    print(cookie_header)
    print('done')
    driver.close()
    driver.quit()


login()
