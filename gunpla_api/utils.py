


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

    results = [ { columns[i]: val for i, val in enumerate(row) } for row in rows ]
    return results


  def append_fields_to_json(self, json_data, **kwargs):
    for k,v in kwargs.items():
      json_data[k] = v
    return json_data
