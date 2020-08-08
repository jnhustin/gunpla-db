import datetime


class Utils():


  def convert_to_snake_case(self, string):
    return string.replace(' ', '_')


  def db_data_to_json(self, db_results):
    """ sample structure of db_results
      {
        'status_message' :  'SELECT 3',
        'col_names'      :  ['timeline_id', 'access_name', 'display_name'],
        'results'        :  [
          (1, 'after_colony', 'after colony'),
          (2, 'universal_century', 'universal century'),
        ],
      }
    """

    """ sample return
      [
        {
          'timeline_id'  :  1,
          'access_name'  :  'after_colony',
          'display_name' :  'after colony'
        },
        {
          'timeline_id' :  2,
          'access_name' :
          'universal_century',
          'display_name' :  'universal century'
        },
      ]
    """

    columns =  db_results['col_names']
    rows    =  db_results['results']

    results = []
    # build 1 row at a time
    for row in rows:

      # for each row, convert cols to key and their corresponding val to dict[key] val
      json_row = {}
      for i, val in enumerate(row):
        is_datetime_obj = type(val) == datetime.date
        json_row[columns[i]] = self.get_date_str(val) if is_datetime_obj else val
      results.append(json_row)

    return results


  def append_fields_to_json(self, json_data, **kwargs):
    for k,v in kwargs.items():
      json_data[k] = v
    return json_data


  def get_date_str(self, date, format='%Y-%m-%d'):
    return date.strftime(format)


  def remove_empty_json_keys(self, json_data):
    adjusted_json = {}
    for k, v in json_data.items():
      if type(v) == list and len(v) == 0:
        continue
      elif v == None:
        continue

      adjusted_json[k] = v
    return adjusted_json
