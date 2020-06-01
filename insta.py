# Import libraries
import requests
import time
from bs4 import BeautifulSoup
import re
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request


def get_image_links(html_page,image_list):
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(html_page, "html.parser")

    # Image URL is in text/javascrpt
    image_src = soup.findAll('script', {"type": "text/javascript"})

    b = re.findall(r'["](.*?)["]',str(image_src))

    for i in b:
        try:
            if(".jpg" in i):
                url = i.replace("\\u0026","&")
                #print(url)
                if(url in image_list):
                    continue
                else:
                    # Add image url to list 
                    image_list.append(url)
		    # Write contents of url to image
                    urllib.request.urlretrieve(url, "photos/"+str(len(image_list))+".jpg")
            else:
                continue
        except:
            print("error")
    return(image_list)


def login():
    # Get current directory
    path = os.getcwd()


    # Create directory for photos
    insta_photos = path+"/photos/"

    try:
        os.mkdir(insta_photos)
    except OSError:
        print ("Creation of the directory %s failed" % insta_photos)
    else:
        print ("Successfully created the directory %s " % insta_photos)


    # Set the URL you want to webscrape from
    url = 'https://www.instagram.com/lifeatdeloitteireland/?hl=en'

    # Create firefox webdriver
    browser = webdriver.Firefox()

    # Open web browser for given url
    browser.get(url)


    browser.implicitly_wait(5)
    try:
        browser.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        browser.implicitly_wait(5)
        browser.find_element_by_xpath("//button[contains(.,'Log in with Facebook')]").click()
    except:
        browser.find_element_by_xpath("//button[contains(.,'Log in with Facebook')]").click()

    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//input[@name='email']").send_keys('email')
    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//input[@name='pass']").send_keys('password') 
    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    browser.implicitly_wait(5)

    # Create empty list to store image urls
    images = []

    # Set pause time in order for page to load
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


login()
