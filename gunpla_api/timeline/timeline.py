from gunpla_api.db_connector import DbConnector


class Timeline():
  db = DbConnector()


  def get_insert_query(self):
    return self.db.get_standard_insert_query('timelines')


  def get_sql_vals(self, timeline_id, access_name, display_name):
    json_data       =  self.db.get_standard_sql_vals(access_name, display_name)
    json_data['id'] =  timeline_id
    return json_data

  def get_select_all_query(self):
    return 'SELECT timeline_id, access_name, display_name FROM timelines'


  def get_update_query(self, id, access_name, display_name):
    query  = """
      UPDATE timelines
      SET access_name = %(access_name)s,
        display_name = %(display_name)s
      WHERE timeline_id = %(id)s;
    """
    return query

