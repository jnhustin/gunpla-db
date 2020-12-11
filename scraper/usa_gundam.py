import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup, element

from helper import Helper

OTHER_KITS       =  'other-kits'
SITE             =  'usa_gundam'
SITE_HTML_FOLDER =  f'html/{SITE}'
BASE_PAGE_LINKS = {
  'rg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=rg-kits',
  'p-bandai' :  'https://www.usagundamstore.com/pages/search-results-page?collection=p-bandai',
  'pg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=pg-gundam-kits',
  'mg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=model-kits',
  # 'sd'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=gundam-bb-sd',
  're'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=re-100-reborn-model-kits',
  # 'hguc'     :  'https://www.usagundamstore.com/pages/search-results-page?collection=hguc-gundam-kits',
  'hg'       :  'https://www.usagundamstore.com/pages/search-results-page?collection=1-144&rb_tags=Gundam',
}
HELPER = Helper()

def main():
    # TODO - NEED TO RUN PASS 1 ON sd kits
  # download_html_pages_extract_basic_info()

  # open json and update models in json data
  for product_line in BASE_PAGE_LINKS.keys():
    print(f'\n\n============== {product_line} ==============')

    # pass 1: scrape for basic info into json format
    # scrape_details_page(product_line)

    # pass 2: clean up json
    # run_pass(
    #   product_line    =  product_line,
    #   input_location  =  f'output/{SITE}/pass-1-original',
    #   output_location =  f'output/{SITE}/pass-2-reduce-details',
    #   operation       =  pass_2,
    #   operation_extra =  {'product_line': product_line},
    #   log             =  'pass 2: reduce json details'
    # )

    # pass 3: update key names
    # run_pass(
    #   product_line    =  product_line,
    #   input_location  =  f'output/{SITE}/pass-2-reduce-details',
    #   output_location =  f'output/{SITE}/pass-3-update-key-names',
    #   operation       =  pass_3,
    #   log             =  'pass 3: update key names'
    # )

    # pass 4: process by grade
    # run_pass(
    #   product_line    =  product_line,
    #   input_location  =  f'output/{SITE}/pass-3-update-key-names',
    #   output_location =  f'output/{SITE}/pass-4-process-name-by-grade',
    #   operation       =  pass_4,
    #   operation_extra =  {'product_line': product_line},
    #   log             =  'pass 4: update by product_line'
    # )

    # pass 5: manual changes
    # if os.path.exists(f'output/{SITE}/pass-5-manual-updates'):
    #   print(
    #     'yo are you sure you want to do that, this step is intended',
    #     'for you to manually update the json, running this again',
    #     'would overwrite any changes already made to those files in',
    #     'the /pass-5-manual-updates/.\nif youre sure you want to continue',
    #     'comment out this if case and uncomment the run_pass_5 code',
    #     'in the script and goodluck!'
    #   )
    #   return

    # run_pass(
    #   product_line    =  product_line,
    #   input_location  =  f'output/{SITE}/pass-4-process-name-by-grade',
    #   output_location =  f'output/{SITE}/pass-5-manual-updates',
    #   operation       =  pass_5,
    #   operation_extra =  {},
    #   log             =  'pass 5: manual updates'
    # )

    # pass 6: update tags and add series field
    run_pass(
      product_line    =  product_line,
      input_location  =  f'output/{SITE}/pass-5-manual-updates',
      output_location =  f'output/{SITE}/pass-6-update-tags-and-add-series-field',
      operation       =  pass_6,
      operation_extra =  {},
      log             =  'pass 6: update tags and add series field'
    )

    # pass 7: add title and access name
    run_pass(
      product_line    =  product_line,
      input_location  =  f'output/{SITE}/pass-6-update-tags-and-add-series-field',
      output_location =  f'output/{SITE}/pass-7-add-title-and-access-name',
      operation       =  pass_7,
      operation_extra =  {},
      log             =  'pass 7: add title and access name'
    )

    generate_sql_file(
      product_line    =  product_line,
      input_location  =  f'output/{SITE}/pass-7-add-title-and-access-name',
      output_location =  f'output/{SITE}/sql_files',
    )
  return


