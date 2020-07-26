from gunpla_api.db_connector import DbConnector


class ProductLine():
  db = DbConnector()


  def get_insert_query(self):
    return (
      'INSERT INTO product_lines (access_name, display_name, short_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )

  def get_insert_param_dict(self, access_name, display_name, short_name):
    json_data = self.db.get_standard_insert_vals(access_name, display_name)
    json_data['short_name'] = short_name
    return json_data

