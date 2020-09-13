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
      'box_art': '',
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
  'gundam_planet_og' :  'https://www.gundamplanet.com/gundam/other-grade.html?product_list_limit=108',
  'gundam_planet_sd' :  'https://www.gundamplanet.com/gundam/sd-gundam.html?product_list_limit=108',
}



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
