from gunpla_api.db_connector import DbConnector
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

logger = Logger().get_logger()



class Brand():
  db         =  DbConnector()
  utils      =  Utils()
  validation =  Validation()

  table_name = 'brands'
  table_id   = 'brand_id'

  # methods
  get_json_field = validation.get_json_field


  def get_insert_query(self):
    return self.db.get_standard_insert_query('brands')


  def get_select_all_query(self):
    return f"SELECT brand_id as id, access_name, display_name FROM {self.table_name};"


  def get_sql_vals(self, access_name, display_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals


  def select_brands(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)

    return results


  def insert_brand(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.get_insert_query(),
      self.get_sql_vals(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def update_brand(self, request):
    brand_id      =  self.get_json_field('id', request.json)
    display_name  =  self.get_json_field('display_name', request.json)
    update_fields =  {
      'display_name' :  display_name,
      'access_name'  :  self.utils.convert_to_snake_case(display_name),
    }

    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.db.get_update_query(self.table_name, update_fields, self.table_id),
      self.utils.append_fields_to_json(update_fields, brand_id=brand_id),
    )

    logger.debug('completed update', extra=db_results)
    return
