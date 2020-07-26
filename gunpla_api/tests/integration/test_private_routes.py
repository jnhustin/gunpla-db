import json
import unittest
import requests

from gunpla_api.db_connector import DbConnector
from gunpla_api.app import create_app


# python -m unittest gunpla_api.tests.integration.test_private_routes.TestPrivateRoutes
class TestPrivateRoutes(unittest.TestCase):
  def setUp(self):
    self.db     =  DbConnector()
    self.app    =  create_app()
    self.client =  self.app.test_client

  """ client.post response

    res:  {
      'headers': Headers([('Content-Type', 'text/html; charset=utf-8'),
      ('Content-Length', '26')]),
      '_status': '400 BAD REQUEST',
      '_status_code': 400,
      'direct_passthrough': False,
      '_on_close': [],
      'response': <werkzeug.wsgi.ClosingIterator object at 0x111afee90>}
  """
  # python -m unittest gunpla_api.tests.integration.test_private_routes.TestPrivateRoutes.test_insert_timeline
  def test_insert_timeline(self):
    test_url = '/api/private/insert/timeline/'
    test_cases = [
      {
        'access_name'          :  'foo_bar',
        'display_name'         :  'foo bar',
        'assert_status_code'   :  200,
      },
    ]

    for test in test_cases:
      access_name =  test['access_name']
      json_data   =  {
        'access_name'  :  access_name,
        'display_name' :  test['display_name'],
      }
      assert_status_code   =  test.get('assert_status_code')

      try:
        with self.client():
          post_res = self.client().post(test_url, json=json_data)
        self.assertEqual(post_res.status_code, assert_status_code)
      finally:

        # verify & delete entry
        self.db.execute_sql(self.db.process_delete_results, f"DELETE FROM timelines WHERE access_name='{access_name}'")

