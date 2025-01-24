from flask import Flask
from api.consulta_navio import consulta_navio
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(consulta_navio)

if __name__ == '__main__':
    app.run(debug=True, port=app.config['PORT'])
