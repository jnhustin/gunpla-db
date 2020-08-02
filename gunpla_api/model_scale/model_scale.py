from gunpla_api.db_connector import DbConnector
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

logger = Logger().get_logger()


class ModelScale():
  db         =  DbConnector()
  utils      =  Utils()
  validation =  Validation()

  table_name =  'scales'
  table_id   =  'scale_id'

  insert_sql_vals =  ['scale_value']
  update_sql_vals =  ['scale_value', table_id]


  # methods
  get_json_field = validation.get_json_field

  def get_select_all_query(self):
    return f"SELECT scale_id as id, scale_value as scale FROM {self.table_name};"


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (scale_value, created_date, updated_date, user_update_id)"
      f"VALUES (%(scale_value)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {self.db.user_id};"
    )


  def select(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)

    return results

  def get_update_query(self, request):
    update_fields = self.db.get_sql_vals(['scale_value'], request)
    return self.db.get_update_query(self.table_name, update_fields, self.table_id)
