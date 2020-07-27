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

logger = Logger().get_logger()

class Controller():
  config     =  Config()
  db         =  DbConnector()
  validation =  Validation()
  utils      =  Utils()

  # models
  timeline     =  Timeline()
  model_scale  =  ModelScale()
  product_line =  ProductLine()
  brand        =  Brand()
  franchise    =  Franchise()

  # methods
  get_json_field = validation.get_json_field


  def insert_timeline(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.timeline.get_insert_query(),
      self.timeline.get_sql_vals(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def insert_model_scale(self, request):
    model_scale =  self.get_json_field('model_scale', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.model_scale.get_insert_query(),
      self.model_scale.get_sql_vals(model_scale), )

    logger.debug('completed insert', extra=res)
    return


  def insert_product_line(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)
    short_name   =  self.get_json_field('short_name', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.product_line.get_insert_query(),
      self.product_line.get_sql_vals(access_name, display_name, short_name),
    )

    logger.debug('completed insert', extra=res)
    return


  def insert_brand(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.brand.get_insert_query(),
      self.brand.get_sql_vals(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def insert_franchise(self, request):
    display_name =  self.get_json_field('display_name', request.json)
    access_name  =  self.utils.convert_to_snake_case(display_name)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.franchise.get_insert_query(),
      self.franchise.get_sql_vals(access_name, display_name), )

    logger.debug('completed insert', extra=res)
    return


  def get_timelines(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.timeline.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)

    return results


  def update_timeline(self, request):
    timeline_id   =  self.get_json_field('id',request.json)
    display_name  =  self.get_json_field('display_name',request.json)
    update_fields =  {
      'display_name' :  display_name,
      'access_name'  :  self.utils.convert_to_snake_case(display_name),
    }

    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.timeline.get_update_query(timeline_id, update_fields),
      self.utils.append_fields_to_json(update_fields, timeline_id=timeline_id),
    )

    logger.debug('completed update', extra=db_results)
    return


  def update_model_scale(self, request):
    timeline_id   =  self.get_json_field('id',request.json)
    display_name  =  self.get_json_field('display_name',request.json)
    update_fields =  {
      'display_name' :  display_name,
      'access_name'  :  self.utils.convert_to_snake_case(display_name),
    }
    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.timeline.get_update_query(timeline_id, update_fields),
      self.utils.append_fields_to_json(update_fields, timeline_id=timeline_id),
    )

    logger.debug('completed update', extra=db_results)
    return


  def update_product_line(self, request):
    product_line_id =  self.get_json_field('id',request.json)
    display_name    =  self.get_json_field('display_name', request.json, optional=True)
    update_fields   =  {
      'short_name'   :  self.get_json_field('short_name', request.json, optional=True),
      'display_name' : display_name,
      'access_name'  :  self.utils.convert_to_snake_case(display_name) if display_name else None,
    }

    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.product_line.get_update_query(product_line_id, update_fields),
      self.utils.append_fields_to_json(update_fields, product_line_id=product_line_id),
    )
    logger.debug('completed update', extra=db_results)
    return

