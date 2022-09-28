# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys
import time
import requests
import schedule
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, HardwareType

import configs

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value]
hardware_types = [HardwareType.COMPUTER.value]

user_agent_rotator = UserAgent(software_names=software_names,
                               operating_systems=operating_systems,
                               hardware_types=hardware_types,
                               limit=10)
user_agent = user_agent_rotator.get_user_agents()

logging.basicConfig(level=configs.LOG_LEVEL)
logger = logging.getLogger(__name__)

if not sys.platform.startswith('win'):
    from pyvirtualdisplay import Display

    display = Display(visible=False, size=(1800, 1000))
    display.start()


def send_image(filename, message="test"):
    data = {'chat_id': configs.MY_ID,
            'caption': message + "\n" + str(datetime.datetime.today()),
            }
    requests.post(f"https://{configs.SERVER_URL}/bot{configs.TOKEN}/sendPhoto",
                  data=data, files={"photo": open(filename, "rb")})


def config_chrome():
    chrome_options = webdriver.ChromeOptions()
    if configs.RUN_HEADLESS:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=1800,1440")
    if not sys.platform.startswith('win'):
        chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


def visit_site(web_url):
    logger.info(f"visiting {web_url} at {datetime.datetime.now()}")
    try:
        driver = webdriver.Chrome(service=Service(os.path.join(configs.BASE_DIR, "chromedriver")),
                                  options=config_chrome())
        driver.get(web_url)
        driver.implicitly_wait(60)

        image_file = os.path.join("screenshots", str(time.time()) + ".png")
        WebDriverWait(driver, 60)
        driver.save_screenshot(image_file)
        return image_file
    except Exception as e:
        logger.error(e)


def check_websites():
    for url in configs.URLS:
        url = url.strip()
        if url:
            try:
                image_name = visit_site(url)
                if image_name:
                    send_image(image_name, url)
                    os.remove(image_name)
            except Exception as e:
                logger.error(e)


if __name__ == '__main__':
    logger.info("Service started at " + str(datetime.datetime.now()))
    schedule.every().day.at(configs.TIME_TO_CHECK).do(check_websites)
    while True:
        schedule.run_pending()
        time.sleep(1)
