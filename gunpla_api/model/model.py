
from gunpla_api.gunpla_sql   import GunplaSql
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

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

  def get_select_query(self, args):
    # meant for filters
    display_name =  self.get_query_param('display_name', args, optional=True)
    timeline     =  self.get_query_param('timeline', args, optional=True)
    series       =  self.get_query_param('series', args, optional=True)
    product_line =  self.get_query_param('product_line', args, optional=True)
    manufacturer =  self.get_query_param('manufacturer', args, optional=True)
    scale        =  self.get_query_param('scale', args, optional=True)
    offset       =  self.get_query_param('page_number', args, optional=True)

    return ("""
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

      -- WHERE CLAUSE
      WHERE mod.display_name ILIKE %(display_name)s
      AND t.display_name ILIKE %(timeline)s

      GROUP BY mod.model_id, t.display_name, se.display_name, p.display_name, sc.scale_value, man.display_name

      --ORDER BY mod.<COLUMN> <ASC/DESC>

      LIMIT 100
      OFFSET 0

      ;
    """, {'display_name': f'%{display_name}%', 'timeline': f'%{timeline}%'})


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