def download_html_pages_extract_basic_info():
  for product_line, page_link in BASE_PAGE_LINKS.items():
    print('product_line: ', product_line)
    # download base pages
    output_json_location =  f'output/{SITE}/pass-1-original/{product_line}.json'
    download_dir         =  f'{SITE_HTML_FOLDER}/base_pages/{product_line}'
    download_location    =  f'{download_dir}/{product_line}.html'
    HELPER.download_dynamic_html(page_link, download_dir, alt_filename=product_line)

    # get all kits in each base page
    get_model_details_page(product_line, download_dir, download_location, output_json_location)
    print('completed extracting base page data!')
  return


def run_pass(product_line, input_location, output_location, operation, operation_extra={}, log=''):
  print(f'running {log}')
  with open(f'{input_location}/{product_line}.json', 'r') as f:
    json_data = json.load(f)
    f.close()

  updated_json = { OTHER_KITS: {} }
  for model_kit, file_model_info in json_data.items():
    operation_extra[OTHER_KITS] = updated_json[OTHER_KITS]

    model_kit, file_model_info =  operation(model_kit, file_model_info, extra=operation_extra)
    updated_json[model_kit]    =  file_model_info

  HELPER.compose_download_dir(output_location)
  with open(f'{output_location}/{product_line}.json', 'w') as f:
    f.write(json.dumps(updated_json, indent=2))
    f.close()

  print(f'completed {log}')
  return


# PASS 1 STUFF
def scrape_details_page(product_line):
  output_json_location =  f'output/{SITE}/pass-1-original/{product_line}.json'
  with open(output_json_location, 'r') as f:
    json_data = json.load(f)
    f.close()

  num_of_kits_to_process = len(json_data.keys())
  print(f'total kits in {product_line}: {num_of_kits_to_process}')

  counter = 1
  for model_kit, file_model_info in json_data.items():
    print(f'{counter}/{num_of_kits_to_process} - {model_kit}')
    if model_kit == 'mg-1-100-full-armor-unicorn-gundam-red-color-ver-p-bandai': # broken for idk why reasons
      counter += 1
      continue
    if file_model_info.get('is_visited'):
      counter += 1
      print('  skipping, already extracted')
      continue

    # get the extra model kit info from details page
    html_model_info =  process_details_page(file_model_info)

    # update json file
    output_json_location =  f'output/{SITE}/pass-1-original/{product_line}.json'
    HELPER.update_json_file_content(html_model_info, model_kit, output_json_location)
    counter += 1
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
      html_model_info['images'] = images

    # mark that the model has been updated
    html_model_info['is_visited'] = True
  finally:
    driver.quit()

  return html_model_info


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


# PASS 2 STUFF
def pass_2(model_kit, file_model_info, extra):
  product_line = extra['product_line']

  # categories section
  # change categories -> tags
  file_model_info['tags'] =[ item[0].lower() for item in file_model_info['categories'] if not item[0].lower().startswith('categories')]
  del file_model_info['categories']

  # add a scale field
  if product_line == 'sd':
    scale = 'n/a'
  elif product_line == 'mg' or product_line == 're':
    scale = '1/100'
  elif product_line == 'hg' or product_line == 'rg' or product_line == 'hguc':
    scale = '1/144'
  else:
    scale = None
  file_model_info['scale'] = scale

  # add product line
  file_model_info['product_line'] = product_line

  # image section
  updated_imgs = []
  for img in file_model_info['images']:
    url = f'https:{img}' if img.startswith('//cdn.shopify') else img
    updated_imgs.append(url)
  file_model_info['images'] = updated_imgs

  # convert description value from list of list -> list of strings
  file_model_info['description'] = [description[0] for description in file_model_info['product_description']]
  del file_model_info['product_description']

  # add manufacturer (all will be the same)
  file_model_info['manufacturer'] = 'bandai'

  return model_kit, file_model_info


# PASS 3 STUFF
def pass_3(model_kit, file_model_info, extra):
  # rename
  """ modify the key name
    - remove "bandai-"
    - remove "-bandai"
    - change "hguc-"    to "hg-"
    - add key-name to the product-line['title']
  """
  replace_list = [
    ('pre-order-', ''),
    ('bandai-', ''),
    ('-bandai', ''),
    ('hguc-', 'hg-'),
    ('bb-', ''),
    ('cross-silhouette-', 'cs-'),
    ('-model-kit', ''),
    ('model-kit-', ''),
    ('sd-gundam-', 'sd-'),
    ('hobby-', ''),
    ('realistic-model-', ''),
    ('master-grade-', 'mg-'),
  ]
  updated_model_kit = model_kit.lower()
  for pair in replace_list:
    to_replace        =  pair[0]
    replacement       =  pair[1]
    updated_model_kit =  updated_model_kit.replace(to_replace, replacement)

  file_model_info.get('title', []).insert(0, updated_model_kit)
  return updated_model_kit, file_model_info



