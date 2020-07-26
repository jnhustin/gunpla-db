from gunpla_api.db_connector import DbConnector


class ProductLine():
  db = DbConnector()


  def get_insert_query(self):
    return (
      'INSERT INTO product_lines (access_name, display_name, short_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, %(short_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )

  def get_sql_vals(self, timeline_id, access_name, display_name, short_name):
    json_data = self.db.get_standard_insert_vals(access_name, display_name)
    json_data['short_name'] =  short_name
    json_data['id']         =  timeline_id
    return json_data


  def get_update_query(self, id, access_name=None, display_name=None, short_name=None):
    # TODO - try this with kwargs
    query = """ UPDATE product_lines SET """

    if short_name:
      query += "short_name = %(short_name)s"

    if short_name and display_name:
      query += ","

    if display_name:
      query += """
        access_name = %(access_name)s,
        display_name = %(display_name)s
      """
    query += "WHERE product_line_id = %(id)s;"

    return query
