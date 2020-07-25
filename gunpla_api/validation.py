from gunpla_api.exceptions import BadRequestException
from gunpla_api.logger import Logger

logger  =  Logger().get_logger()


class Validation():


  def get_field(self, field, json):
    try:
      return json[field]
    except:
      logger.exception('[get_field] error')
      raise BadRequestException
