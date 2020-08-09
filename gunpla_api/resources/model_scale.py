from gunpla_api.gunpla_sql   import GunplaSql
# from gunpla_api.logger       import Logger
# from gunpla_api.utils        import Utils
# from gunpla_api.validation   import Validation

# logger = Logger().get_logger()


class ModelScale():
  sql        =  GunplaSql()
  # utils      =  Utils()
  # validation =  Validation()

  table_name =  'scales'
  table_id   =  'scale_id'

  required_insert_sql_vals =  ['scale_value']
  optional_insert_sql_vals =  []

  required_update_sql_vals =  ['scale_value', '_id']
  optional_update_sql_vals =  []

  required_update_fields =  ['scale_value']
  optional_update_fields =  []


  # # methods
  # get_json_field = validation.get_json_field


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (scale_value, created_date, updated_date, user_update_id)"
      f"VALUES (%(scale_value)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {self.sql.user_id};"
    )


  def get_select_all_query(self):
    return f"SELECT scale_id as id, scale_value as scale FROM {self.table_name};"


  def get_select_query(self):
    pass

