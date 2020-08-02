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

  insert_sql_vals =  ['display_name', 'short_name']
  update_sql_vals =  ['display_name', 'short_name', table_id]

  # methods
  get_json_field = validation.get_json_field


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (access_name, display_name, short_name, created_date, updated_date, user_update_id)"
      "VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);"
    )


  def get_select_all_query(self):
    return f"SELECT product_line_id as id, access_name, display_name, short_name FROM {self.table_name};"


  def select(self, request):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)
    return results


  def get_update_query(self, request):
    update_fields = self.db.get_sql_vals(['display_name', 'short_name'], request)
    return self.db.get_update_query(self.table_name, update_fields, self.table_id)


