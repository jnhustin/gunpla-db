import os
import json
from gunpla_api.singleton import Singleton
from dotenv import load_dotenv
load_dotenv('.env.local')

@Singleton
class Config:
  app_name =  'gunpla_api'
  stage    =  os.getenv('STAGE')

  # env_vars
  def __init__(self):
    print('config class loaded')


  def something(self):
    pass
