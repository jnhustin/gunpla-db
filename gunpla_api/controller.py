from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger
from gunpla_api.utils         import Utils
from gunpla_api.gunpla_sql    import GunplaSql
from gunpla_api.exceptions    import UnsupportedTableException

from gunpla_api.timeline.timeline           import Timeline
from gunpla_api.model_scale.model_scale     import ModelScale
from gunpla_api.product_line.product_line   import ProductLine
from gunpla_api.manufacturer.manufacturer   import Manufacturer
from gunpla_api.series.series               import Series

logger = Logger().get_logger()

class Controller():
  db    =  DbConnector()
  utils =  Utils()
  sql   =  GunplaSql()

  models =  {
    'timeline'     :  Timeline(),
    'model_scale'  :  ModelScale(),
    'product_line' :  ProductLine(),
    'manufacturer' :  Manufacturer(),
    'series'       :  Series(),
  }


  def direct_select_request(self, table, request):
    try:
      query_params =  request.args
      query        =  self.models[table].get_select_query(query_params) if query_params else self.models[table].get_select_all_query()
    except UnsupportedTableException:
      logger.exception('request to unsupported table')

    db_results =  self.db.execute_sql(self.db.process_select_results, query)
    res        =  self.utils.db_data_to_json(db_results)

    logger.debug('completed select', extra={'res': res})
    return res


  def direct_insert_request(self, table, request):
    try:
      table        =  table.lower()
      insert_query =  self.models[table].get_insert_query()
      sql_vals     =  self.sql.get_sql_vals(self.models[table].insert_sql_vals, request)
    except UnsupportedTableException:
      logger.exception('request to unsupported table')

    res = self.db.execute_sql( self.db.process_insert_results, insert_query, sql_vals)
    logger.debug('completed insert', extra=res)
    return


  def direct_update_request(self, table, request):
    try:
      table        =  table.lower()
      update_query =  self.models[table].get_update_query(request)
      sql_vals     =  self.sql.get_sql_vals(self.models[table].update_sql_vals, request)
    except UnsupportedTableException:
      logger.exception('request to unsupported table')

    db_results =  self.db.execute_sql(self.db.process_update_results, update_query, sql_vals)
    logger.debug('completed update', extra=db_results)
    return


  def process_delete_request(self, table, _id):
    # get delete query
    table_name =  self.models[table].table_name
    table_id   =  self.models[table].table_id
    query      =  self.sql.get_delete_query(table_name, table_id)

    # delete
    db_results =  self.db.execute_sql(self.db.process_delete_results, query, { '_id': _id })
    logger.debug('completed delete', extra=db_results)
    return



