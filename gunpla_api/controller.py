from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger

from gunpla_api.timeline.timeline         import Timeline
from gunpla_api.model_scale.model_scale   import ModelScale
from gunpla_api.product_line.product_line import ProductLine
from gunpla_api.brand.brand               import Brand
from gunpla_api.franchise.franchise       import Franchise

logger = Logger().get_logger()

class Controller():
  db =  DbConnector()

  # models
  timeline     =  Timeline()
  model_scale  =  ModelScale()
  product_line =  ProductLine()
  brand        =  Brand()
  franchise    =  Franchise()


  def direct_select_request(self, table, request):
    if table == 'timeline':
      results = self.timeline.select_timelines()

    return results


  def direct_insert_request(self, table, request):
    if   table == 'timeline':
      self.timeline.insert_timeline(request)
    elif table == 'model_scale':
      self.model_scale.insert_model_scale(request)
    elif table == 'product_line':
      self.product_line.insert_product_line(request)
    elif table == 'brand':
      self.brand.insert_brand(request)
    elif table == 'franchise':
      self.franchise.insert_franchise(request)


  def direct_update_request(self, table, request):
    if   table == 'timeline':
      self.timeline.update_timeline(request)
    elif table == 'model_scale':
      self.model_scale.update_model_scale(request)
    elif table == 'product_line':
      self.product_line.update_product_line(request)
    # elif table == 'brand':
    #   self.brand.update_brand(request)
    # elif table == 'franchise':
    #   self.franchise.update_franchise(request)
