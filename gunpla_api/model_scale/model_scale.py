from gunpla_api.db_connector import DbConnector
from gunpla_api.logger       import Logger
from gunpla_api.utils        import Utils
from gunpla_api.validation   import Validation

logger = Logger().get_logger()


class ModelScale():
  db         =  DbConnector()
  utils      =  Utils()
  validation =  Validation()

  table_name =  'scales'
  table_id   =  'scale_id'

  # methods
  get_json_field = validation.get_json_field

  def get_select_all_query(self):
    return f"SELECT scale_id as id, scale_value as scale FROM {self.table_name};"


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (scale_value, created_date, updated_date, user_update_id)"
      "VALUES (%(scale)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);"
    )


  def get_sql_vals(self, scale):
    return {
      'scale'   :  scale,
      'user_id' :  self.db.user_id,
    }


  def select(self):
    db_results =  self.db.execute_sql(
      self.db.process_select_results,
      self.get_select_all_query())
    results =  self.utils.db_data_to_json(db_results)

    return results


  def insert(self, request):
    model_scale =  self.get_json_field('model_scale', request.json)

    res = self.db.execute_sql(
      self.db.process_insert_results,
      self.get_insert_query(),
      self.get_sql_vals(model_scale), )

    logger.debug('completed insert', extra=res)
    return


  def update(self, request):
    scale_id      =  self.get_json_field('id', request.json)
    update_fields =  {
      'scale_value' :  self.get_json_field('scale_value',request.json),
    }
    db_results =  self.db.execute_sql(
      self.db.process_update_results,
      self.db.get_update_query(self.table_name, update_fields, self.table_id),
      self.utils.append_fields_to_json(update_fields, scale_id=scale_id),
    )

    logger.debug('completed update', extra=db_results)
    return


