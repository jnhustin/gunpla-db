""" POSTGRESQL DB class """
import psycopg2
from dotenv  import load_dotenv
from os.path import join, dirname

from gunpla_api.config      import Config
from gunpla_api.logger      import Logger
from gunpla_api.utils       import Utils
from gunpla_api.exceptions  import DatabaseUniqueException, BadRequestException

logger = Logger().get_logger()

class DbConnector():
  config   =  Config()
  host     =  config.db_host
  port     =  config.db_port
  user     =  config.db_user
  password =  config.db_password
  db_name  =  config.db_name

  user_id = 1


  def __init__(self):
    self.initialize_conn()


  def initialize_conn(self):
    self.conn =  psycopg2.connect(
      host     =  self.host,
      port     =  self.port,
      user     =  self.user,
      password =  self.password,
      dbname   =  self.db_name, )
    return


  def get_conn(self):
    try:
      if self.conn == None or self.conn.closed == 1:
        logger.debug('conn down, reinitializing')
        self.initialize_conn()
      else:
        return self.conn

    except Exception:
      logger.exception('db_connector.get_conn error')
      raise


  def execute_sql(self, function, sql, vals=None, is_close_conn=True):
    try:
      self.get_conn()
      cursor =  self.conn.cursor()
      cursor.execute(sql, vals)
      result = function(cursor)
    except psycopg2.errors.UniqueViolation:
      logger.exception('db_connector unique constraint violation', extra={'sql': sql, 'vals': vals})
      self.rollback()
      raise DatabaseUniqueException()
    except psycopg2.Error as e:
      logger.exception('some psycopg error', extra={'sql': sql, 'vals': vals, 'pg_code': e.pgcode})
      self.rollback()
      raise
    except Exception as e:
      logger.exception('unknown database execution error', extra={'sql': sql, 'vals': vals, 'error': str(e)})
      self.rollback()
      raise

    if is_close_conn:
      self.conn.commit()
      self.conn.close()

    return result


  def commit_sql(self, cursor=None):
    try:
      self.conn.commit()
      self.conn.close()
      return
    except:
      print('bruh, already done')


  def process_insert_results(self, cursor):
    status_message =  cursor.statusmessage

    return { 'status_message' :  status_message, }


  def process_update_results(self, cursor) :
    status_message =  cursor.statusmessage

    if status_message == 'UPDATE 0':
      raise BadRequestException('id does not exist')

    return { 'status_message' :  status_message, }


  def process_select_results(self, cursor) :
    status_message =  cursor.statusmessage
    col_names      =  [ desc[0] for desc in cursor.description ]
    results        =  cursor.fetchall()
    return {
      'status_message' :  status_message,
      'results'        :  results,
      'col_names'      :  col_names,
    }


  def process_delete_results(self, cursor) :
    status_message =  cursor.statusmessage
    return { 'status_message': status_message, }


  def rollback(self) :
    self.conn.rollback()
    self.conn.close()
    return


  def get_standard_insert_query(self, table):
    return (
      f'INSERT INTO {table} (access_name, display_name, created_date, updated_date, user_update_id)'
      'VALUES (%(access_name)s, %(display_name)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s);'
    )


  def get_update_query(self, table_name, update_fields, table_id):
    query  =  f"UPDATE {table_name}"
    query +=  self.generate_update_set_query(update_fields)
    query +=  f"WHERE {table_id} = %({table_id})s;"
    return query


  def generate_update_set_query(self, update_fields: dict):
    query  =  " SET "
    query +=  ",".join( [ f"{col} = %({col})s" for col, val in update_fields.items() if val != None ] )
    query +=  f", user_update_id = {self.user_id}, updated_date='NOW' "
    return query


  def get_delete_query(self, table_name, table_id):
    return f"DELETE FROM {table_name} WHERE {table_id} = %(_id)s"
