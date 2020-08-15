import os
import time
import json
import requests
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



SITE_HTML_FOLDER = 'html/usa_gundam'
BASE_PAGE_LINKS = {
  # 'rg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=rg-kits',
  # 'p-bandai' :  'https://www.usagundamstore.com/pages/search-results-page?collection=p-bandai',
  # 'pg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=pg-gundam-kits',
  'mg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=model-kits',
  # 'sd'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=gundam-bb-sd',
  # 'hguc'     :  'https://www.usagundamstore.com/pages/search-results-page?collection=hguc-gundam-kits',
  # 're'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=re-100-reborn-model-kits',
}



def main():
  for product_line, page_link in BASE_PAGE_LINKS.items():
    # download base pages
    download_base_page(product_line, page_link)

    # get all kits in each base page
    get_model_details_page(product_line)

  # pass



def get_model_details_page(product_line):
  # open the page
  with open(f'{SITE_HTML_FOLDER}/base_pages/{product_line}.html') as f:
    page_html = f.read()
    f.close()

  soup          =  BeautifulSoup(page_html, 'html.parser')
  paginator_div =  soup.find('div', class_='snize-pagination')
  a_tags        =  paginator_div.findAll('a')

  num_of_pages = get_num_of_pages(a_tags)
  print(f'\n{product_line} has {num_of_pages} of pages')

  # create the folder f'{SITE_HTML_FOLDER}/{product_line} if it doesn't exist

  # get this page's content
  json_data = extract_table_contents(soup)

  # get any subsequent page contents
  num_of_pages > 0:
    # iterate range up to num_of_ages
    # visit page:   https://www.usagundamstore.com/pages/search-results-page?collection=model-kits&page={page_number}
    # download the html to f'{SITE_HTML_FOLDER}/base_pages/{product_line}
    # source soup the page from downloaded file
    # send to extract_table_contents
    # add sleep 1 second
    pass
    #
    json_data.update(extract_table_contents(soup))

  json_data = json.dumps(json_data, indent=2)
  print(json_data)
  pass


def extract_table_contents(soup):

  # loops through a tables worth of content and extracts model info of all models in the table
  # returns a dict of the models on the page

  product_info =  {}

  a_tags =  soup.findAll('a', class_ = 'snize-view-link')
  for tag in a_tags:
    page_link =  tag['href']
    model     =  page_link.split('https://www.usagundamstore.com/collections/model-kits/products/')[1]
    image     =  tag.find('img', class_ = 'snize-item-image')['src']

    product_info[model] = {
      'href'   :  page_link,
      'images' :  [image],
    }
    print('finished processing: ', model)

  return product_info


def download_base_page(product_line, page_link):
  download_location = f'{SITE_HTML_FOLDER}/base_pages/{product_line}.html'
  if os.path.exists(download_location):
    print('page link already downloaded, skipping: ', page_link)
    return

  print('downloading base_page:', page_link)
  try:
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(page_link)
    page_html = driver.page_source
  finally:
    driver.quit()

  # page_html = requests.get(page_link).text
  with open(download_location, 'w') as f:
    f.write(page_html)

  return




def get_num_of_pages(a_tags):
  num = 0
  for tag in a_tags:
    if len(tag.contents):
      int_val = safe_cast(tag.contents[0], int)
      if isinstance(int_val, int):
        num = int_val if num < int_val else num
  return num


def safe_cast(val, to_type):
  try:
    return to_type(val)
  except:
    return val




if __name__ == '__main__':
  main()
