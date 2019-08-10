#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# NASA Mars News

# In[3]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# In[4]:


# Retrieve page with the requests module
response = requests.get(url)


# In[5]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())


# In[6]:


news_title = soup.find(class_='content_title').text
news_title.strip()


# In[7]:


news_p = soup.find(class_='article_teaser_body')
news_p


# JPL Mars Space Images - Featured Image

# In[8]:


mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[9]:


mars_response = requests.get(mars_img_url)


# In[10]:


img_soup = BeautifulSoup(mars_response.text, 'html.parser')
print(soup.prettify())


# In[11]:


featured_img=img_soup.find('a', class_='button fancybox')
featured_img


# In[12]:


print(f"https://www.jpl.nasa.gov{featured_img['data-fancybox-href']}")


# Mars Weather

# In[13]:


tweet_url = 'https://twitter.com/marswxreport?lang=en'


# In[14]:


tweet_response = requests.get(tweet_url)


# In[15]:


tweet_soup = BeautifulSoup(tweet_response.text, 'html.parser')
print(soup.prettify())


# In[16]:


weather_tweet = tweet_soup.find('p',class_='TweetTextSize').text
weather_tweet


# Mars Facts!

# In[17]:


fact_url='https://space-facts.com/mars/'
fact_response = requests.get(fact_url)
fact_soup = BeautifulSoup(fact_response.text, 'html.parser')
print(soup.prettify())


# In[18]:


table_rows= fact_soup.find_all('tr')


# In[19]:


facts = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    facts.append(row)
fact_df = pd.DataFrame(facts, columns=["Description", "Value","C"])
fact_df.drop(["C"], axis=1)


# Hemispheres!

# In[20]:


hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)
hemi_response = requests.get(hemi_url)
hemi_soup = BeautifulSoup(hemi_response.text, 'html.parser')
print(soup.prettify())


# In[21]:


hemisphere_names = []
names= hemi_soup.find_all('h3')

for name in names:
    hemisphere_names.append(name.text)
    
hemisphere_names


# In[22]:


img_urls = []

for hemisphere in hemisphere_names:
    hemi_dict = {}
    time.sleep(3)
    browser.click_link_by_partial_href('_enhanced')
    hemi_dict['img_urls']= browser.find_by_text('Sample')['href']
    hemi_dict['title']= name
    img_urls.append(hemi_dict)
    pprint(hemi_dict)
    browser.click_by_test('Back')


# In[ ]:




