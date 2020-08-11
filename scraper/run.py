import requests
from bs4 import BeautifulSoup

""" data structure
{
  '<site>': {
    'display_name'  :  '',
    'timeline'      :  '',
    'series'        :  '',
    'product_line'  :  '',
    'manufacturer'  :  '',
    'scale'         :  '',
    'japanese_name' :  '',
    'sku'           :  '',
    'description'   :  '',
    'release_date'  :  '',
    'images'        :  {
      'main_image' :  '',
      'box_art' '',
      gallery_images :  [ '', '', ...]
    }
  }
}

"""

# scrape sites for gunpla data
"""
  values needed
  ================
  'display_name',
  'timeline',
  'series',
  'product_line',
  'manufacturer',
  'scale',
  'japanese_name',
  'sku',
  'info',
  'info_source',
  'release_date',
"""

"""
  dirs needed
  ===============
  gunpla/
    /<site>
      html files = [mg, pg, hg, og, sd]
      mg/    -> will contain the .html files for corresponding model
      pg/
      hg/
      og/
      sd/

"""

site_urls = {
  'wiki'             :  'https://gundam.fandom.com',
  'wiki_mg'          :  'https://gundam.fandom.com/wiki/Master_Grade',
  'gundam_planet_pg' :  'https://www.gundamplanet.com/gundam/perfect-grade.html?product_list_limit=108',
  'gundam_planet_mg' :  'https://www.gundamplanet.com/gundam/master-grade.html?product_list_limit=108',
  'gundam_planet_hg' :  'https://www.gundamplanet.com/gundam/high-grade.html?product_list_limit=108',
  'gundam_planet_pg' :  'https://www.gundamplanet.com/gundam/perfect-grade.html',
  'gundam_planet_og' :  'https://www.gundamplanet.com/gundam/other-grade.html?product_list_limit=108',
  'gundam_planet_sd' :  'https://www.gundamplanet.com/gundam/sd-gundam.html?product_list_limit=108',
}

page = requests.get(site_urls['gundam_planet_mg'])
with open('mg.html', 'w') as f:
  f.write(page.text)




# soup = BeautifulSoup(page.content, 'html.parser')

# get all links + base image from hg, pg, mg list
  # go to base page
  # loop through pages
  # grab link
  # grab image
# loop through each
  # grab data set



# gundam planet
# grab the image + all links into the product
# TODO - figure out pagination
  # find ul with class = 'items pages-items
    # grab all hrefs from child.ul.li.a tags



# ol. class = 'products list items product-items'
  # child.div (class = 'products list items product-items')
    # details page = child.a.href
    # image = child.a.image.src (class = 'photo image')

# print('soup:', soup)
# table = soup.findAll('li', {'class': 'item product product-item blue_wrap'})
# # print('table:', len(tabxle))

# for model in table:
#   link_tag = model.find('a', {'class': 'product-item-link'})
#   model_name = link_tag.text
#   model_link = link_tag['href']
#   print(f'{model_name}: {model_link}')





""" gundam planet - details page
  div class = 'prod_spec_wrap'
    - 'manufacturer',
    - 'series',
    - 'product_line',

  h1 class = 'page-title' > child .span class = 'base'
    - 'display_name',


  images
    - main image: img id = 'gallerymainimg' src
    - gallery images
      - ul class = gallery-thumbsection
        - loop through children li > figure a tag href
    - box art:
      - div class = 'package_availabity' > img class = 'package_img' src
    - promotional image / info
      - not always available
      - div class = 'product attibute description' > div class = 'value' > img source



  product details
    - description

  'scale',
  'timeline',
  'japanese_name',
  'sku',
  'info',
  'info_source',
  'release_date',

"""




"""  gkgundamkit.com
  https://gkgundamkit.com/en/mg-master-grade
  https://gkgundamkit.com/en/rg-real-grade
  https://gkgundamkit.com/en/hg-high-grade
  https://gkgundamkit.com/en/pg-perfect-grade
  https://gkgundamkit.com/en/re100
  https://gkgundamkit.com/en/gunpla


  jan code
  package weight
  release date

"""


""" hobbylinkjapan
  https://www.hlj.com/gundam
  https://www.hlj.com/search/?q=*&productFilter=itemType%3APerfect-Grade%20Kits
  https://www.hlj.com/search/?q=*&productFilter=itemType%3AMaster-Grade%20Kits
  https://www.hlj.com/search/?q=*&productFilter=category%3AGundam%3B%3BitemType%3AHigh-Grade%20Kits
  https://www.hlj.com/search/?q=*&productFilter=category%3AGundam%3B%3BitemType%3AReal-Grade%20Kits
  https://www.hlj.com/search/?q=SD&productFilter=category%3AGundam%3B%3BitemType%3AHigh-Grade%20Kits

  - manufacturer
  - JAN code
  - item size/weight
  - description

"""
