import os
import time
import json
import requests
from bs4 import BeautifulSoup, element


PAGE_LINKS = {
  'og' :  'https://www.gundamplanet.com/gundam/other-grade.html?product_list_limit=108',
  'mg' :  'https://www.gundamplanet.com/gundam/master-grade.html?product_list_limit=108',
  'pg' :  'https://www.gundamplanet.com/gundam/perfect-grade.html',
  'hg' :  'https://www.gundamplanet.com/gundam/high-grade.html?product_list_limit=108',
  'rg' :  'https://www.gundamplanet.com/gundam/real-grade.html',
  'sd' :  'https://www.gundamplanet.com/gundam/sd-gundam.html?product_list_limit=108',
}

SITE_HTML_FOLDER =  'html/gundam_planet'
OUTPUT_FILE      =  'output/gundam_planet.json'


def main():
  """
    download the html

    download all product_listings pages
      and initialize product entry for product in json

    loop through downloaded product listing pages
      extract data
      append data to product_listing key
  """

  storage_dir = 'base_pages'
  download_html_pages(PAGE_LINKS, storage_dir)

  dirs = os.listdir(f'{SITE_HTML_FOLDER}/{storage_dir}')
  for page in dirs:
    get_details_page_from_product_line(storage_dir, page)

  for product_line in PAGE_LINKS.keys():
    dirs = os.listdir(f'{SITE_HTML_FOLDER}/{product_line}')
    for page in dirs:
      if len(page):
        process_details_page(product_line, page)

  return


def download_html_pages(links, location):
  # downloads the main html page where the contents will be stored
  for product_line, link in links.items():
    file_location = f'{SITE_HTML_FOLDER}/{location}/{product_line}.html'
    if os.path.exists(file_location):
      continue

    html = requests.get(link).text
    with open(f'{file_location}', 'w') as f:
      f.write(html)
  return


def get_details_page_from_product_line(directory, html):
  product_line  =  html.split('.')[0]
  if os.path.exists(f'{SITE_HTML_FOLDER}/{product_line}'):
    return
  else:
    os.mkdir(f'{SITE_HTML_FOLDER}/{product_line}')

  file_location =  f'{SITE_HTML_FOLDER}/{directory}/{html}'
  with open(f'{file_location}', 'r') as f:
    page = f.read()
    f.close()

  soup  =  BeautifulSoup(page, 'html.parser')
  a_tag =  soup.findAll('a', class_='product photo product-item-photo')
  print(f'identified {len(a_tag)} elements to write')

  json_data = {}
  for tag in a_tag:
    href       =  tag['href']
    image_link =  tag.find('img', class_='photo image')['src']
    print(f'working on page: {href.split("https://www.gundamplanet.com/")[1]}')

    # TODO - check if the page already exists
    page       =  requests.get(href).text
    model_name =  href.split('https://www.gundamplanet.com/')[1]

    with open(f'{SITE_HTML_FOLDER}/{product_line}/{model_name}', 'w') as f:
      f.write(page)
      f.close()

    json_data[model_name] = {
      'href'   :  href,
      'images' :  [image_link]
    }

  with open(OUTPUT_FILE, 'r+') as f:
    file_data = json.load(f)
    file_data[product_line] = json_data
    f.seek(0)
    f.write(json.dumps(file_data, indent=2))
    f.close()

  return


def process_details_page(product_line, page):
  with open(f'{SITE_HTML_FOLDER}/{product_line}/{page}', 'r') as html:
    soup =  BeautifulSoup(html, 'html.parser')

  # find data
  product_spec : list =  get_product_specifications(soup)
  images       : list =  get_product_images(soup)
  misc_info    : list =  get_misc_info(soup)

  # package data
  json_data = {
    'product_spec' :  product_spec,
    'images'       :  images,
    'misc_info'    :  misc_info,
  }

  # write data
  with open(OUTPUT_FILE, 'r+') as f:
    file_data = json.load(f)
    if file_data.get(product_line) == None:
      file_data[product_line] = {}

    file_data[product_line][page] = {**file_data[product_line][page], **json_data}
    f.seek(0)
    f.write(json.dumps(file_data, indent=2))
    f.close()
  return

def get_misc_info(soup):
  try:
    section =  soup.find('div', class_='product attibute description').find('div', class_='value').contents
    return [str(row) for row in section if type(row) == element.Tag]
  except:
    title = soup.find('title')
    print(f'{title} failed misc info extract')
    return []


def get_product_images(soup):
  images   =  []
  main_img =  soup.find('img', id='gallerymainimg')['src']
  images.append(main_img)

  gallery_section = soup.find('ul', class_='gallery-thumbsection').findAll('a')
  for image in gallery_section:
    images.append(image['href'])

  return images


def get_product_specifications(soup):
  # results = ['Brand', 'BANDAI', 'Grade/Scale', 'RG', 'Series', 'Neon Genesis Evangelion', 'Condition', 'This product needs to be assembled.']
  product_spec = soup.find('div', class_='prod_spec_wrap')

  vals =  []
  for p in product_spec:
    for tag in p:
      if type(tag) == element.Tag:
        vals.append(tag.text)

  return vals




def cleanup():
  with open(OUTPUT_FILE, 'r') as f:
    json_data = json.load(f)

  for val in json_data.keys():
    print('val: ',val)

if __name__ == '__main__':
  start_time = time.time()
  # main()
  cleanup()
  seconds  =  time.time() - start_time
  print('Time Taken:', time.strftime("%H:%M:%S",time.gmtime(seconds)))

