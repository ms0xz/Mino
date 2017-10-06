 
#########################
# Author ms0xz          # 
# github.com/ms0xz/Mino #
# Free use              #
# -*- coding: utf-8 -*- #
#                       #
#########################


##FOR PYTHON3 use pip3
from flask import Flask, render_template, json, request, url_for, redirect, jsonify, session
import jinja2
import MySQLdb
import configuration
from flask_bcrypt import Bcrypt, check_password_hash
from langs import es_ES as lang
##LANGUAGE SELECT, if you want to change the laguage you only change the import
##For example, i want to change to English i change "import es_ES as lang" to "import_en_EN as lang"

cur = MySQLdb.connect(host=configuration.mySQL['host'], user=configuration.mySQL['user'], passwd=configuration.mySQL['password'], db=configuration.mySQL['database'])
Environment = Flask(__name__, template_folder="views", static_folder="assets")
Environment.config['SECRET_KEY'] = 'ms0xz'
bcrypt = Bcrypt(Environment)

print("M I N O")
@Environment.route('/')
def index():

	return render_template('index.html',
		title = lang.index_title,
		slogan = lang.index_slogan,
		description = lang.index_description,
		label_username = lang.index_label_username,
		input_username = lang.index_input_username,
		label_password = lang.index_label_password,
		input_password = lang.index_input_password,
		button_submit = lang.index_submit_button
		)
		
@Environment.route('/signup')
def signUp():
	return render_template('register.html',
		title = lang.register_title,
		slogan = lang.register_slogan,
		description = lang.register_description,
		label_username = lang.register_label_username,
		label_password = lang.register_label_password,
		label_mail = lang.register_label_mail,
		input_username = lang.register_input_username,
		input_password = lang.register_input_password,
		input_mail = lang.register_input_mail,
		button_submit = lang.register_button_submit

		)

@Environment.route('/dashboard')
def dashboard():
	if session.get('logged'):
		return render_template('dashboard.html')
	else:

		return json.dumps({'error': 'Error al iniciar sesion, intentelo de nuevo'})


@Environment.route('/checkUser', methods=['POST', 'GET'])
def signin():
	
	if request.method == "POST":
		user = request.form["username"]
		passw = request.form["password"]

		cursor = cur.cursor()
		cursor.execute('''SELECT * FROM users WHERE username =%s''', (user, ))
		check = cursor.fetchall()
		
		if bcrypt.check_password_hash(str(check[0][2]), passw) and user == check[0][1]:
			session['logged'] = True
			return jsonify(dict(redirect='/dashboard'))
		
			


			cursor.close()
			cur.close()

@Environment.route('/generatingData',methods=['POST','GET'])
def register():

		try:
			username = request.form["username"]
			password = request.form["password"]
			mail = request.form["mail"]
			

			if username and password and mail:
				cursor = cur.cursor()

				
				##VERIFICATION USER EXITS

				cursor.execute('''SELECT username FROM users WHERE username =%s OR mail=%s''', (username,mail, ))

				check = cursor.fetchall()
				if(len(check) > 0):
					return json.dumps({'message:' :'El nombre de usuario o correo ya esta ocupado'})

				##FOR PYTHON 3 USE password_hash = bcrypt.generate_password_hash(_password).decode('utf8-8')
				password_hash = bcrypt.generate_password_hash(password)

				cursor.execute('''INSERT INTO users(username, password, mail) VALUES(%s,%s,%s)''',(username, password_hash, mail))
				data = cursor.fetchall()
			


				if len(data) is 0:
					cur.commit()
					return jsonify(dict(redirect='/'))

			
				else:
					return json.dumps({'error':str(data[0])})


			else:
				return json.dumps({'html': 'No dejes espacios en blanco'})

		except Exception as e:
			return json.dumps({'error': str(e)})

			cursor.close()
			cur.close()


@Environment.route('/destroy', methods=['POST'])
def logout():
	if request.method == 'POST':
		session.pop('logged', None)
		return jsonify(dict(redirect='/'))




if __name__ == "__main__":
	Environment.run(port=8080, debug=True)
