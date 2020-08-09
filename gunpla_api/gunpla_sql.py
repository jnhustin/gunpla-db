from gunpla_api.config      import Config
from gunpla_api.logger      import Logger
from gunpla_api.utils       import Utils
from gunpla_api.validation  import Validation
from gunpla_api.exceptions  import BadRequestException

logger = Logger().get_logger()

class GunplaSql():
  config     =  Config()
  utils      =  Utils()
  validation =  Validation()

  user_id = 1


  # methods
  get_json_field  =  validation.get_json_field
  get_query_param =  validation.get_query_param


  def get_standard_insert_query(self, table):
    return (
      f"INSERT INTO {table} (access_name, display_name, created_date, updated_date, user_update_id)"
      f"VALUES (%(access_name)s, %(display_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, {self.user_id});"
    )


  def get_update_query(self, table_id, table_name, update_fields):
    query  =  f"UPDATE {table_name}"
    query +=  self.build_update_set_query(update_fields)
    query +=  f"WHERE {table_id} = %(_id)s;"
    return query


  def get_update_fields(self, required_fields, optional_fields, request):
    update_fields: dict = self.get_sql_vals(required_fields, optional_fields, request)
    if len(update_fields) == 0:
      raise BadRequestException('Payload missing fields to update')

    return update_fields


  def build_update_set_query(self, update_fields: dict):
    query  =  " SET "
    query +=  ",".join( [ f"{col} = %({col})s" for col, val in update_fields.items() ] )
    query +=  f", user_update_id = {self.user_id}, updated_date='NOW' "
    return query


  def get_delete_query(self, table_name, table_id):
    return f"DELETE FROM {table_name} WHERE {table_id} = %(_id)s"


  def get_sql_vals(self, required_keys: list, optional_keys: list, request):
    required_vals =  { val : self.get_json_field(val, request.json) for val in required_keys }
    optional_vals =  { val : self.get_json_field(val, request.json, optional=True) for val in optional_keys }
    optional_vals =  self.utils.remove_empty_json_keys(optional_vals)

    if 'display_name' in required_keys:
      required_vals['access_name'] = self.utils.convert_to_snake_case(required_vals['display_name'])

    return { **required_vals, **optional_vals }


  def get_pagination(self, query_params, limit):
    # page will start at 1
    sent_offset = self.get_query_param('page_number', query_params, optional=True)
    if sent_offset is None:
      return 0

    return (int(sent_offset) - 1) * limit


  def build_where_query(self, accepted_params: dict, search_params: dict):
    if len(search_params) == 0:
      return ''

    sql  =  'WHERE '
    sql +=  ' AND '.join([accepted_params[k] for k in accepted_params.keys() if k in search_params])
    sql +=  ' '

    return sql


  def format_select_search_params(self, vals_for_sql_regex: list, sent_params: dict):
    # loops query_param dict and converts val lists into psycopg string-formatted vals
    formatted =  {}
    for k, v in sent_params.items():
      split_vals   =  [ element.strip() for element in v.split(',') ]
      formatted[k] =  f"({ '|'.join(split_vals) })" if k in vals_for_sql_regex else tuple(split_vals)

    return formatted
