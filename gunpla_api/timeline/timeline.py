from gunpla_api.db_connector import DbConnector


class Timeline():
  db = DbConnector()
  table_name =  'timelines'
  table_id   =  'timeline_id'

  def get_insert_query(self):
    return self.db.get_standard_insert_query({self.table_name})


  def get_select_all_query(self):
    return f"SELECT timeline_id, access_name, display_name FROM {self.table_name}"


  def get_sql_vals(self, display_name, access_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals



