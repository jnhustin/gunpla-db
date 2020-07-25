from gunpla_api.config import Config
from gunpla_api.db_connector import DbConnector
from gunpla_api.exceptions import DatabaseException


class GunplaDb:
  db      =  DbConnector()
  user_id =  1

  def insert_model(self):
    pass


  def get_standard_insert_query(self, table):
    return (
      f'INSERT INTO {table} (access_name, display_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )


  def get_standard_insert_vals(access_name, display_name):
    return {
      'access_name'  :  access_name,
      'display_name' :  display_name,
      'user_id'      :  self.user_id,
    }


  def insert_timeline(self, access_name, display_name):
    query  =  self.get_standard_insert_query('timelines')
    values =  self.get_standard_insert_vals(access_name, display_name)

    res =  self.db.execute_sql(self.db.process_insert_results, query, values)
    logger.debug('completed insert', extra=res)
    return


  def insert_model_scale(self, scale):
    query = (
      'INSERT INTO scales (scale_value, created_date, updated_date, user_update_id)'
      'VALUES (%(scale)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )
    values = {
      'scale'   :  scale,
      'user_id' :  self.user_id
    }

    res =  self.db.execute_sql(self.db.process_insert_results, query, values)
    logger.debug('completed insert', extra=res)
    return


  def insert_product_line(self, access_name, display_name, short_name):
    query = (
      'INSERT INTO product_lines (access_name, display_name, short_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )
    values = get_standard_insert_vals(access_name, display_name)
    values['short_name'] = short_name

    res =  self.db.execute_sql(self.db.process_insert_results, query, values)
    logger.debug('completed insert', extra=res)
    return


  def insert_brand(self, access_name, display_name):
    query  =  self.get_standard_insert_query('brands')
    values =  self.get_standard_insert_vals(access_name, display_name)

    res    =  self.db.execute_sql(self.db.process_insert_results, query, values)
    logger.debug('completed insert', extra=res)
    return

  def insert_franchise(self, access_name, display_name):
    query  =  self.get_standard_insert_query('franchises')
    values =  self.get_standard_insert_vals(access_name, display_name)

    res    =  self.db.execute_sql(self.db.process_insert_results, query, values)
    logger.debug('completed insert', extra=res)
    return
