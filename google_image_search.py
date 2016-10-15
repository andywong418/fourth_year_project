from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_html(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

query = "car"
query = query.split()
query = '+'.join(query)
google_image_url = "https://www.google.com/search?q=" + query +  "&source=lnms&tbm=isch"
print google_image_url
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
DIR = "google_images"
html_page = get_html(google_image_url, header)
image_array = []
for link in html_page.find_all("div", {"class": "rg_meta"}):
    image_link = json.loads(link.text)["ou"]
    image_type = json.loads(link.text)['ity']
    print image_link
    image_array.append((image_link,image_type))
if not os.path.exists(DIR):
    os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])
if not os.path.exists(DIR):
    os.mkdir(DIR)
print len(image_array)
print "DIR"
print DIR
for index,img in enumerate(image_array):

    try:
        req = urllib2.Request(img[0],headers={'User-Agent': header})
        raw_img = urllib2.urlopen(req).read()
        counter = len([i for i in os.listdir(DIR)]) + 1
        print counter
        print img[1]
        f = open(os.path.join(DIR, "image" + "_" + str(counter) + '.' + img[1]), 'wb')
        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e

    # try:
    #     req = urllib2.Request(img, headers={'User-Agent' : header})
    #     raw_img = urllib2.urlopen(req).read()
    #
    #     cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
    #     print cntr
    #     if len(Type)==0:
    #         f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
    #     else :
    #         f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')
    #
    #
    #     f.write(raw_img)
    #     f.close()
    # except Exception as e:
    #     print "could not load : "+img
    #     print e
