from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

#####################################
# Main function to scrape Mars data
#####################################
def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Get latest news
    latest_news = get_latest_news(browser)

    #Add latest news to mars_data dict
    mars_data = {}
    mars_data["news_title"] = latest_news[0]
    mars_data["news_content"] = latest_news[1]

    #Get featured image and add it to mars_data dict
    featured_image = get_featured_img(browser)
    mars_data[featured_image[0]] = featured_image[1]

    #Get mars facts and add it to mars_data dict
    mars_facts = get_mars_facts(browser)
    mars_data[mars_facts[0]] = mars_facts[1]

    #Get mars facts and add it to mars_data dict
    hemisphere_images = get_mars_hemisphere_images(browser)
    mars_data["mars_hemispheres"] = hemisphere_images

    return mars_data

####################################
# Function to get latest news on Mars
####################################
def get_latest_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    #Get the latest news title
    content_title_tag = slide_elem.find("div", class_="content_title")
    content_title = content_title_tag.text

    #Get the content description
    # Use the parent element to find the paragraph text
    news_content_tag = slide_elem.find('div', class_="article_teaser_body")
    news_content = news_content_tag.text

    latest_news = [content_title, news_content]

    return latest_news

#########################################
# Function to get the featured image
#########################################
def get_featured_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    browser.links.find_by_partial_text('FULL').click()
    img_html = browser.html

    # Parse the resulting html with soup
    img_soup = soup(img_html, 'html.parser')

    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image')['src']

    #construct the url for the image
    img_url = f"{url}/{img_url_rel}"

    featured_image = ["featured_image", img_url]

    return featured_image

############################################
# Function to get mars facts
############################################
def get_mars_facts(browser):
    galaxy_url = "https://galaxyfacts-mars.com/"

    tables = pd.read_html(galaxy_url)
    df = tables[0]
    df.columns = df.iloc[0]
    df = df.rename(columns={'Mars - Earth Comparison': 'Description'})

    df.set_index('Description', inplace = True)

    df_html = df.to_html()

    mars_facts = ["mars_facts", df_html]

    return mars_facts

##########################################
# Function to get mars hemisphere images
##########################################
def get_mars_hemisphere_images(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    
    html = browser.html
    astro_soup = soup(html, 'html.parser')
    divs = astro_soup.find_all('div', class_='item')
    hemisphere_images = []
    #print(links)

    #Loop through divs
    for div in divs:
        
        #Fing link to navigate
        ref_url = div.find('a')['href']
        
        #Construct the complete URL
        hem_url = url + ref_url
        
        #Navigate to constructed URL
        browser.visit(hem_url)
        hem_html = browser.html  
        hem_soup = soup(hem_html, 'html.parser')
        
        #Get title
        title  = hem_soup.find('h2', class_='title').text
        
        #Get image URL
        div = hem_soup.find('div', class_= 'downloads')
        image_url = div.find('a')['href']
        full_image_url = url + image_url

        hemisphere_dict = {}
        hemisphere_dict["img_url"] = full_image_url
        hemisphere_dict["title"] = title
        hemisphere_images.append(hemisphere_dict)
        
        #Click back button on browser
        browser.back()
        
    return hemisphere_images
