# Import libraries
from bs4 import BeautifulSoup
import re
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request


def get_image_links(html_page,image_list):
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(html_page, "html.parser")

    # Image URLs located within text/javascrpt
    image_src = soup.findAll('script', {"type": "text/javascript"})

    b = re.findall(r'["](.*?)["]',str(image_src))
    for i in b:
        try:
            if(".jpg" in i):
                # Replace the below character set in order to open url
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
    url = 'https://www.instagram.com/'

    # Create firefox webdriver
    browser = webdriver.Firefox()

    # Open web browser for given url
    browser.get(url)

    # Set pause time in order for page to load
    SCROLL_PAUSE_TIME = 2.0

    # Wait some time for the browser to load
    browser.implicitly_wait(SCROLL_PAUSE_TIME)

    # Since depending on which screen appears for instagram there are two variations/order that login could occur
    try:
        browser.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        browser.implicitly_wait(SCROLL_PAUSE_TIME)
        browser.find_element_by_xpath("//button[contains(.,'Log in with Facebook')]").click()
    except:
        browser.find_element_by_xpath("//button[contains(.,'Log in with Facebook')]").click()



    # Wait some time for the browser to load
    browser.implicitly_wait(SCROLL_PAUSE_TIME)
    # Search for email id and input email address
    browser.find_element_by_xpath("//input[@name='email']").send_keys('email')
    # Search for pass id and input password
    browser.find_element_by_xpath("//input[@name='pass']").send_keys('password')
    # Search for login button and click
    browser.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    # Wait some time for page to load
    browser.implicitly_wait(SCROLL_PAUSE_TIME)

    # Create empty list to store image urls
    images = []

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    print("Starting download of instagram images")

    while True:
        get_image_links(browser.page_source, images)
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait some time for page to load
        browser.implicitly_wait(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # browser.refresh()
        # Wait some time for page to load
        browser.implicitly_wait(SCROLL_PAUSE_TIME)

    print("Finished download of "+str(len(images)))

login()
