from gunpla_api.exceptions import BadRequestException
from gunpla_api.logger import Logger

logger  =  Logger().get_logger()


class Validation():


  def get_json_field(self, field, json, optional=False):
    if optional:
      return json.get(field)
    try:
      return json[field]
    except:
      logger.exception('[get_json_field] error')
      raise BadRequestException(f'missing field: {field}')


  def get_query_param(self, field, params):
    try:
      return params[field]
    except:
      logger.exception('[get_query_param] error')
      raise BadRequestException


