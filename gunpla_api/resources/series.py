from gunpla_api.gunpla_sql   import GunplaSql
# from gunpla_api.logger       import Logger
# from gunpla_api.utils        import Utils
# from gunpla_api.validation   import Validation

# logger = Logger().get_logger()



class Series():
  sql        =  GunplaSql()
  # utils      =  Utils()
  # validation =  Validation()

  table_name =  'series'
  table_id   =  'series_id'

  required_insert_sql_vals =  ['display_name']
  optional_insert_sql_vals =  []

  required_update_sql_vals =  ['display_name', '_id']
  optional_update_sql_vals =  []

  required_update_fields =  ['display_name']
  optional_update_fields =  []

  # # methods
  # get_json_field = validation.get_json_field


  def get_insert_query(self):
    return self.sql.get_standard_insert_query(self.table_name)


  def get_select_all_query(self):
    return f"SELECT series_id as id, access_name, display_name FROM {self.table_name};"


  def get_select_query(self):
    pass
