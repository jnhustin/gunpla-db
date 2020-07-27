from gunpla_api.db_connector import DbConnector


class ModelScale():
  db = DbConnector()


  def get_insert_query(self):
    return (
      'INSERT INTO scales (scale_value, created_date, updated_date, user_update_id)'
      'VALUES (%(scale)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )


  def get_sql_vals(self, scale):
    return {
      'scale'   :  scale,
      'user_id' :  self.db.user_id,
    }

