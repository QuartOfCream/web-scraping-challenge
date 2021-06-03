from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    MarsDict = {}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    response = requests.get(news_url)
    soup = bs(response.text, 'html.parser')

    news_html = browser.html
    news_soup = bs(news_html,'lxml')

    find_title = news_soup.find("div",class_="content_title").text
    find_paragraph = news_soup.find("div", class_="rollover_description_inner").text

    MarsDict['find_title'] = find_title.get_text()
    MarsDict['find_paragraph'] = find_paragraph.get_text()


    img_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(img_url)
    html = browser.html
    soup = bs(html,'html.parser')

    soup.find('img', class_='headerimage fade-in')['src']

    image = soup.find('img', class_='headerimage fade-in')

    base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"

    final_img = base_url + image['src']

    MarsDict['final_img'] = final_img

    facts_url = "https://space-facts.com/mars/"


    info = pd.read_html(facts_url)[0]
    info.reset_index(inplace=True)
    info.columns=["ID", "Properties", "Mars", "Earth"]

    info.to_html('MarsFacts.html')

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    items = soup.find_all('div', class_='item')

    final_urls = []

    usgs_url = 'https://astrogeology.usgs.gov'

    for item in items:
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(usgs_url + image_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        image_url = usgs_url + soup.find('img', class_='wide-image')['src']
        final_urls.append({'Title': title, "Image_URL": image_url})

    MarsDict['final_urls'] = final_urls

    browser.quit()

    return MarsDict