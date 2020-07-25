


class Utils():


  def convert_to_snake_case(self, string):
    return string.replace(' ', '_')


  def db_data_to_dict(self, db_results):
    """ sample structyre of db_results
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
    for row in rows:
      row_data = { columns[i]: val for i, val in enumerate(row) }
      results.append(row_data)

    return results