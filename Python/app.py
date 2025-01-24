from flask import Flask
from api.consulta_navio import consulta_navio

app = Flask(__name__)

app.register_blueprint(consulta_navio)

if __name__ == '__main__':
    app.run(debug=True)
