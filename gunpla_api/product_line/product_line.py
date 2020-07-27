from gunpla_api.db_connector import DbConnector


class ProductLine():
  db = DbConnector()


  def get_insert_query(self):
    return (
      'INSERT INTO product_lines (access_name, display_name, short_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )


  def get_sql_vals(self, display_name, access_name, short_name):
    vals            =  locals()
    vals['user_id'] =  self.db.user_id
    return vals


  def get_update_query(self, product_line_id, update_fields):
    query  =  "UPDATE product_lines"
    query +=  self.db.generate_update_set_query(update_fields)
    query +=  "WHERE product_line_id = %(product_line_id)s;"
    return query
