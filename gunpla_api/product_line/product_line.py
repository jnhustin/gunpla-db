from gunpla_api.db_connector import DbConnector
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

logger = Logger().get_logger()


class ProductLine():
  db         =  DbConnector()
  utils      =  Utils()
  validation =  Validation()

  table_name =  'product_lines'
  table_id   =  'product_line_id'

  # methods
  get_json_field = validation.get_json_field


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (access_name, display_name, short_name, created_date, updated_date, user_update_id)"
      "VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);"
    )


  def get_select_all_query(self):
    return f"SELECT product_line_id as id, access_name, display_name, short_name FROM {self.table_name};"


  def get_sql_vals(self, display_name, access_name, short_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals


  def select_product_lines(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)
    return results


  def insert_product_line(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    short_name   =  self.get_json_field('short_name', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.get_insert_query(),
      self.get_sql_vals(access_name, display_name, short_name),
    )

    logger.debug('completed insert', extra=res)
    return


  def update_product_line(self, request):
    product_line_id =  self.get_json_field('id', request.json)
    display_name    =  self.get_json_field('display_name', request.json, optional=True)
    update_fields   =  {
      'short_name'   :  self.get_json_field('short_name', request.json, optional=True),
      'display_name' : display_name,
      'access_name'  :  self.utils.convert_to_snake_case(display_name) if display_name else None,
    }

    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.db.get_update_query(self.table_name, update_fields, self.table_id),
      self.utils.append_fields_to_json(update_fields, product_line_id=product_line_id),
    )
    logger.debug('completed update', extra=db_results)
    return

