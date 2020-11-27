from flask import Flask

app = Flask(__name__)

# Flask will always be in production ENV unless explicitly set
if app.config['ENV'] == 'production':
    app.config.from_object('app_config.ProdConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('app_config.TestConfig')
else:
    app.config.from_object('app_config.DevConfig')

from app import views
