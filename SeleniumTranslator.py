from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from pathlib import Path

from time import sleep
import random

import os
from os import listdir
from os.path import isfile, join

class SeleniumTranslator:

    def __init__ (self, sourceLang, targetLang):
        self.service = "https://www.deepl.com/translator"
        self.sourceLang = sourceLang
        self.targetLang = targetLang

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,OperatingSystem.LINUX.value]

        user_agent_rotator = UserAgent(software_names=software_names,operating_systems=operating_systems,limit=100)

        user_agent = user_agent_rotator.get_random_user_agent()

        print("ST uses agent: " +user_agent)

        chrome_options = Options()
        chrome_options.add_argument("Cache-Control=no-cache")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--dns-prefetch-disable")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("window-size=900,1000")

        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        self.driver = webdriver.Chrome(executable_path='assets/chromedriver_stealth', options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://www.deepl.com/translator")
        self.setLanguages()


    def setLanguages(self,soureLang=None,targetLang=None):
        if soureLang != None:
            self.sourceLang = soureLang
        if targetLang != None:
            self.targetLang = targetLang

        inputLanguageBtn = self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-source-lang-btn')]")
        targetLanguageBtn = self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-target-lang-btn')]")

        inputLanguageBtn.click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-lang-option-"+self.sourceLang+"')]").click()

        targetLanguageBtn.click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-lang-option-"+self.targetLang+"')]").click()

    def translate(self,sourceText):
        sourceInput = self.driver.find_element_by_xpath("//textarea[contains(@dl-test,'translator-source-input')]")
        targetInput = self.driver.find_element_by_xpath("//textarea[contains(@dl-test,'translator-target-input')]")

        self.simulateTyping(sourceInput,sourceText,0.1)
        sleep(2)
        return targetInput.get_attribute("value")


    def checkIfElementExist(self,xpath):
        if len(self.driver.find_elements_by_xpath(xpath))>0:
            return True
        else:
            return False

    def simulateTyping(self,element,myText,mySpeed=0.3):
        for char in myText:
            sleep(mySpeed)
            element.send_keys(char)

    def exit(self):
        self.driver.quit()
