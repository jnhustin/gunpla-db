from gunpla_api.db_connector  import DbConnector
from gunpla_api.config        import Config
from gunpla_api.validation    import Validation
from gunpla_api.utils         import Utils
from gunpla_api.logger        import Logger

from gunpla_api.timeline.timeline         import Timeline
from gunpla_api.model_scale.model_scale   import ModelScale
from gunpla_api.product_line.product_line import ProductLine
from gunpla_api.brand.brand               import Brand
from gunpla_api.franchise.franchise       import Franchise
from gunpla_api.franchise.franchise       import Franchise

logger = Logger().get_logger()

class Controller():
  config     =  Config()
  db         =  DbConnector()
  validation =  Validation()
  utils      =  Utils()

  timeline     =  Timeline()
  model_scale  =  ModelScale()
  product_line =  ProductLine()
  brand        =  Brand()
  franchise    =  Franchise()



  def insert_timeline(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.timeline.get_insert_query(),
      self.timeline.get_insert_param_dict(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def insert_model_scale(self, request):
    model_scale =  self.validation.get_json_field('model_scale', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.model_scale.get_insert_query(),
      self.model_scale.get_insert_param_dict(model_scale), )

    logger.debug('completed insert', extra=res)
    return


  def insert_product_line(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    short_name   =  self.validation.get_json_field('short_name', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.product_line.get_insert_query(),
      self.product_line.get_insert_param_dict(access_name, display_name, short_name), )

    logger.debug('completed insert', extra=res)
    return


  def insert_brand(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.brand.get_insert_query(),
      self.brand.get_insert_param_dict(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def insert_franchise(self, request):
    display_name =  self.validation.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.franchise.get_insert_query(),
      self.franchise.get_insert_param_dict(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def get_timelines(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.timeline.get_select_all_query(),
      None)
    results =  self.utils.db_data_to_dict(db_results)

    return results


  def update_timeline(self, request):
    timeline_id  =  self.validation.get_json_field('id',request.json)
    display_name =  self.validation.get_json_field('display_name',request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    db_results   =  self.db.execute_sql(
      self.db.process_update_results,
      self.timeline.get_update_query(timeline_id, access_name, display_name),
      self.timeline.get_sql_vals(timeline_id, access_name, display_name),
    )
    logger.debug('completed update', extra=db_results)
    return


  def update_product_line(self, request):
    product_line_id =  self.validation.get_json_field('id',request.json)
    short_name      =  self.validation.get_json_field('short_name', request.json, optional=True)
    display_name    =  self.validation.get_json_field('display_name', request.json, optional=True)
    access_name     =  self.utils.convert_to_snake_case(display_name) if display_name else None

    db_results   =  self.db.execute_sql(
      self.db.process_update_results,
      self.product_line.get_update_query(product_line_id, access_name, display_name, short_name),
      self.product_line.get_sql_vals(product_line_id, access_name, display_name, short_name),
    )
    logger.debug('completed update', extra=db_results)
    return

