from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    mars_data = {}

    #NASA Mars News Scraping
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')
    time.sleep(5)

    news_title = soup.find_all(class_='content_title')[1].get_text()

    news_p = soup.find_all(class_='article_teaser_body')[0].get_text()

    #JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')

    full_image = soup.find("a", class_='button fancybox')["data-fancybox-href"]

    featured_image_url = ('https://www.jpl.nasa.gov' + full_image)


    # Mars Facts
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    html = browser.html

    soup = bs(html, 'html.parser')

    mars_table = soup.find("table", id="tablepress-p-mars")


    # Mars Hemispheres
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html = browser.html

    soup = bs(html, 'html.parser')

    results = soup.find_all("div", class_="item")
    title = []
    link = []

    hemisphere_image_urls = [
    {"title": title, "img_url": link}
]  

    for result in results:
        
        title = result.find("img", class_="thumb")["alt"]
        hemisphere_image_urls.append(title)
        link = result.a["href"]
        hemisphere_image_urls.append(link)

  
    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data
