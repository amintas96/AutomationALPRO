from flask import Flask, request, jsonify
from Services import Service
app = Flask(__name__)

@app.route('/registra-ponto', methods=['POST'])
def sua_funcao():
    
    json = request.json
    resultado = Service.do_registration(json)

    if resultado['Sucesso']:
        return resultado, 200
    else: 
        return resultado, 400



if __name__ == '__main__':
    app.run(debug=True)
