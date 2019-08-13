# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time

def init_browser():
# Chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():    
    browser=init_browser()
    mars_info = {}

    # Nasa Mars News-------------------------------------------------------------------
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # response = requests.get(url)
    browser.visit(news_url)
    news_html = browser.html
    

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(news_html, 'html.parser')
    print(soup.prettify())

    # News title
    news_title = soup.find(class_='content_title').text
    news_title.strip()

    # News Paragraph
    news_p = soup.find(class_='article_teaser_body')
    news_p

    mars_info['news_title'] = news_title
    mars_info['news_paragraph']= news_p

    time.sleep(2)
    # JPL Mars Space Images - Featured Image------------------------------------------
    mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # mars_response = requests.get(mars_img_url)
    browser.visit(mars_img_url)
    mars_img_html = browser.html

    # Create soup object
    img_soup = BeautifulSoup(mars_img_html, 'html.parser')
    print(soup.prettify())

    # Find & print img url
    featured_img=img_soup.find('a', class_='button fancybox')

    # full_featured_img_url = (f"https://www.jpl.nasa.gov{featured_img['data-fancybox-href']}")
    full_featured_img_url = 'https://www.jpl.nasa.gov' + featured_img

    mars_info['image_url']= full_featured_img_url

    time.sleep(2)
    # Mars Weather -----------------------------------------------------------------------
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    # tweet_response = requests.get(tweet_url)
    browser.visit(tweet_url)
    tweet_html = browser.html

    #twitter soup
    tweet_soup = BeautifulSoup(tweet_html, 'html.parser')
    print(soup.prettify())

    #Tweet find and print text
    weather_tweet = tweet_soup.find('p',class_='TweetTextSize').text
    weather_tweet

    mars_info['weather'] = weather_tweet

    time.sleep(2)
    # Mars Facts-------------------------------------------------------
    fact_url='https://space-facts.com/mars/'
    # fact_response = requests.get(fact_url)
    browser.visit(fact_url)
    fact_html = browser.html

    # Facts soup (yum)
    fact_soup = BeautifulSoup(fact_html, 'html.parser')
    print(soup.prettify())

    # scrapy table
    table_rows= fact_soup.find_all('tr')

    facts = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        facts.append(row)
    fact_df = pd.DataFrame(facts, columns=["Description", "Value","C"])
    fact_df.drop(["C"], axis=1)

    mars_info['facts'] = fact_df

    time.sleep(2)
    #Hemispheres----------------------------------------------------------
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    # hemi_response = requests.get(hemi_url)
    hemi_html = browser.html

    #hemisphere soup
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    print(soup.prettify())

    # Getting these names
    hemisphere_names = []
    names= hemi_soup.find_all('h3')

    for name in names:
        hemisphere_names.append(name.text)
        
    hemisphere_names

    mars_info['hemispheres'] = hemisphere_names

    # Getting the image urls(This is broken, I spent 4 hours on it and I just can't quite get it)
    # img_urls = []

    # for hemisphere in hemisphere_names:
    #     hemi_dict = {}
    #     time.sleep(3)
    #     browser.click_link_by_partial_href('_enhanced')
    #     hemi_dict['img_urls']= browser.find_by_text('Sample')['href']
    #     hemi_dict['title']= name
    #     img_urls.append(hemi_dict)
    #     pprint(hemi_dict)
    #     browser.click_by_test('Back')

    # mars_info['images'] = img_urls

    browser.quit()

    return mars_info