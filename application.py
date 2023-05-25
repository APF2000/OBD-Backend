from flask import Flask, jsonify, request
import mysql.connector

import os

application = app = Flask(__name__)

@app.route('/')
def home():
    return 'API is up and running!'

@app.route('/getAllData')
def connect_to_db():
	cursor.execute(query_select)

	# Retorna os resultados em formato JSON
	data = cursor.fetchall()
	result = []
	for row in data:
		# print(row)
		result.append(row)

	return jsonify(result)

@app.route('/addData', methods = ['POST'])
def add_cmd_results():
	# request_params = request.get_json()
	cmd_id = request.args['cmd_id']
	cmd_name = request.args['cmd_name']
	cmd_result = request.args['cmd_result']

	query_to_execute = query_insert_cmd % (cmd_id, cmd_name, cmd_result)
	cursor.execute(query_to_execute)
	cnx.commit()
	return "success"

if __name__ == '__main__':
	app.run(debug=True, port=80)

	host = os.environ["TCC_AWS_HOST"]
	user = os.environ["TCC_AWS_USER"]
	passwd = os.environ["TCC_AWS_PASSWORD"]
	db_name = os.environ["TCC_AWS_DB_NAME"]

	# query_insert_cmd = """INSERT INTO teste_tcc(cmd_id, cmd_name, cmd_result, timestamp)
	# VALUES (321, 'hello_world', '-1', NOW());"""
	query_insert_cmd = """INSERT INTO teste_tcc(cmd_id, cmd_name, cmd_result, timestamp)
	VALUES (%s, '%s', %s, NOW());"""
	query_select = "SELECT * FROM teste_tcc"


	# Conexão com o banco de dados MySQL
	cnx = mysql.connector.connect(user=user, password=passwd, host=host, database=db_name)

	# Executa uma consulta
	cursor = cnx.cursor()

	# Fecha a conexão com o banco de dados MySQL
	cursor.close()
	cnx.close()