# PASS 4 STUFF
def pass_4(model_kit, file_model_info, extra):
  product_line =  extra['product_line']
  other_kits   =  extra[OTHER_KITS]

  # json doesnt require modification
  if product_line in []:
    return model_kit, file_model_info

  # grade specific cleaning
  if product_line == 'rg':
    fn = pass_4_rg
  elif product_line == 'pg':
    fn = pass_4_pg
  elif product_line == 're':
    fn = pass_4_re
  elif product_line == 'sd':
    fn = pass_4_sd
  elif product_line == 'hg':
    fn = pass_4_hg
  elif product_line == 'mg':
    fn = pass_4_mg
  elif product_line == 'p-bandai':
    fn = pass_4_pbandai
  else:
    raise Exception(f'this isnt accounted for: {product_line}')

  model_kit, file_model_info = fn(model_kit, file_model_info, other_kits)
  return model_kit, file_model_info


def compose_model_name(product_line, scale, model_kit):
  if model_kit == OTHER_KITS:
    return OTHER_KITS

  model_kit =  model_kit.replace(f'{scale}-', '')
  model_kit =  model_kit.replace(f'{product_line}-', '')
  return f'{product_line}-{scale}-{model_kit}'


def pass_4_rg(model_kit, file_model_info, other_kits):
  model_kit = compose_model_name('rg', '1-144', model_kit)

  # remove evangelion models
  if 'evangelion' in file_model_info.get('tags', []) or 'evangelion' in model_kit:
    other_kits[model_kit] = file_model_info
    model_kit       =  OTHER_KITS
    file_model_info =  other_kits

  return model_kit, file_model_info


def pass_4_re(model_kit, file_model_info, other_kits):
  model_kit = compose_model_name('re', '1-100', model_kit)
  model_kit = model_kit.replace('1-100-100', '1-100')
  return model_kit, file_model_info


def pass_4_pg(model_kit, file_model_info, other_kits):
  model_kit = compose_model_name('pg', '1-60', model_kit)

  # remove evangelion models
  if 'led' in model_kit or 'mazinger' in model_kit or 'star-wars' in model_kit or 'mega' in model_kit:
    other_kits[model_kit] = file_model_info
    model_kit       =  OTHER_KITS
    file_model_info =  other_kits

  return model_kit, file_model_info


def pass_4_sd(model_kit, file_model_info, other_kits):
  model_kit = model_kit.replace('-sd', '')
  model_kit =  'sd-' + model_kit.replace(f'sd-', '')

  if 'sangoku-soketsuden-' in model_kit or '-sangoku-soketsuden' in model_kit or 'sangokusoketsuden' in model_kit:
    model_kit = model_kit.replace('-sangokusoketsuden', '')
    model_kit = model_kit.replace('-sangoku-soketsuden', '')
    model_kit = model_kit.replace('sangoku-soketsuden-', '')
    file_model_info.get('tags', []).append('sangoku-soketsuden')
  if 'sangokuden-animation-' in model_kit:
    model_kit = model_kit.replace('sangokuden-animation-', '')
    file_model_info.get('tags', []).append('sangokuden')
  if 'ex-standard-' in model_kit:
    model_kit = model_kit.replace('ex-standard-', '')
    file_model_info.get('tags', []).append('ex-standard')
  if '-senshi-sangokuden' in model_kit or '-dongzhuo-forces-senshi-sangokuden' in model_kit:
    model_kit = model_kit.replace('-dongzhuo-forces-senshi-sangokuden', '')
    model_kit = model_kit.replace('-senshi-sangokuden', '')
    file_model_info.get('tags', []).append('senshi-sangokuden')

  #  remove bb designation
  split_name = model_kit.split('-')
  cleaned_name = []
  for section in split_name:
    if 'bb' in section:
      file_model_info['tags'].append(section)
    else:
      cleaned_name.append(section)


  return '-'.join(cleaned_name), file_model_info


