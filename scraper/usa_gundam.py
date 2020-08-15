import os
import time
from bs4 import BeautifulSoup, element

from helper import Helper

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


HELPER = Helper()

def main():

  for product_line, page_link in BASE_PAGE_LINKS.items():
    # download base pages
    download_dir =  f'{SITE_HTML_FOLDER}/base_pages'
    HELPER.download_dynamic_html(page_link, download_dir, alt_filename=product_line)

    # get all kits in each base page
    get_model_details_page(product_line)




def get_model_details_page(product_line):
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
    model     =  page_link.split('https://www.usagundamstore.com/collections/model-kits/products/')[1]
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
