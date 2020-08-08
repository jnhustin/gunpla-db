
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

  table_name =  'models'
  table_id   =  'model_id'

  # methods
  get_json_field  =  validation.get_json_field
  get_query_param =  validation.get_query_param

  def get_select_all_query(self):
    return f"""
      SELECT
        mod.model_id,
        mod.access_name,
        mod.display_name,
        mod.japanese_name,
        mod.info,
        mod.info_source,
        mod.release_date,
        t.display_name,
        se.display_name,
        p.display_name,
        man.display_name,
        sc.scale_value
      FROM models mod
      LEFT JOIN timelines     t   ON mod.timeline_id       = t.timeline_id
      LEFT JOIN series        se  ON mod.series_id         = se.series_id
      LEFT JOIN product_lines p   ON mod.product_line_id   = p.product_line_id
      LEFT JOIN manufacturers man ON mod.manufacturer_id   = man.manufacturer_id
      LEFT JOIN scales        sc  ON mod.timeline_id       = sc.scale_id
    ;
    """


  def get_select_query(self, search_params, query_params):
    where_clause =  self.build_where_statement(search_params)
    offset       =  self.get_query_param('page_number', query_params, optional=True) or 0    # TODO AFFECTED BY THIS GET_QUERY_PARAM
    sort_order   =  'ASC' if self.get_query_param('sort_order', query_params, optional=True) ==  'ASC' else 'DESC'   # TODO AFFECTED BY THIS GET_QUERY_PARAM
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

      "LIMIT 100 "
      f"OFFSET {offset} "
      ";"
    )


  def get_search_params(self, query_params):
    filter_params =  {
      'model_name'   :  self.get_query_param('model_name', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
      'timeline'     :  self.get_query_param('timeline', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
      'series'       :  self.get_query_param('series', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
      'product_line' :  self.get_query_param('product_line', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
      'manufacturer' :  self.get_query_param('manufacturer', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
      'scale'        :  self.get_query_param('scale', query_params, optional=True),   # TODO AFFECTED BY THIS GET_QUERY_PARAM
    }
    sent_params      =  self.utils.remove_empty_json_keys(filter_params)
    formatted_params =  self.format_search_params(sent_params)
    return formatted_params


  def format_search_params(self, sent_params: dict):
    # loops query_param dict and converts val lists into psycopg string-formatted vals
    formatted        =  {}
    is_pattern_match =  ['model_name']
    for k, v in sent_params.items():
      formatted[k] = f"({ '|'.join(v) })" if k in is_pattern_match else tuple(v)

    return formatted


  def build_where_statement(self, search_params: dict):
    try:
      if len(search_params) == 0:
        return ''

      accepted_params = {
        'model_name'   :  'mod.display_name ~* %(model_name)s',
        'timeline'     :  't.timeline_id IN %(timeline)s',
        'series'       :  'se.series_id IN %(series)s',
        'product_line' :  'p.product_line_id IN %(product_line)s',
        'manufacturer' :  'man.manufacturer_id IN %(manufacturer)s',
        'scale'        :  'sc.scale_id IN %(scale)s',
      }
      where_clause =  ' AND '.join([accepted_params[k] for k in accepted_params.keys() if k in search_params])

      sql  =  'WHERE '
      sql +=  where_clause
      sql +=  ' '

      return sql
    except KeyError as e:
      logger.exception('user attempted unsupported field', extra={'search_params': search_params})
      raise BadRequestException(f'{e} not an accepted field')


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
    sort_by = self.get_query_param('sort_by', query_params, optional=True) # TODO AFFECTED BY THIS GET_QUERY_PARAM
    return sort_options['model_id'] if len(sort_by) == 0 else sort_options[sort_by[0]] # TODO AFFECTED BY THIS GET_QUERY_PARAM



  def get_insert_query(self):
    return (
      f"""
        INSERT INTO {self.table_name} (
          access_name,
          display_name,
          japanese_name,
          sku,
          info,
          info_source,
          release_date,
          timeline_id,
          series_id,
          product_line_id,
          manufacturer_id,
          scale_id,
          updated_date,
          created_date,
          user_update_id
        VALUES (
          %(access_name)s,
          %(display_name)s,
          %(japanese_name)s,
          %(sku)s,
          %(info)s,
          %(info_source)s,
          %(release_date)s,
          %(timeline_id)s,
          %(series_id)s,
          %(product_line_id)s,
          %(manufacturer_id)s,
          %(scale_id)s,
          CURRENT_TIMESTAMP,
          CURRENT_TIMESTAMP,
          %(user_id)s
        )
      );"""
    )


  def insert(self, request):
    display_name    =  self.get_json_field('display_name', request.json)
    access_name     =  self.utils.convert_to_snake_case(display_name)
    japanese_name   =  self.get_json_field('japanese_name', request.json)
    sku             =  self.get_json_field('sku', request.json)
    info            =  self.get_json_field('info', request.json, optional=True)
    info_source     =  self.get_json_field('info_source', request.json, optional=True)
    release_date    =  self.get_json_field('release_date', request.json, optional=True)
    timeline_id     =  self.get_json_field('timeline_id', request.json)
    series_id       =  self.get_json_field('series_id', request.json)
    product_line_id =  self.get_json_field('product_line_id', request.json)
    manufacturer_id =  self.get_json_field('manufacturer_id', request.json)
    scale_id        =  self.get_json_field('scale_id', request.json)
    updated_date    =  self.get_json_field('updated_date', request.json)
    created_date    =  self.get_json_field('created_date', request.json)
    user_update_id  =  self.get_json_field('user_update_id', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.get_insert_query(),
    )
