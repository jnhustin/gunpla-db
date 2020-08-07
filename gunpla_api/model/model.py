from gunpla_api.gunpla_sql  import GunplaSql
from gunpla_api.logger        import Logger
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
  get_json_field = validation.get_json_field

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

