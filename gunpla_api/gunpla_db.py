from gunpla_api.config import Config
from gunpla_api.db_connector import DbConnector
from gunpla_api.exceptions import DatabaseException


class GunplaDb:
  db      =  DbConnector()
  user_id =  1

  def insert_model(self):
    pass


  def insert_timeline(self, timeline):
    query = (
      'INSERT INTO timelines (timeline_name, created_date, updated_date, user_update_id)'
      'VALUES (%(timeline)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )
    values = {
      'timeline' :  timeline,
      'user_id'  :  self.user_id
    }
    try:
      res = self.db.execute_sql(self.db.process_insert_results, query, values)
      return
    except Exception as e:
      logger.exception('insert_timeline exception')
      raise DatabaseException()


  def insert_model_scale(self, scale):
    query = (
      'INSERT INTO scales (scale_value, created_date, updated_date, user_update_id)'
      'VALUES (%(scale)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )
    values = {
      'scale'   :  scale,
      'user_id' :  self.user_id
    }

    res = self.db.execute_sql(self.db.process_insert_results, query, values)
    return

