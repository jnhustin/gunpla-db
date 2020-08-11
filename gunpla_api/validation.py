from gunpla_api.exceptions import BadRequestException
from gunpla_api.logger import Logger

logger  =  Logger().get_logger()


class Validation():


  def get_json_field(self, field, json, optional=False):
    try:
      return json.get(field) if optional else json[field]
    except:
      logger.exception('[get_json_field] error')
      raise BadRequestException(f'missing field: {field}')


  def get_query_param(self, field, params, optional=False):
    try:
      return params.get(field) if optional else params[field]
    except:
      logger.exception('[get_query_param] error')
      raise BadRequestException(f'missing required field: "{field}"')



