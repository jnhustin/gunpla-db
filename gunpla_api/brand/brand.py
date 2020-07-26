from gunpla_api.db_connector import DbConnector


class Brand():
  db = DbConnector()


  def get_insert_query(self):
    return self.db.get_standard_insert_query('brands')


  def get_insert_param_dict(self, access_name, display_name):
    return self.db.get_standard_insert_vals(access_name, display_name)

