from gunpla_api.db_connector import DbConnector


class ProductLine():
  db         =  DbConnector()
  table_name =  'product_lines'
  table_id   =  'product_line_id'


  def get_insert_query(self):
    return (
      f"INSERT INTO {self.table_name} (access_name, display_name, short_name, created_date, updated_date, user_update_id)"
      "VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);"
    )


  def get_sql_vals(self, display_name, access_name, short_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals

