from flask import Flask, jsonify, request
import mysql.connector

import os

application = app = Flask(__name__)

class DBHandler:
	def __init__(self):
		user = os.environ["TCC_AWS_USER"]
		host = os.environ["TCC_AWS_HOST"]
		passwd = os.environ["TCC_AWS_PASSWORD"]
		db_name = os.environ["TCC_AWS_DB_NAME"]

		# query_insert_cmd = """INSERT INTO teste_tcc(cmd_id, cmd_name, cmd_result, timestamp)
		# VALUES (321, 'hello_world', '-1', NOW());"""
		self.query_insert_cmd = """INSERT INTO teste_tcc(cmd_id, cmd_name, cmd_result, timestamp)
		VALUES (%s, '%s', %s, NOW());"""
		self.query_select = "SELECT * FROM teste_tcc"


		# Conexão com o banco de dados MySQL
		self.cnx = mysql.connector.connect(user=user, password=passwd, host=host, database=db_name)

		# Executa uma consulta
		self.cursor = self.cnx.cursor()

		# # Fecha a conexão com o banco de dados MySQL
		# cursor.close()
		# cnx.close()

	def add_cmd_data_to_db(self, cmd_id, cmd_name, cmd_result):
		query_to_execute = self.query_insert_cmd % (cmd_id, cmd_name, cmd_result)
		self.cursor.execute(query_to_execute)
		self.cnx.commit()

	def get_all_data_from_db(self):
		self.cursor.execute(self.query_select)

		# Retorna os resultados em formato JSON
		data = self.cursor.fetchall()
		result = []
		for row in data:
			# print(row)
			result.append(row)

		return result

@app.route('/')
def home():
	return 'API is up and running!'

@app.route('/getAllData')
def connect_to_db():
	db_handler = DBHandler()
	data = db_handler.get_all_data_from_db()

	return jsonify(data)

@app.route('/addData', methods = ['POST'])
def add_cmd_results():
	db_handler = DBHandler()

	# request_params = request.get_json()
	cmd_id = request.args['cmd_id']
	cmd_name = request.args['cmd_name']
	cmd_result = request.args['cmd_result']

	try:
		db_handler.add_cmd_data_to_db(cmd_id, cmd_name, cmd_result)
	except:
		return "unexpected error"

	return "success"

if __name__ == '__main__':
	app.run(debug=True, port=80)