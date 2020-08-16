import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class Helper():
  def make_dir_if_no_dir(self, desired_location):
    if not os.path.exists(desired_location):
      os.mkdir(desired_location)
    return


  def compose_download_dir(self, download_dir):
    # takes in desired directory
    # loops through each sub_dir and creates if not exists
    dirs = download_dir.split('/')

    compose_dir = ''
    for dir in dirs:
      compose_dir += f'{dir}/'
      self.make_dir_if_no_dir(compose_dir)
    return


  def download_dynamic_html(self, page_url, download_dir, alt_filename=None):
    # create dirs if needed
    self.compose_download_dir(download_dir)

    # check if file already exists (already downloaded)
    download_location = f'{download_dir}/{alt_filename if alt_filename else page_url}.html'

    if os.path.exists(download_location):
      print('page already downloaded, skipping: ', page_url)
      return

    print('downloading page:', page_url)
    try:
      driver = webdriver.Firefox()
      driver.implicitly_wait(20)
      driver.get(page_url)
      page_html = driver.page_source
    finally:
      driver.quit()
      time.sleep(1)

    with open(download_location, 'w') as f:
      f.write(page_html)

    return


  def update_json_file_content(self, json_data, product_line, output_file):
    with open(output_file, 'r+') as f:
      file_data = json.load(f)
      file_data[product_line] = json_data if file_data.get(product_line) == None else { **file_data[product_line], **json_data }
      f.seek(0)
      f.write(json.dumps(file_data, indent=2))
      f.close()
    return


  def time_fn_execution(self, fn):
    start_time = time.time()
    fn()
    seconds  =  time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S",time.gmtime(seconds)))
    return


  def safe_cast(self, val, to_type):
    try:
      return to_type(val)
    except:
      return val


if __name__ == '__main__':
  helper = Helper()
