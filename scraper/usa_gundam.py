import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup, element

from helper import Helper

SITE = 'usa_gundam'
SITE_HTML_FOLDER = f'html/{SITE}'
BASE_PAGE_LINKS = {
  'rg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=rg-kits',
  'p-bandai' :  'https://www.usagundamstore.com/pages/search-results-page?collection=p-bandai',
  'pg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=pg-gundam-kits',
  'mg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=model-kits',
  # 'sd'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=gundam-bb-sd',
  # 'hguc'     :  'https://www.usagundamstore.com/pages/search-results-page?collection=hguc-gundam-kits',
  # 're'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=re-100-reborn-model-kits',
}
HELPER = Helper()

def main():

  # for product_line, page_link in BASE_PAGE_LINKS.items():
  #   print('product_line: ', product_line)
  #   # download base pages
  #   output_json_location =  f'output/{SITE}-{product_line}.json'
  #   download_dir         =  f'{SITE_HTML_FOLDER}/base_pages/{product_line}'
  #   download_location    =  f'{download_dir}/{product_line}.html'
  #   HELPER.download_dynamic_html(page_link, download_dir, alt_filename=product_line)

  #   # get all kits in each base page
  #   get_model_details_page(product_line, download_dir, download_location, output_json_location)
  #   print('completed extracting base page data!\n\n\n')


  # open json and update models in json data
  for product_line in BASE_PAGE_LINKS.keys():
    print(f'\n\n============== {product_line} ==============')

    output_json_location =  f'output/{SITE}-{product_line}.json'
    with open(output_json_location, 'r') as f:
      json_data = json.load(f)
      f.close()

    for model_kit, file_model_info in json_data.items():
      print(f'{counter}/{num_of_kits_to_process} - {model_kit}')

      cleaned_model_info   =  clean_model_kit_json(product_line, file_model_info)
      json_data[model_kit] =  cleaned_model_info
      output_json_location =  f'output/{SITE}-cleaned.json'
      HELPER.update_json_file_content(cleaned_model_info, model_kit, output_json_location)

      counter += 1
      # return # TODO

  return


def process_details_page(file_model_info):
  try:
    page_url =  file_model_info['href']
    driver   =  webdriver.Firefox()
    driver.implicitly_wait(20)
    driver.get(page_url)
    page_html =  driver.page_source
    soup      =  BeautifulSoup(page_html, 'html.parser')

    html_model_info =  {}

    # title
    html_model_info['title'] = soup.find('h1', class_='product-single__title').contents

    # sku
    sku = soup.find('p', class_='product-single__sku').contents
    html_model_info['sku'] = sku[1] if len(sku) > 1 else None

    # category
    category_tags = soup.find('p', class_='product-single__cat')
    html_model_info['categories'] = [el.contents for el in category_tags if type(el) == element.Tag and el != None and len(el)]

    # description
    product_description =  []

    product_description_1_tag     =  soup.findAll('div', class_='productdescription')
    product_description_1_content =  [tags.text for tags in product_description_1_tag]
    if len(product_description_1_content):
      product_description.append(product_description_1_content)

    product_description_2_tag     =  soup.findAll('div', class_='product attibute description')
    product_description_2_content =  [tags.text for tags in product_description_2_tag if len(tags)]
    if len(product_description_2_content):
      product_description.append(product_description_2_content)

    product_description_3_tag     =  soup.findAll('div', id='proTabs1')
    product_description_3_content =  [tags.text for tags in product_description_3_tag if len(tags)]
    if len(product_description_3_content):
      product_description.append(product_description_3_content)

    for el in product_description_3_tag:
      description_images = el.find('img')
      if description_images:
        product_description.append([description_images['src']])

    html_model_info['product_description'] = product_description

    # images
    main_img    =  soup.find('img', id='ProductPhotoImg')['src']
    img_gallery =  soup.find('div', class_='owl-stage-outer')

    if img_gallery != None:
      a_tags = img_gallery.findAll('a', class_='product-single__thumbnail')
      images = file_model_info['images']
      images.append(main_img)
      for tag in a_tags:
        images.append(tag['data-zoom-image'])

    # mark that the model has been updated
    html_model_info['is_visited'] = True
  finally:
    driver.quit()

  return html_model_info


def clean_model_kit_json(product_line, file_model_info):
  # print(model_kit)
  # categories section
  file_model_info['categories'] =[ item[0].lower() for item in file_model_info['categories'] if not item[0].lower().startswith('categories')]

  # TODO - add a scale field

  file_model_info['product_line'] = product_line

  # image section

  return file_model_info


def get_model_details_page(product_line, download_dir, download_location, output_json_location):
  print('\n ================')
  print('processing page: ', product_line)

  # open the page
  with open(download_location, 'r') as f:
    page_html = f.read()
    f.close()

  soup          =  BeautifulSoup(page_html, 'html.parser')
  paginator_div =  soup.find('div', class_='snize-pagination')
  a_tags        =  paginator_div.findAll('a')

  num_of_pages = get_num_of_pages(a_tags)
  print(f'\n{product_line} has {num_of_pages} of pages.')

  # content already in file, used as a base to append new content unto
  with open(output_json_location, 'r') as f:
    file_json = json.load(f)
    f.close()

  # get initial page's content
  print(f'processing page : {product_line}.html')
  html_json = extract_table_contents(soup, file_json)

  # get any subsequent page contents
  if num_of_pages > 0:

    # iterate range up to num_of_ages
    for page_num in range(2, num_of_pages + 1):
      page_link         =  f'{BASE_PAGE_LINKS[product_line]}&page={page_num}'
      filename          =  f'{product_line}-{page_num}'
      download_location =  f'{download_dir}/{filename}'

      # download page
      HELPER.download_dynamic_html(page_link, download_dir, alt_filename=filename)
      with open(f'{download_location}.html', 'r') as f:
        html = f.read()
        f.close()

      # extract page content
      soup        =  BeautifulSoup(html, 'html.parser')
      models_info =  extract_table_contents(soup, file_json)
      html_json.update(models_info)

  # write data to file
  for model, model_info in html_json.items():
    HELPER.update_json_file_content(model_info, model, output_json_location)

  # update model key on json
  print(f'finished extracting base pages, {output_json_location} updated')
  return


def extract_table_contents(soup, file_json):
  # loops through a tables worth of content and extracts model info of all models in the table
  # returns a dict of the models on the page

  a_tags =  soup.findAll('a', class_ = 'snize-view-link')
  for tag in a_tags:
    page_link =  tag['href']
    model     =  page_link.split('/products/')[1]
    image     =  tag.find('img', class_ = 'snize-item-image')['src']

    # first time content, just assign a new dict
    if file_json.get(model) == None:
      file_json[model] = {
        'href'   :  page_link,
        'images' :  [image],
      }
    # else carefully append to existing content
    else:
      if image not in file_json[model].get('images'):
        file_json[model]['images'].append(image)

    print(f'  {model} processed')

  return file_json


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
