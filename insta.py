# Import libraries
import requests
import time
from bs4 import BeautifulSoup
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

#print(soup)

# Image URL is in text/javascrpt
quote = soup.findAll('script', {"type": "text/javascript"})
#print(quote)

#print(type(quote))
b = re.findall(r'["](.*?)["]',str(quote))
#print(b)

#find the twtter description as the quote lies in that reference
for i in b:
    try:
        if(".jpg" in i):
            url = i.replace("\\u0026","&")
            count = 1

            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--start-maximized')
            driver = webdriver.Chrome(chrome_options=chrome_options)

            time.sleep(2)

            #the element with longest height on page
            ele=driver.find_element("xpath", '//div[@class="react-grid-layout layout"]')
            total_height = ele.size["height"]+1000

            driver.set_window_size(1920, total_height)      #the trick
            time.sleep(2)

            #driver.set_window_size(1024, 768) # set the window size that you need
            driver.get(url)
            driver.save_screenshot(insta_photos+count+'.jpg')
            driver.quit()


            count=count+1
            print(url)

    except:
        print("error")
