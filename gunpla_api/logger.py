import logging
from pythonjsonlogger import jsonlogger
from gunpla_api.singleton import Singleton


@Singleton
class Logger:
  def __init__(self):
    self.l =  None


  def get_logger(self):
    if not self.l:
      self.l = self.start_logger()
    return self.l


  def start_logger(self):
    # configure logging
    formatter  = jsonlogger.JsonFormatter('(message), (module), (funcName), (levelname), (asctime), (process)')
    logger     = logging.getLogger(__name__)
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # change log lvls here  ['INFO', 'DEBUG']
    logger.setLevel(logging.DEBUG)

    # Disable flask logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    return logger
