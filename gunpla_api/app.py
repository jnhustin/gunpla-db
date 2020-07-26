from flask import Flask

from gunpla_api.config import Config


# add app extensions
# cors, etc


# instantiate, initialize & configure App
# http://flask.pocoo.org/docs/0.12/patterns/appfactories/
def create_app(config_class=Config):

  # CONFIGURATION
  # http://flask.pocoo.org/docs/1.0/config/#configuration-basics
  app = Flask(__name__)
  app.config.from_object(Config)


  # EXTENSIONS
  # bind app to extensions
  # http://flask.pocoo.org/docs/1.0/extensiondev/#the-extension-code


  # REGISTER BLUEPRINTS
  from gunpla_api.private_routes import private
  from gunpla_api.public_routes import public

  app.register_blueprint(private)
  app.register_blueprint(public)



  return app