def pass_4_pbandai(model_kit, file_model_info, other_kits):
  if 'gundam-decal' in model_kit:
    other_kits[model_kit] = file_model_info
    model_kit       =  OTHER_KITS
    file_model_info =  other_kits

  if not 'p-bandai' in file_model_info.get('tags', []):
    file_model_info.get('tags', []).append('p-bandai')

  return model_kit, file_model_info


def pass_4_mg(model_kit, file_model_info, other_kits):
  model_kit = model_kit.replace('-1-100-scale-kit', '')
  model_kit = model_kit.replace('-master-grade', '')
  model_kit = model_kit.replace('master-grade-', '')
  model_kit = compose_model_name('mg', '1-100', model_kit)

  if model_kit.startswith('hirm') or 'hi-resolution-model' in model_kit:
    model_kit  =  model_kit.replace('hirm', '')
    model_kit  =  model_kit.replace('hi-resolution-model', '')
    model_kit +=  '-hirm'
    file_model_info['tags'] = file_model_info['tags'] + ['hi-resolution-model', 'hirm']

  if 'figure-rise-jet-effect' in model_kit or 'led-' in model_kit:
    other_kits[model_kit] = file_model_info
    model_kit       =  OTHER_KITS
    file_model_info =  other_kits

  return model_kit, file_model_info


def pass_4_hg(model_kit, file_model_info, other_kits):
  replacement_list = [
    'hgbf-',
    'hgfc-',
    'hgbd-',
    'hgcc-',
    'hgbc-',
    'hgtb-',
    'hgac-',
    'hgce-',
    'hgaw-',
    'hgfc-',
  ]
  for keyword in replacement_list:
    model_kit = model_kit.replace(keyword, 'hg-')
  model_kit = compose_model_name('hg', '1-144', model_kit)

  if 'rg-' in model_kit or 'no-grade' in model_kit:
    other_kits[model_kit] = file_model_info
    model_kit       =  OTHER_KITS
    file_model_info =  other_kits

  if 'orphans-' in model_kit or "-ibo" in model_kit:
    model_kit = model_kit.replace('orphans-', '')
    model_kit = model_kit.replace('ibo-', '')
    file_model_info['tags']   =  file_model_info['tags'] + ['ibo', 'orphans', 'iron-blooded-orphans']
    file_model_info['series'] =  'ibo'
  elif 'endless-waltz-' in model_kit:
    model_kit = model_kit.replace('endless-waltz-', '')
    file_model_info['tags']   =  file_model_info['tags'] + ['ew', 'endless-waltz', 'gundam-wing']
    file_model_info['series'] =  'gundam_wing'
  elif 'gundam-age-' in model_kit:
    model_kit = model_kit.replace('gundam-age-', '')
    file_model_info['tags']   =  file_model_info['tags'] + ['gundam-age']
    file_model_info['series'] =  'gundam-age'
  elif 'build-fighters-' in model_kit or 'gundam-build-fighters-':
    model_kit = model_kit.replace('gundam-build-fighters-', '')
    model_kit = model_kit.replace('build-fighters-', '')
    file_model_info['tags'] = file_model_info['tags'] + ['build-fighters']
    file_model_info['series'] = 'build-fighters'
  elif 'build-divers-' in model_kit:
    model_kit = model_kit.replace('build-divers-', '')
    file_model_info['tags'] = file_model_info['tags'] + ['build-divers']
    file_model_info['series'] = 'build-divers'
  elif 'the-origin-' in model_kit:
    model_kit = model_kit.replace('the-origin-', '')
    model_kit = model_kit.replace('the-origin-1-144', '')
    file_model_info['tags'] = file_model_info['tags'] + ['origin', 'the-origin']
    file_model_info['series'] = 'the-origin'

  return model_kit, file_model_info


# PASS 5 STUFF
def pass_5(model_kit, file_model_info, extra):
  # TODO - [ ] - sd
  return model_kit, file_model_info

