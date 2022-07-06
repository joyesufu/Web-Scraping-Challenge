# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define function to scrape the data
def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    url = "https://redplanetscience.com/"

    browser.visit(url)

    time.sleep(3)

    html = browser.html

    soup = bs(html, 'html.parser')


    news_title = soup.find_all('div', class_="content_title")[1].text
    news_paragraph = soup.find_all('div',class_='article_teaser_body')[0].text


    space_url = 'https://spaceimages-mars.com/'
    browser.visit(space_url)
    time.sleep(3)
    html = browser.html
    images_soup = bs(html, 'html.parser')


    element = images_soup.find_all('div',class_='header')

    image_string = element[0].find('img', class_='headerimage')['src']
    
    featured_image_url = f'{space_url}{image_string}'


    mars_facts_url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(mars_facts_url)
    
    mars_facts_df = table[1]
    mars_facts_df.columns=['Measurement','Value']
    
    mars_html = mars_facts_df.to_html(index=False, justify='center')
    

    mars_html.replace('\n','')


    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    time.sleep(3)
    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')

    hem_list = []

    hemisphere_results = hemisphere_soup.find('div', class_="collapsible results")

    diff_hemisphere = hemisphere_results.find_all('div', class_="item")


    for hemisphere in diff_hemisphere:
        
        title = hemisphere.find('h3').text
        
        
        hemisphere_link = hemisphere.find('a', class_="itemLink product-item")['href']
        
        browser.visit(f'{hemispheres_url}{hemisphere_link}')
        time.sleep(3)
        
        
        image_html = browser.html
        hemisphere_img_soup = bs(image_html, 'html.parser')
        
        image = hemisphere_img_soup.find('div', class_='downloads')

        
       
        img_url = image.find('li').a['href']
        
        
        img_url_full = f'{hemispheres_url}{img_url}'
        
        
        hemisphere_dict = {"title":title,
                        "img_url":img_url_full}
        
        
        hem_list.append(hemisphere_dict)

    # Store all the data into a dictionary to return
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html),
        "hemisphere_images": hem_list
    }

    return mars_dict