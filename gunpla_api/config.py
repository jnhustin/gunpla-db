import os
import json
from gunpla_api.singleton import Singleton
from dotenv import load_dotenv
load_dotenv('.env.local')

@Singleton
class Config:
  app_name =  'gunpla_api'
  stage    =  os.getenv('STAGE')

  # db connector
  db_host     =  os.getenv('DB_HOST')
  db_port     =  os.getenv('DB_PORT')
  db_user     =  os.getenv('DB_USER')
  db_password =  os.getenv('DB_PASSWORD')
  db_name     =  os.getenv('DB_NAME')

  # env_vars
  def __init__(self):
    print('config class loaded')


  def something(self):
    pass
