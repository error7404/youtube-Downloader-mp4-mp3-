from selenium import webdriver
from selenium.webdriver.common.keys import Keys #import the keyboard keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException

from bs4 import BeautifulSoup
import requests

from time import sleep

def start_driver(url):
    """start chrome driver with the url as maximised"""
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--start-maximized")
    driver = webdriver.PhantomJS("phantomjs.exe")

    driver.get(url)
    return driver

def main(url):
    driver = start_driver(url)
    start(driver)

def start(driver):
    input_field = driver.find_element_by_xpath("//input")
    with open("link.txt", "r") as f:
        input_field.send_keys(f.read())
    input_field.send_keys(Keys.ENTER)
    delay = 20 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'progress')]")))
    except TimeoutException:
        print("Loading took too much time!")
    while True:
        try:
            myElem = driver.find_element_by_xpath("//div[contains(@class, 'progress')]")
        except NoSuchElementException:
            sleep(1)
            break
    # driver.save_screenshot('screen.png')
    button = driver.find_elements_by_xpath("//button")
    try:
        button[-1].click()
    except ElementClickInterceptedException:
        close_ifram = driver.find_element_by_xpath("//span[contains(@class, 'labs-iframe-close-button')]")
        close_ifram.click()
        sleep(.2)
        button[-1].click()
    except ElementNotInteractableException:
        driver.refresh()
        start(driver)

    print(driver.window_handles)
    if not len(driver.window_handles) == 2:
        driver.refresh()
        start(driver)
    else:
        driver.switch_to.window(driver.window_handles[0])
        # driver.save_screenshot('screen2.png')
        sleep(1)
        soup = BeautifulSoup(driver.page_source,features="html.parser")
        a = soup.find("a",class_="btn btn-primary")
        with open("music.mp3", "wb") as f:
            f.write(requests.get(a['href']).content)
        print(a)

        driver.quit()

if __name__ == "__main__":
    url = "https://mp3-youtube.download/en/faster-audio-converter"
    main(url)
    