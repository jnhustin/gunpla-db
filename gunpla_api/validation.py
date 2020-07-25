from gunpla_api.exceptions import BadRequestException
from gunpla_api.logger import Logger

logger  =  Logger().get_logger()


class Validation():


  def get_json_field(self, field, json):
    try:
      return json[field]
    except:
      logger.exception('[get_json_field] error')
      raise BadRequestException