# PASS 6 STUFF
def pass_6(model_kit, file_model_info, extra):
  if model_kit == OTHER_KITS:
    return model_kit, file_model_info
  tags_to_ignore = [
    'gundam',
    'fsale',
    'best deals',
    'model',
    'model kit',
    'detail',
    'sale',
    'origins',
  ]

  series       =  None
  timeline     =  None
  updated_tags =  []
  for tag in file_model_info.get('tags', []):

    # update tags
    if tag in tags_to_ignore or tag in updated_tags or 'backorder' in tag:
      continue

    # add the tag
    tag = tag.replace('-', '_')
    tag = tag.replace(' ', '_')
    updated_tags.append(tag)

    # add meta-data to tags
    if file_model_info['scale'] not in file_model_info['tags']:
      updated_tags.append(file_model_info['scale'])

    if file_model_info['product_line'] not in file_model_info['tags']:
      updated_tags.append(file_model_info['product_line'])

    if file_model_info['product_line'] == 're':
      updated_tags.append('reborn')

    # add series
    series_data = get_series_data(tag)
    if series_data == None:
      continue

    series   =  series_data['series']
    timeline =  series_data['timeline']

    for new_tag in series_data['tags_to_add']:
      updated_tags = add_unique_to_list(updated_tags, new_tag)

  file_model_info['series']   =  series
  file_model_info['timeline'] =  timeline
  file_model_info['tags']     =  updated_tags
  return model_kit, file_model_info

def add_unique_to_list(arr:list, el:str):
  if el not in arr:
    arr.append(el)
  return arr


def get_series_data(tag):
  series_mapping = {
    'seed': {
      'series'      :  'seed',
      'timeline'    :  'cosmic_era',
      'tags_to_add' :  ['seed'],
    },
    'seed_destiny': {
      'series'      :  'seed_destiny',
      'timeline'    :  'cosmic_era',
      'tags_to_add' :  ['seed_destiny'],
    },
    'ibo': {
      'series'      :  'iron_blooded_orphans',
      'timeline'    :  'post_disaster',
      'tags_to_add' :  ['ibo', 'iron_blooded_orphans']
    },
    'unicorn': {
      'series'      :  'unicorn',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['unicorn', 'universal_century', 'uc']
    },
    'wing': {
      'series'      :  'wing',
      'timeline'    :  'after_colony',
      'tags_to_add' :  ['wing', 'after_colony', 'ac']
    },
    'endless_waltz': {
      'series'      :  'wing',
      'timeline'    :  'after_colony',
      'tags_to_add' :  ['wing', 'after_colony', 'ac', 'ew', 'endless_waltz']
    },
    'age': {
      'series'      :  'age',
      'timeline'    :  'advance_generation',
      'tags_to_add' :  ['age', 'advance_generation', 'ac']
    },
    'build_fighters': {
      'series'      :  'build_fighters',
      'timeline'    :  'build',
      'tags_to_add' :  ['build', 'build_fighters', 'bf']
    },
    'build_divers': {
      'series'      :  'build_divers',
      'timeline'    :  'build',
      'tags_to_add' :  ['build', 'build_divers','bd']
    },
    'narrative': {
      'series'      :  'narrative',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['universal_century', 'uc','narrative','nt']
    },
    'universal_century': {
      'series'      :  'universal_century',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['universal_century', 'uc']
    },
    'the_origin': {
      'series'      :  'the_origin',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['origin', 'the_origin' ,'universal_century', 'uc']
    },
    'thunderbolt': {
      'series'      :  'thunderbolt',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['thunderbolt', 'universal_century', 'uc']
    },
    '08th_ms_team': {
      'series'      :  '08th_ms_team',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['08th_ms_team', '08th', 'universal_century', 'uc']
    },
    'beginning_g': {
      'series'      :  'beginning_g',
      'timeline'    :  'build',
      'tags_to_add' :  ['bg', 'beginning_g', 'build']
    },
    'reconguista_in_g': {
      'series'      :  'reconguista_in_g',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['reconguista_in_g', 'unversal_century', 'uc', 'regild_century']
    },
    '00': {
      'series'      :  '00',
      'timeline'    :  'anno_domini',
      'tags_to_add' :  ['anno_domini', '00', 'ad', 'double_0']
    },
    'zeta': {
      'series'      :  'zeta',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['universal_century', 'z', 'zeta']
    },
    'zz': {
      'series'      :  'zeta',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['universal_century', 'z', 'zeta', 'zz']
    },
    'g': {
      'series'      :  'mobile_fighter_g',
      'timeline'    :  'future_century',
      'tags_to_add' :  ['future_century', 'fc', 'mobile_fighter_g', 'mobile_fighter_legend_g',]
    },
    'victory': {
      'series'      :  'victory',
      'timeline'    :  'universal_century',
      'tags_to_add' :  ['universal_century', 'uc', 'victory',]
    },
  }
  # print ('tag:', tag)
  series = None

  # normalize series where name could listed as multiple things
  if tag in ['iron_blooded_orphans', 'ibo']:
    series = 'ibo'
  elif tag in ['endless_waltz', 'ew']:
    series = 'endless_waltz'
  elif tag in ['universal_century', 'uc']:
    series = 'universal_century'
  elif tag in ['08th_ms_team', '08', '08th', '08th_ms']:
    series = '08th_ms_team'
  elif tag in ['gundam_00']:
    series = '00'
  elif tag in ['g_gundam']:
    series = 'g'
  else:
    series = tag

  return series_mapping.get(series)


