from gunpla_api.exceptions import BadRequestException


class Validation():


  def get_field(self, field, json):
    try:
      return json[field]
    except:
      raise BadRequestException
