from gunpla_api.db_connector  import DbConnector
from gunpla_api.logger        import Logger
from gunpla_api.utils         import Utils
from gunpla_api.gunpla_sql    import GunplaSql
from gunpla_api.exceptions    import UnsupportedTableException

from gunpla_api.resources.timeline       import Timeline
from gunpla_api.resources.model_scale    import ModelScale
from gunpla_api.resources.product_line   import ProductLine
from gunpla_api.resources.manufacturer   import Manufacturer
from gunpla_api.resources.series         import Series
from gunpla_api.resources.model          import Model

logger = Logger().get_logger()

class Controller():
  db    =  DbConnector()
  utils =  Utils()
  sql   =  GunplaSql()

  resources =  {
    'timeline'     :  Timeline(),
    'model_scale'  :  ModelScale(),
    'product_line' :  ProductLine(),
    'manufacturer' :  Manufacturer(),
    'series'       :  Series(),
    'model'        :  Model(),
  }

  def access_resource(self, table):
    try:
      table = table.lower()
      return self.resource[table]
    except KeyError:
      logger.exception('request to unsupported table')
      raise UnsupportedTableException


  def direct_select_request(self, table, request):
    resource     =  self.access_resource(table)
    query_params =  request.args

    search_params =  resource.get_search_params(query_params)
    query         =  resource.get_select_query(search_params, query_params)

    db_results =  self.db.execute_sql(self.db.process_select_results, query, search_params)
    res        =  self.utils.db_data_to_json(db_results)

    logger.debug('completed select', extra={'res_len': len(res)})
    return res


  def direct_insert_request(self, table, request):
    resource     =  self.access_resource[table]
    insert_query =  resource.get_insert_query()
    sql_vals     =  self.sql.get_sql_vals(resource.required_insert_sql_vals, resource.optional_insert_sql_vals, request,)

    res = self.db.execute_sql( self.db.process_insert_results, insert_query, sql_vals)
    logger.debug('completed insert', extra=res)
    return


  def direct_update_request(self, table, request):
    resource      =  self.access_resource[table]
    update_fields =  self.sql.get_update_fields(resource.required_update_fields, resource.optional_update_fields, request)
    update_query  =  self.sql.get_update_query(resource.table_id, resource.table_name, update_fields)
    sql_vals      =  self.sql.get_sql_vals(resource.required_update_sql_vals, resource.optional_update_sql_vals, request)

    db_results =  self.db.execute_sql(self.db.process_update_results, update_query, sql_vals)
    logger.debug('completed update', extra=db_results)
    return


  def process_delete_request(self, table, _id):
    resource =  self.access_resource[table]

    # get delete query
    table_name =  resource.table_name
    table_id   =  resource.table_id
    query      =  self.sql.get_delete_query(table_name, table_id)

    # delete
    db_results =  self.db.execute_sql(self.db.process_delete_results, query, { '_id': _id })
    logger.debug('completed delete', extra=db_results)
    return



