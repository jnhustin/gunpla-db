from gunpla_api.gunpla_db   import GunplaDb
from gunpla_api.config      import Config
from gunpla_api.validation  import Validation

class Controller():
  config     =  Config()
  gunpla_db  =  GunplaDb()
  validation =  Validation()


  def post_timeline(self, request):
    timeline = self.validation.get_field('timeline', request.json)
    self.gunpla_db.insert_timeline(timeline)
    return


  def post_model_scape(self, request):
    model_scale = self.validation.get_field('model_scale', request.json)
    self.gunpla_db.insert_model_scale(model_scale)
    return
