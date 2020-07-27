from gunpla_api.db_connector import DbConnector


class Brand():
  db = DbConnector()


  def get_insert_query(self):
    return self.db.get_standard_insert_query('brands')


  def get_sql_vals(self, access_name, display_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals
