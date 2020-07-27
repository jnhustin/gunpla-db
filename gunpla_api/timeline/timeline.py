from gunpla_api.db_connector import DbConnector


class Timeline():
  db = DbConnector()


  def get_insert_query(self):
    return self.db.get_standard_insert_query('timelines')


  def get_select_all_query(self):
    return 'SELECT timeline_id, access_name, display_name FROM timelines'


  def get_sql_vals(self, display_name, access_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals


  def get_update_query(self, timeline_id, update_fields):
    query  =  "UPDATE timelines"
    query +=  self.db.generate_update_set_query(update_fields)
    query +=  "WHERE timeline_id = %(timeline_id)s;"
    return query


