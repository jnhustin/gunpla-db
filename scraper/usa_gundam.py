import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup, element

from helper import Helper

SITE_HTML_FOLDER = 'html/usa_gundam'
BASE_PAGE_LINKS = {
  'rg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=rg-kits',
  'p-bandai' :  'https://www.usagundamstore.com/pages/search-results-page?collection=p-bandai',
  'pg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=pg-gundam-kits',
  'mg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=model-kits',
  'sd'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=gundam-bb-sd',
  'hguc'     :  'https://www.usagundamstore.com/pages/search-results-page?collection=hguc-gundam-kits',
  're'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=re-100-reborn-model-kits',
}


HELPER = Helper()

def main():

  # for product_line, page_link in BASE_PAGE_LINKS.items():
  #   # download base pages
  #   download_dir =  f'{SITE_HTML_FOLDER}/base_pages'
  #   HELPER.download_dynamic_html(page_link, download_dir, alt_filename=product_line)

  #   # get all kits in each base page
  #   get_model_details_page(product_line)

  with open('output/usa_gundam.json', 'r') as f:
    json_data = json.load(f)
    f.close()
  # open json
  # loop through top level keys (product_line)
    # for each kit in the product_line:
  for product_line in json_data:
    print('product_line:' , product_line)
    for model_kit, file_model_info in json_data[product_line].items():
      print('model_kit:' , model_kit)
      if file_model_info.get('is_visited'):
        print('skipping, already extracted')
        continue
      # TODO - figure out a way to mark if a kit detailed page has already been visited
        # key on the model_kit dict that marks that it has been visited
      try:
        page_url =  file_model_info['href']
        driver   =  webdriver.Firefox()
        driver.implicitly_wait(20)
        driver.get(page_url)
        page_html =  driver.page_source
        soup      =  BeautifulSoup(page_html, 'html.parser')

        html_model_info =  {}
        # title = soup.find('h1', class_='product-single__title').contents
        html_model_info['title'] = soup.find('h1', class_='product-single__title').contents
        # sku = soup.find('p', class_='product-single__sku').contents
        html_model_info['sku'] = soup.find('p', class_='product-single__sku').contents[1]
        # print('sku: ', sku)


        category_tags = soup.find('p', class_='product-single__cat')
        # print('category_tags: ', category_tags)
        # print('\ncategory')
        html_model_info['categories'] = [el.contents for el in category_tags if type(el) == element.Tag and el != None and len(el)]
        # for el in category_tags:
        #   if type(el) == element.Tag:
        #     print('category: ', el.contents)

        # print('\ndescription')
        product_description = soup.findAll('div', class_='productdescription')


        html_model_info['product_description'] = [tags.text for tags in product_description]
        # print('product_description: ', product_description)

        # images
        # print('\nimages')
        main_img = soup.find('img', id='ProductPhotoImg')['src']
        # print('main_img: ', main_img)

        img_gallery = soup.find('div', class_='owl-stage-outer')
        # print('img_gallery:' ,img_gallery)
        a_tags = img_gallery.findAll('a', class_='product-single__thumbnail')
        images = file_model_info['images']
        images.append(main_img)
        for tag in a_tags:
          # print('tag: ', tag['data-zoom-image'])
          images.append(tag['data-zoom-image'])
        file_model_info['is_visited'] = True

      finally:
        driver.quit()
        time.sleep(1)

      json_data[product_line][model_kit] = { **file_model_info, **html_model_info }
      with open('output/usa_gundam.json', 'w') as f:
        f.write(json.dumps(json_data, indent=2))
        f.close()

  return


def process_details_page(product_line):
  pass




def get_model_details_page(product_line):
  print('\n ================')
  print('processing page: ', product_line)
  # open the page
  with open(f'{SITE_HTML_FOLDER}/base_pages/{product_line}.html') as f:
    page_html = f.read()
    f.close()

  soup          =  BeautifulSoup(page_html, 'html.parser')
  paginator_div =  soup.find('div', class_='snize-pagination')
  a_tags        =  paginator_div.findAll('a')

  num_of_pages = get_num_of_pages(a_tags)
  print(f'\n{product_line} has {num_of_pages} of pages.')

  # get initial page's content
  print(f'downloading page : {product_line}.html')
  json_data = extract_table_contents(soup)

  # get any subsequent page contents
  if num_of_pages > 0:
    # iterate range up to num_of_ages
    for page_num in range(2, num_of_pages + 1):
      page_link         =  f'https://www.usagundamstore.com/pages/search-results-page?collection=model-kits&page={page_num}'
      filename          =  f'{product_line}-{page_num}'
      download_dir      =  f'{SITE_HTML_FOLDER}/base_pages'
      download_location =  f'{download_dir}/{filename}'

      # download page
      HELPER.download_dynamic_html(page_link, download_dir, alt_filename=filename)
      with open(f'{download_location}.html', 'r') as f:
        html = f.read()
        f.close()

      soup =  BeautifulSoup(html, 'html.parser')

      # extract page content
      models_info = extract_table_contents(soup)
      json_data.update(models_info)



  output_file = 'output/usa_gundam.json'
  HELPER.update_json_file_content(json_data, product_line, output_file)
  print(f'finished extracting base pages, {output_file} updated')
  return


def extract_table_contents(soup):
  # loops through a tables worth of content and extracts model info of all models in the table
  # returns a dict of the models on the page
  product_info =  {}

  a_tags =  soup.findAll('a', class_ = 'snize-view-link')
  for tag in a_tags:
    page_link =  tag['href']
    model     =  page_link.split('/products/')[1]
    image     =  tag.find('img', class_ = 'snize-item-image')['src']

    product_info[model] = {
      'href'   :  page_link,
      'images' :  [image],
    }
    print('finished processing: ', model)

  return product_info


def get_num_of_pages(a_tags):
  num = 0
  for tag in a_tags:
    if len(tag.contents):
      int_val = HELPER.safe_cast(tag.contents[0], int)
      if isinstance(int_val, int):
        num = int_val if num < int_val else num
  return num


if __name__ == '__main__':
  HELPER.time_fn_execution(main)
