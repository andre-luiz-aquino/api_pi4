from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec
from sqlalchemy import create_engine, text
import configparser
import os

# Criar um objeto ConfigParser
config = configparser.ConfigParser()

# Ler o arquivo
config.read(os.path.join('api_pi', 'config.ini'))


# Acessar os valores
host = config['BancoDeDados']['host']
porta = config['BancoDeDados']['porta']
usuario = config['BancoDeDados']['usuario']
senha = config['BancoDeDados']['senha']
banco = config['BancoDeDados']['banco']

# # Construir a string de conexão
db_url = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"


# Criar uma conexão com o banco de dados
engine = create_engine(db_url)


app = Flask(__name__)
spec = FlaskPydanticSpec('Flask',title='Api Clima Bom')
spec.register(app)

# Rota para buscar todos os registros de uma tabela
@app.route('/buscar_registros', methods=['GET'])
def buscar_registros():
    try:
        # Abrir uma conexão
        with engine.connect() as connection:
            # Exemplo: executar uma consulta SQL
            query = text("SELECT * FROM sua_tabela;")
            results = connection.execute(query)

            # Transformar os resultados em uma lista de dicionários
            registros = [{'id': row.id, 'campo1': row.campo1, 'campo2': row.campo2} for row in results]

            # Retornar os resultados em formato JSON
            return jsonify({'registros': registros})

    except Exception as e:
        return jsonify({'erro': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
