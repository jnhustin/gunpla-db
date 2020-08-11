import json
import requests
from bs4 import BeautifulSoup

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

links = {
  'mg' :  'https://www.gundamplanet.com/gundam/master-grade.html?product_list_limit=108',
  'hg' :  'https://www.gundamplanet.com/gundam/high-grade.html?product_list_limit=108',
  'pg' :  'https://www.gundamplanet.com/gundam/perfect-grade.html',
  'rg' :  'https://www.gundamplanet.com/gundam/real-grade.html',
  'og' :  'https://www.gundamplanet.com/gundam/other-grade.html?product_list_limit=108',
  'sd' :  'https://www.gundamplanet.com/gundam/sd-gundam.html?product_list_limit=108',
}

HTML_FOLDER = 'html/gundam_planet'


def get_html_pages(links):
  for product_line, link in links.items():
    html = requests.get(link).text
    with open(f'{HTML_FOLDER}/{product_line}.html', 'w') as f:
      f.write(html)


def get_details_page_from_product_line(html):
  with open(f'{HTML_FOLDER}/{html}', 'r') as f:
    page = f.read()
    f.close()
  soup  =  BeautifulSoup(page, 'html.parser')
  ol    =  soup.find('ol', class_='products list items product-items')
  a_tag =  ol.findAll('a', class_='product photo product-item-photo')
  print(f'identified {len(a_tag) elements to write}')


  # TODO - move this to last operation after all the data has been collected
  # TODO - start with empty json_data[product_line]
  with open(f'{HTML_FOLDER}/json_data.py', 'r') as f:
    json_data = json.load(f)

  for tag in a_tag:
    href       =  tag['href']
    image_link =  tag.find('img', class_='photo image')['src']

    page  =  requests.get(href).text
    model =  href.split('https://www.gundamplanet.com/')[1]

    print('href:', href)
    print('model: ', model)
    with open(f'{HTML_FOLDER}/rg/{model}', 'w') as f:
      f.write(page)

    # TODO - change this to json_data[product_line][model]
    json_data[model] = {
      'href'   :  href,
      'images' :  [image_link]
    }

  with open(f'{HTML_FOLDER}/json_data.py', 'w') as f:
    f.write(json.dumps(json_data, indent=2))

if __name__ == '__main__':
  get_details_page_from_product_line('rg.html')
  # get_html_pages(links)

