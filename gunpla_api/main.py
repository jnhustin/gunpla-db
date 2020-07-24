import json
from flask              import Blueprint, Response, request
from gunpla_api.config  import Config
from gunpla_api.logger  import Logger
# from gunpla_api.utils   import Utils

logger  =  Logger().get_logger()
main =  Blueprint(
  'main',
  __name__,
  url_prefix='/api/main',
)

CONFIG =  Config()
# UTILS  =  Utils()

# MAIN_CONTROLLER   =  MainController()


@main.route('/lifecheck',  methods=['GET'])
@main.route('/lifecheck/', methods=['GET', 'POST'])
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
      'path'    :  '/main/lifecheck',
      'status'  :  200,
    })
  )
