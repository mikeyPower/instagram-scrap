# Import libraries
import requests
import time
from bs4 import BeautifulSoup
import re
import os
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities







def get_image_links(html_page,image_list):
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(html_page, "html.parser")

    # Image URL is in text/javascrpt
    quote = soup.findAll('script', {"type": "text/javascript"})

    b = re.findall(r'["](.*?)["]',str(quote))

    for i in b:
        try:
            if(".jpg" in i):
                url = i.replace("\\u0026","&")
                print(url)
                count = 1
                if(url in image_list):
                    continue
                else:
                    image_list.append(url)
            else:
                continue
        except:
            print("error")
    return(image_list)















# Current directory
path = os.getcwd()


insta_photos = path+"/photos/"

try:
    os.mkdir(insta_photos)
except OSError:
    print ("Creation of the directory %s failed" % insta_photos)
else:
    print ("Successfully created the directory %s " % insta_photos)


# Set the URL you want to webscrape from
url = 'https://www.instagram.com/lifeatdeloitteireland/?hl=en'


browser = webdriver.Firefox()
browser.get(url)
images = []

SCROLL_PAUSE_TIME = 2.0

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

# Need to make sure I'm still logged in in order to keep scrolling
while True:

    get_image_links(browser.page_source, images)
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


