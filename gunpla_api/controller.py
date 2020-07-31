from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger

from gunpla_api.timeline.timeline           import Timeline
from gunpla_api.model_scale.model_scale     import ModelScale
from gunpla_api.product_line.product_line   import ProductLine
from gunpla_api.manufacturer.manufacturer   import manufacturer
from gunpla_api.series.series               import Series

logger = Logger().get_logger()

class Controller():
  db     =  DbConnector()
  models =  {
    'timeline'     :  Timeline(),
    'model_scale'  :  ModelScale(),
    'product_line' :  ProductLine(),
    'manufacturer' :  manufacturer(),
    'series'       :  Series(),
  }


  def direct_select_request(self, table, request):
    res = self.models[table].select()
    return res


  def direct_insert_request(self, table, request):
    res = self.models[table].insert(request)
    return res


  def direct_update_request(self, table, request):
    res = self.models[table].update(request)
    return res


  def process_delete_request(self, table, _id):
    # get delete query
    table_name =  self.models[table].table_name
    table_id   =  self.models[table].table_id
    query      =  self.db.get_delete_query(table_name, table_id)

    # delete
    db_results =  self.db.execute_sql(self.db.process_delete_results, query, { '_id': _id })
    logger.debug('completed delete', extra=db_results)
    return
