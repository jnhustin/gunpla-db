from gunpla_api.gunpla_db   import GunplaDb
from gunpla_api.config      import Config
from gunpla_api.validation  import Validation
from gunpla_api.utils       import Utils

class Controller():
  config     =  Config()
  gunpla_db  =  GunplaDb()
  validation =  Validation()
  utils      =  Utils()


  def post_timeline(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    self.gunpla_db.insert_timeline(access_name, display_name)
    return


  def post_model_scale(self, request):
    model_scale = self.validation.get_json_field('model_scale', request.json)
    self.gunpla_db.insert_model_scale(model_scale)
    return


  def post_product_line(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    short_name   =  self.validation.get_json_field('short_name', request.json)
    self.gunpla_db.insert_product_line(access_name, display_name, short_name)
    return


  def post_brand(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    self.gunpla_db.insert_product_line(access_name, display_name)
    return


  def post_franchise(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    self.gunpla_db.insert_product_line(access_name, display_name)
    return
