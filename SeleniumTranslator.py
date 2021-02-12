from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        self.driver = webdriver.Chrome(executable_path='assets/chromedriver_stealth', options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get("https://www.deepl.com/translator")
        self.setLanguages()


    def setLanguages(self,soureLang=None,targetLang=None):
        sleep(5)
        if soureLang != None:
            self.sourceLang = soureLang
        if targetLang != None:
            self.targetLang = targetLang

        inputLanguageBtn = self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-source-lang-btn')]")
        targetLanguageBtn = self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-target-lang-btn')]")

        inputLanguageBtn.click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-lang-option-"+self.sourceLang+"')]").click()

        targetLanguageBtn.click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(@dl-test,'translator-lang-option-"+self.targetLang+"')]").click()

    def translate(self,sourceText):
        sourceInput = self.driver.find_element_by_xpath("//textarea[contains(@dl-test,'translator-source-input')]")
        targetInput = self.driver.find_element_by_xpath("//textarea[contains(@dl-test,'translator-target-input')]")

        self.clearInput(sourceInput)

        self.simulateTyping(sourceInput,sourceText,0.005)
        sleep(1)
        return targetInput.get_attribute("value")


    def checkIfElementExist(self,xpath):
        if len(self.driver.find_elements_by_xpath(xpath))>0:
            return True
        else:
            return False

    def simulateTyping(self,element,myText,mySpeed=0.01):
        for char in myText:
            sleep(mySpeed)
            element.send_keys(char)

    def clearInput(self,element):
        element.clear()

    def exit(self):
        self.driver.quit()
