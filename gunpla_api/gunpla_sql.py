from gunpla_api.config      import Config
from gunpla_api.logger      import Logger
from gunpla_api.utils       import Utils
from gunpla_api.validation  import Validation

logger = Logger().get_logger()

class GunplaSql():
  config     =  Config()
  utils      =  Utils()
  validation =  Validation()

  user_id = 1


  # methods
  get_json_field = validation.get_json_field


  def get_standard_insert_query(self, table):
    return (
      f"INSERT INTO {table} (access_name, display_name, created_date, updated_date, user_update_id)"
      f"VALUES (%(access_name)s, %(display_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {self.user_id});"
    )


  def get_update_query(self, table_name, update_fields, table_id):
    query  =  f"UPDATE {table_name}"
    query +=  self.generate_update_set_query(update_fields)
    query +=  f"WHERE {table_id} = %({table_id})s;"
    return query


  def generate_update_set_query(self, update_fields: dict):
    query  =  " SET "
    query +=  ",".join( [ f"{col} = %({col})s" for col, val in update_fields.items() if val != None ] )
    query +=  f", user_update_id = {self.user_id}, updated_date='NOW' "
    return query


  def get_delete_query(self, table_name, table_id):
    return f"DELETE FROM {table_name} WHERE {table_id} = %(_id)s"


  def get_sql_vals(self, desired_keys: list, request):
    sql_vals = { val : self.get_json_field(val, request.json) for val in desired_keys }

    if 'display_name' in desired_keys:
      sql_vals['access_name'] = self.utils.convert_to_snake_case(sql_vals['display_name'])

    return sql_vals
