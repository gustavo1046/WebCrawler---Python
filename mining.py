
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep
from selenium import webdriver

url = 'https://www.usquidditch.org/teams'


#open selenium - use your own info for PATH
PATH = (r"C:\\Users\\Gustavo\\Desktop\\scoutfy\\Team USA\\chromedriver.exe")

driver = webdriver.Chrome(PATH)
driver.get(url)
driver.implicitly_wait(3)


#wait for page loading
sleep(2)
#html got with selenium
selenium_get = driver.page_source

soup = bs(selenium_get, 'html.parser')

link=[]

#close selenium
driver.close() 

for a in soup.findAll('a'):
    link.append(a['href'])

#get every team website
link=link[115:346]
#get every team's info from the main page
info = soup.find('tbody').findAll('tr')

def find_acronym(s):
    #return only letters between ()
    return s[s.find("(")+1:s.find(")")]

def find_class(soup):
    list =[]
    for el in range(230):
        element = (soup.find("table", attrs = {"class" : "teams-display"}))
        list.append(element.find("tr", attrs ={"id" : "t"+str(el)}).find_all("td")[2].get_text())
# find_class(soup)

def find_socialmedia(soup):
    refs = []
    listsocial = []
    acuts = (soup.find_all("a"))
    for el in acuts:
        refs.append(el.get("href"))
    listsocial.append(refs)
    return listsocial
# find_socialmedia(soup)


def main():
    # this list will store every dictionary of each club
    my_list = []

    for i in range(len(info)):
       # This dict will store the information of each club
        my_dict = {}
        
        my_dict['Name'] = info[i].findAll('td')[0].text
        my_dict['City'] = info[i].findAll('td')[1].text.split(',')[0].strip()
        my_dict['State'] = info[i].findAll('td')[1].text.split(',')[1].strip()

        #here it's oppened every team's new page with another info
        
        url = 'https://www.usquidditch.org' + str(link[i])
        
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        req = requests.get(url, headers=agent)
        soup = bs(req.content, features="lxml") 
           
        my_dict['Acronym'] = find_acronym(soup.find('h2').text)
        my_dict['social_media'] = find_socialmedia(soup.find("ul", attrs ={"class" : "team-social-media-links"}))

        #this are all the constants that must be added
        my_dict['Category'] = 'Non Recognized'
        my_dict['Sport'] = 'Quidditch'
        my_dict['Country'] = 'United States of America'
        my_dict['Affilated'] = 'US Quidditch'
        my_dict['Recorded By'] = 'Gustavo Florindo Oliveira'
        my_dict['Recorded Date'] = '27/02/2022'

        my_list.append(my_dict)

    return my_list

res = main()

df = pd.DataFrame(data=res)
df.to_excel('US_Quidditch.xlsx', index=False)