
from gunpla_api.gunpla_sql   import GunplaSql
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation
from gunpla_api.exceptions   import BadRequestException

logger = Logger().get_logger()

class Model():
  sql        =  GunplaSql()
  utils      =  Utils()
  validation =  Validation()

  table_name   =  'models'
  table_id     =  'model_id'
  select_limit =  50

  vals_for_sql_regex = ['model_name']
  accepted_select_params = {
    'model_name'   :  'mod.display_name ~* %(model_name)s',
    'timeline'     :  't.timeline_id IN %(timeline)s',
    'series'       :  'se.series_id IN %(series)s',
    'product_line' :  'p.product_line_id IN %(product_line)s',
    'manufacturer' :  'man.manufacturer_id IN %(manufacturer)s',
    'scale'        :  'sc.scale_id IN %(scale)s',
  }


  required_insert_sql_vals =  [ 'display_name', 'timeline_id', 'series_id', 'product_line_id', 'manufacturer_id', 'scale_id', ]
  optional_insert_sql_vals =  [ 'japanese_name', 'sku', 'info', 'info_source', 'release_date', ]

  required_update_sql_vals =  [ '_id' ]
  optional_update_sql_vals =  [
    'display_name',
    'timeline_id',
    'series_id',
    'product_line_id',
    'manufacturer_id',
    'scale_id',
    'japanese_name',
    'sku',
    'info',
    'info_source',
    'release_date',
  ]

  required_update_fields =  []
  optional_update_fields =  optional_update_sql_vals


  # methods
  get_json_field  =  validation.get_json_field
  get_query_param =  validation.get_query_param



  def get_select_all_query(self):
    # TODO - maybe just get rid of this
    return (
      "SELECT "
        "mod.model_id, "
        "mod.access_name, "
        "mod.display_name, "
        "mod.japanese_name, "
        "mod.info, "
        "mod.info_source, "
        "mod.release_date, "
        "t.display_name, "
        "se.display_name, "
        "p.display_name, "
        "man.display_name, "
        "sc.scale_value "
      "FROM models mod "
      "LEFT JOIN timelines     t   ON mod.timeline_id       = t.timeline_id "
      "LEFT JOIN series        se  ON mod.series_id         = se.series_id "
      "LEFT JOIN product_lines p   ON mod.product_line_id   = p.product_line_id "
      "LEFT JOIN manufacturers man ON mod.manufacturer_id   = man.manufacturer_id "
      "LEFT JOIN scales        sc  ON mod.timeline_id       = sc.scale_id "

      "GROUP BY mod.model_id, t.display_name, se.display_name, p.display_name, sc.scale_value, man.display_name "
      "ORDER BY mod.model_id ASC "
    ";"
  )


  def get_select_query(self, search_params, query_params):
    where_clause =  self.sql.build_where_query(self.accepted_select_params, search_params)
    offset       =  self.sql.get_pagination(query_params, self.select_limit)
    sort_order   =  'DESC' if self.get_query_param('sort_order', query_params, optional=True) == 'DESC' else 'ASC'
    sort_by      =  self.get_sort_col(query_params)

    return (
      "SELECT "
        "mod.model_id, "
        "mod.access_name, "
        "mod.display_name, "
        "mod.japanese_name, "
        "mod.info, "
        "mod.info_source, "
        "mod.release_date, "
        "t.display_name as timeline, "
        "se.display_name as series, "
        "p.display_name as product_line, "
        "man.display_name as manufacturer, "
        "sc.scale_value as scale "
      "FROM models mod "
      "LEFT JOIN timelines     t   ON mod.timeline_id       = t.timeline_id "
      "LEFT JOIN series        se  ON mod.series_id         = se.series_id "
      "LEFT JOIN product_lines p   ON mod.product_line_id   = p.product_line_id "
      "LEFT JOIN manufacturers man ON mod.manufacturer_id   = man.manufacturer_id "
      "LEFT JOIN scales        sc  ON mod.timeline_id       = sc.scale_id "

      f"{where_clause}"

      "GROUP BY mod.model_id, t.display_name, se.display_name, p.display_name, sc.scale_value, man.display_name "
      f"ORDER BY {sort_by} {sort_order} "

      f"LIMIT {self.select_limit} "
      f"OFFSET {offset} "
      ";"
    )


  def get_search_params(self, query_params):
    filter_params =  {
      'model_name'   :  self.get_query_param('model_name', query_params, optional=True),
      'timeline'     :  self.get_query_param('timeline', query_params, optional=True),
      'series'       :  self.get_query_param('series', query_params, optional=True),
      'product_line' :  self.get_query_param('product_line', query_params, optional=True),
      'manufacturer' :  self.get_query_param('manufacturer', query_params, optional=True),
      'scale'        :  self.get_query_param('scale', query_params, optional=True),
    }
    sent_params      =  self.utils.remove_empty_json_keys(filter_params)
    formatted_params =  self.sql.format_select_search_params(self.vals_for_sql_regex, sent_params)
    return formatted_params


  def get_sort_col(self, query_params):
    sort_options = {
      'model_id'     :  'mod.model_id',
      'model_name'   :  'mod.display_name',
      'timeline'     :  't.display_name',
      'series'       :  'se.display_name',
      'product_line' :  'p.display_name',
      'manufacturer' :  'man.display_name',
      'scale'        :  'sc.display_name',
    }
    sort_by = self.get_query_param('sort_by', query_params, optional=True)

    return sort_options['model_id'] if sort_by is None else sort_options[sort_by]


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} ( "
        "access_name, "
        "display_name, "
        "japanese_name, "
        "sku, "
        "info, "
        "info_source, "
        "release_date, "
        "timeline_id, "
        "series_id, "
        "product_line_id, "
        "manufacturer_id, "
        "scale_id, "
        "updated_date, "
        "created_date, "
        "user_update_id "
      ") "
      "VALUES ( "
        "%(access_name)s, "
        "%(display_name)s, "
        "%(japanese_name)s, "
        "%(sku)s, "
        "%(info)s, "
        "%(info_source)s, "
        "%(release_date)s, "
        "%(timeline_id)s, "
        "%(series_id)s, "
        "%(product_line_id)s, "
        "%(manufacturer_id)s, "
        "%(scale_id)s, "
        "CURRENT_TIMESTAMP, "
        "CURRENT_TIMESTAMP, "
        f"{self.sql.user_id}"
      ") "
      "; "
    )

