#--------import requests--------#
from turtle import title
import requests
import re 
from selenium  import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import nltk
import heapq
import csv
import json
import pandas as pd

#--------GLOBAL VARIABLE--------#
global nx_choice
nx_choice = 'Y' or 'y'

#------Mention THE OUTPUT CSV FILE--------#

#summaries_file = open('summaries.csv', mode='a', encoding='utf-8')

#------Mention URL FOR SCRAPING--------#

URL=input("ENTER URL:")
#------Mention URL and CHROME DRIVER--------#

CHROMEDRIVER_PATH ='C:\Windows\chromedriver.exe'
s=Service('C:\Windows\chromedriver')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
#------Selenium using chrome driver to get html code /java code -------#

driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'lxml')

#------Saving outputto page.txt--------#

file =open('page.txt', mode='w' ,encoding ='utf-8')
file.write(soup.prettify())

################################################################
#############   FUNCTIONS #####################################
###############################################################

def extract_title(soup):
    title=soup.find('title')
    print('title element:',title)
    df=pd.DataFrame(title)
    #df.to_csv('data.csv')
    df.to_csv('data.csv', mode='a', index=False, header=False)

def extract_images(soup):
    images_dict={'ALT':[],'SRC':[]}
    images = soup.find_all('img')
    for image in images:
        imageAlt = image.get('alt')
        imageSrc = image.get('src')
        print("ALT: ", imageAlt, "SRC: ", imageSrc)
        images_dict['ALT'].append(imageAlt)
        images_dict['SRC'].append(imageSrc)   
    df=pd.DataFrame(images_dict)
    #df.to_csv('data.csv')
    df.to_csv('data.csv', mode='a', index=False, header=False)

def extract_links(soup):
    linking=[]
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
      print(link.get('href'))
      linking.append(link.get('href'))  
    df=pd.DataFrame(linking)
    #df.to_csv('data.csv')
    df.to_csv('data.csv', mode='a', index=False, header=False)

def main():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'lxml')
    global nx_choice
    while nx_choice == 'Y' or nx_choice == 'y':
        print("\n WELCOME TO WEB SCRAPER \n"
        "\n 1.TITLE ""\n 2.IMAGES""\n 3.Extract_links")
        choice=int(input("\n What Do You Want To Extract"))
        match choice:
            case 1:extract_title(soup)
            case 2:extract_images(soup)
            case 3:extract_links(soup)
        nx_choice
        nx_choice=input("\n Do You Want To Continue Y/N  :")
        if nx_choice =='N' or nx_choice == 'n':
            print("\n\n\n HAPPY WEB SCRAPPING RESULTS SAVED")
            break
############# MAIN  CODE #######################################
main()
