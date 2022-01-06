from flask import Flask
from app.messages.blueprints.message_blueprint import message_blueprint
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__, static_folder='common/static',
            template_folder='common/templates')
app.register_blueprint(message_blueprint)


def run():
    app.run(host=os.environ.get('HOST', '0.0.0.0'),
            port=os.environ.get('PORT', 5000),
            debug=bool(os.environ.get('DEBUG', '1')))
