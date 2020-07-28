import json
from flask              import Blueprint, Response, request

from gunpla_api.config  import Config
from gunpla_api.logger  import Logger

# from gunpla_api.utils   import Utils
from gunpla_api.controller  import Controller
from gunpla_api.validation  import Validation
from gunpla_api.exceptions  import BadRequestException, DatabaseException, DatabaseUniqueException

logger  =  Logger().get_logger()
private =  Blueprint(
  'private',
  __name__,
  url_prefix='/api/private',
)

CONFIG =  Config()
CONTROLLER =  Controller()
VALIDATION =  Validation()
# UTILS  =  Utils()

# MAIN_CONTROLLER   =  MainController()


@private.route('/lifecheck',  methods=['GET'])
@private.route('/lifecheck/', methods=['GET', 'POST'])
def lifecheck():
  # MAIN_CONTROLLER.handle_auth(app.current_request)
  # print('request json: ', request.json)
  app_name     =  CONFIG.app_name
  logging_json =  { 'app_name': app_name }
  logger.info(logging_json)
    # if multiple qs for 'search'- params = request.args.getlist('search')
    # have request as dict = request.args.to_dict()
  return Response(
    response =  json.dumps({
      'appName' :  app_name,
      'stage'   :  CONFIG.stage,
      'path'    :  '/private/lifecheck',
      'status'  :  200,
    })
  )


@private.route('/<table>',  methods=['POST'])
@private.route('/<table>/', methods=['POST'])
def insert_route(table):

  logger.info(f'request received - insert to table: {table}')
  try:
    CONTROLLER.direct_insert_request(table, request)
    response = Response(status=200, response=json.dumps({'message': 'success'}))

  except BadRequestException:
    response = Response(status=400, response=json.dumps({'message': 'error'}))
  except DatabaseUniqueException:
    response = Response(status=400, response=json.dumps({'message': 'bad request'}))
  except DatabaseException:
    response = Response(status=500, response=json.dumps({'message': 'error'}))
  except Exception as e:
    logger.exception('unknown error occured')
    response = Response(status=400, response=json.dumps({'message': 'error'}))

  logger.info('request complete')
  return response


@private.route('/<table>',  methods=['PUT'])
@private.route('/<table>/', methods=['PUT'])
def update_route(table):

  logger.info(f'request received - update to table: {table}')
  try:
    CONTROLLER.direct_update_request(table, request)
    response = Response(status=200, response=json.dumps({'message': 'success'}))

  except BadRequestException as e:
    response = Response(status=400, response=json.dumps({'message': f'error, {e}'}))
  except DatabaseUniqueException:
    response = Response(status=400, response=json.dumps({'message': 'bad request'}))
  except DatabaseException:
    response = Response(status=500, response=json.dumps({'message': 'error'}))
  except Exception as e:
    logger.exception('unknown error occured')
    response = Response(status=400, response=json.dumps({'message': 'error'}))

  logger.info('request complete')
  return response


@private.route('/<table>/<_id>',  methods=['DELETE'])
@private.route('/<table>/<_id>/', methods=['DELETE'])
def delete_route(table, _id):

  logger.info(f'request received - delete from table: {table}, id: {_id}')
  try:
    CONTROLLER.process_delete_request(table, _id)
    response = Response(status=200, response=json.dumps({'message': 'success'}))

  except BadRequestException as e:
    response = Response(status=400, response=json.dumps({'message': f'error, {e}'}))
  except DatabaseUniqueException:
    response = Response(status=400, response=json.dumps({'message': 'bad request'}))
  except DatabaseException:
    response = Response(status=500, response=json.dumps({'message': 'error'}))
  except Exception as e:
    logger.exception('unknown error occured')
    response = Response(status=400, response=json.dumps({'message': 'error'}))

  logger.info('request complete')
  return response


