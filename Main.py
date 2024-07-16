from flask import Flask, request
from flask_basicauth import BasicAuth
from Services import Service
from Mapped import Components as cp

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = cp.USUARIO_AUTH
app.config['BASIC_AUTH_PASSWORD'] = cp.PASSWORD_AUTH

basic_auth = BasicAuth(app)


@app.route('/registra-ponto', methods=['POST'])
@basic_auth.required
def sua_funcao():
    json = request.json
    resultado = Service.do_registration(json)
    if resultado['Sucesso']:
        return resultado, 200
    else:
        return resultado, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
