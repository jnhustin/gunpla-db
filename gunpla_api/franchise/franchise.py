from gunpla_api.db_connector import DbConnector
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

logger = Logger().get_logger()



class Franchise():
  db         =  DbConnector()
  utils      =  Utils()
  validation =  Validation()

  # methods
  get_json_field = validation.get_json_field


  def get_insert_query(self):
    return self.db.get_standard_insert_query('franchises')


  def get_sql_vals(self, access_name, display_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals


  def insert_franchise(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.get_insert_query(),
      self.get_sql_vals(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return
