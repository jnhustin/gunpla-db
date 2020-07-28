from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger

from gunpla_api.timeline.timeline         import Timeline
from gunpla_api.model_scale.model_scale   import ModelScale
from gunpla_api.product_line.product_line import ProductLine
from gunpla_api.manufacturer.manufacturer               import manufacturer
from gunpla_api.series.series             import Series

logger = Logger().get_logger()

class Controller():
  db =  DbConnector()

  # models
  timeline     =  Timeline()
  model_scale  =  ModelScale()
  product_line =  ProductLine()
  manufacturer =  manufacturer()
  series       =  Series()


  def direct_select_request(self, table, request):
    if   table == 'timeline':
      results = self.timeline.select_timelines()
    elif table == 'model_scale':
      results = self.model_scale.select_model_scales()
    elif table == 'product_line':
      results = self.product_line.select_product_lines()
    elif table == 'manufacturer':
      results = self.manufacturer.select_manufacturers()
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
    elif table == 'manufacturer':
      self.manufacturer.insert_manufacturer(request)
    elif table == 'series':
      self.series.insert_series(request)

    return


  def direct_update_request(self, table, request):
    if   table == 'timeline':
      self.timeline.update_timeline(request)
    elif table == 'model_scale':
      self.model_scale.update_model_scale(request)
    elif table == 'product_line':
      self.product_line.update_product_line(request)
    elif table == 'manufacturer':
      self.manufacturer.update_manufacturer(request)
    elif table == 'series':
      self.series.update_series(request)

    return


  def process_delete_request(self, table, _id):
    if   table == 'timeline':
      query = self.db.get_delete_query(self.timeline.table_name, self.timeline.table_id)
    elif table == 'model_scale':
      query = self.db.get_delete_query(self.model_scale.table_name, self.model_scale.table_id)
    elif table == 'product_line':
      query = self.db.get_delete_query(self.product_line.table_name, self.product_line.table_id)
    elif table == 'manufacturer':
      query = self.db.get_delete_query(self.manufacturer.table_name, self.manufacturer.table_id)
    elif table == 'series':
      query = self.db.get_delete_query(self.series.table_name, self.series.table_id)

    db_results =  self.db.execute_sql(self.db.process_delete_results, query, { '_id': _id })
    logger.debug('completed delete', extra=db_results)
    return
