from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger

from gunpla_api.timeline.timeline         import Timeline
from gunpla_api.model_scale.model_scale   import ModelScale
from gunpla_api.product_line.product_line import ProductLine
from gunpla_api.brand.brand               import Brand
from gunpla_api.series.series             import Series

logger = Logger().get_logger()

class Controller():
  db =  DbConnector()

  # models
  timeline     =  Timeline()
  model_scale  =  ModelScale()
  product_line =  ProductLine()
  brand        =  Brand()
  series          =  Series()


  def direct_select_request(self, table, request):
    if   table == 'timeline':
      results = self.timeline.select_timelines()
    elif table == 'model_scale':
      results = self.model_scale.select_model_scales()
    elif table == 'product_line':
      results = self.product_line.select_product_lines()
    elif table == 'brand':
      results = self.brand.select_brands()
    elif table == 'series':
      results = self.series.select_series()

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
    elif table == 'series':
      self.series.insert_series(request)


  def direct_update_request(self, table, request):
    if   table == 'timeline':
      self.timeline.update_timeline(request)
    elif table == 'model_scale':
      self.model_scale.update_model_scale(request)
    elif table == 'product_line':
      self.product_line.update_product_line(request)
    elif table == 'brand':
      self.brand.update_brand(request)
    elif table == 'series':
      self.series.update_series(request)
