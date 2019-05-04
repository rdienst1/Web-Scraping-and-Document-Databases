import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': '/user/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

#Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
#Hold variables in library list
def scrape():
    browser = init_browser()
    listings = {}
    #NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html,"lxml")
    
    listings["news_title"] = soup.find_all('div', class_='content_title')[0].text.strip()
    listings["news_p"] = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()

    #JPL Mars Space Images - Featured Image
    url_JPLimages = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_JPLimages)
    html = browser.html
    soup1 = bs(html, "lxml")
    p_path_featuresimage = soup1.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    browser.visit(featured_image_url)
    listings["featured_image_url"] = "https://www.jpl.nasa.gov" + p_path_featuresimage
    #Mars Weather
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)
    html = browser.html
    soup2 = bs(html, "lxml")
    listings["mars_weather"] = soup2.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.strip()
    #Mars Facts
    url_marsfacts = "http://space-facts.com/mars/"
    table_Scrape = pd.read_html(url_marsfacts)
    df_table = table_Scrape[0]
    df_table.set_index('description', inplace=True)
    listings["mars_facts"] = df_table.to_html('table.html')
    #Mars Hemispheres
    url_USGS = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_USGS)
    html = browser.html
    soup_soup = bs(html, "lxml")

    results = soup_soup.find_all('h3')

    img_urls = []
    dict = {}

    for result in results:
        x = result.text
        browser.click_link_by_partial_text(x) #click link text matching h3 name
        y = soupy.find_all('div', class_="downloads")[0].find_all('a')[0].get("href") #grab all link sources
        dict["title"] = x #name keys
        dict["img_url"] = y
        img_urls.append(dict) #add dict of each img to list
        dict = {} #I'm seeing last img repeated as all entry without this
        browser.click_link_by_partial_text('Back')
    
    listings["hemisphere_urls"] = img_urls

    return listings
