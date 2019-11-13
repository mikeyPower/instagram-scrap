# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import os
import urllib

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

#quote is in meta tag
quote = soup.findAll('script', {"type": "text/javascript"})
#print(quote)
quote_of_the_day = ""
#print(type(quote))
b = re.findall(r'["](.*?)["]',str(quote))
#print(b)

#find the twtter description as the quote lies in that reference
for i in b:
    try:
        if(".jpg" in i):
            url = i.replace("\\u0026","&")
            count = 1
           # print(url)

            img = urllib.urlopen(url)

            print(img.info().type)
            image_data = img.read()
            # Open output file in binary mode, write, and close.
            f = open(insta_photos+count+'.jpg','wb')
            f.write(image_data)
            f.close()



            count=count+1

    except:
        a = "Not everything that is faced can be changed, but nothing can be changed until it is faced.-James Baldwin"


#check if quote of the day string is empty
#if not quote_of_the_day:
#    quote_of_the_day = a

#remove quotes
newstr = quote_of_the_day.replace('"', "")

print(newstr)
#split string into quote and author
spit = newstr.rsplit('-',1)
#print(spit)