# PASS 7 STUFF
def pass_7(model_kit, file_model_info, extra):
  model_scale = {
    '1 144' :  '1/144',
    '1 100' :  '1/100',
    '1 60'  :  '1/60',
  }

  file_model_info['access_name'] =  model_kit.replace('-', '_')
  file_model_info['title']       =  [model_kit] + file_model_info.get('title', [])

  display_name = model_kit.replace('-', ' ')

  for k,v in model_scale.items():
    if k in display_name:
      file_model_info['display_name'] = display_name.replace(k, v)
      break
  file_model_info['display_name'] = file_model_info.get('display_name', model_kit)




  if file_model_info.get('description') == None:
    file_model_info['description'] = ''
  return model_kit, file_model_info


def is_other_kit(model_kit, file_model_info):
  if 'pre-order' in model_kit or 'preorder' in model_kit:
    return True

  elif 'star-wars' in model_kit:
    return True
  elif 'decal' in model_kit:
    return True
  else:
    return False


#
def generate_sql_file(product_line, input_location, output_location):
  with open(f'{input_location}/{product_line}.json', 'r') as f:
    json_data = json.load(f)
    f.close()

  sql_statements = (
    'INSERT INTO models ( '
    'access_name, '
    'display_name, '
    'japanese_name, '
    'sku, '
    # 'info, '
    'info_source, '
    'release_date, '
    'timeline_id, '
    'series_id, '
    'product_line_id, '
    'manufacturer_id, '
    'scale_id, '
    'updated_date, '
    'created_date, '
    'user_update_id '
    ') '
    'VALUES '
  )

  sql_list        =  [ build_model_sql_vals(model_kit, file_model_info) for model_kit, file_model_info in json_data.items() if model_kit != OTHER_KITS]
  sql_statements +=  ',\n'.join(sql_list)
  sql_statements +=  ';'

  HELPER.compose_download_dir(output_location)
  with open(f'{output_location}/{product_line}.sql', 'w') as f:
    f.write(sql_statements)
    f.close()

  return

def build_model_sql_vals(model_kit, file_model_info):
  sql = "(\n  "
  if file_model_info.get('product_line') == None:
    print(model_kit)

  data = [
    "'%s'" % file_model_info['access_name'],
    "'%s'" % file_model_info['display_name'],
    "NULL",
    "'%s'" % file_model_info.get('sku', "NULL"),
    # "\n\n".join(file_model_info['description']),
    "'usa_gundam'",
    "NULL",
    "(SELECT timeline_id from timelines WHERE access_name = '%s')" % file_model_info["timeline"],
    "(SELECT series_id from series WHERE access_name = '%s')" % file_model_info["series"],
    "(SELECT product_line_id from product_lines WHERE short_name = '%s')" % file_model_info["product_line"],
    "(SELECT manufacturer_id from manufacturers WHERE access_name = '%s')" % file_model_info["manufacturer"],
    "(SELECT scale_id from scales WHERE scale_value = '%s')" % file_model_info["scale"],
    "CURRENT_TIMESTAMP",
    "CURRENT_TIMESTAMP",
    "(SELECT user_id from users WHERE user_name = 'initial_user')",
  ]
  sql +=  ",\n  ".join(data)
  sql +=  "\n)"
  return sql

if __name__ == '__main__':
  HELPER.time_fn_execution(main)
