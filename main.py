 
#########################
# Author ms0xz          # 
# github.com/ms0xz/Mino #
# Free use              #
# -*- coding: utf-8 -*- #
#                       #
#########################
##LANGUAGE SELECT, if you want to change the laguage you only change the import
##For example, i want to change to English i change "import es_ES as lang" to "import en_EN as lang"

##FOR PYTHON3 use pip3
from flask import Flask, flash, render_template, json, request, url_for, redirect, jsonify, session
from flask_bcrypt import Bcrypt, check_password_hash
from flask_caching import Cache
from langs import es_ES as lang
import configuration
import MySQLdb
from flask_bcrypt import Bcrypt, check_password_hash
cur = MySQLdb.connect(host=configuration.mySQL['host'], user=configuration.mySQL['user'], passwd=configuration.mySQL['password'], db=configuration.mySQL['database'])
Environment = Flask(__name__, template_folder="views", static_folder="assets")
Environment.config['SECRET_KEY'] = 'ms0xz'
bcrypt = Bcrypt(Environment)
cache = Cache(config={'CACHE_TYPE': 'simple'})

@Environment.route('/')
def render_index():

	if session.get('logged'):
		return redirect(url_for('render_dashboard'))
	else:
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
def render_signUp():
	if session.get('logged'):
		return redirect(url_for('render_dashboard'))
	else:
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
@cache.cached(timeout=5)
@Environment.route('/dashboard')
def render_dashboard():
	if session.get('logged'):
		login.user = session.get('username')
		cursor = cur.cursor()
		cursor.execute(''' SELECT * FROM users WHERE username =%s ''', (login.user, ))
		data = cursor.fetchall()
		_id = data[0][0]
		_username = data[0][1]
		_mail = data[0][3]	
		_motto = data[0][12]
		return render_template('dashboard.html', id = _id, username = _username, mail = _mail, motto = _motto)

	else:

		return redirect(url_for('render_index'))

@Environment.route('/checkUser', methods=['POST'])
def signin():
	
		return login()

		

@Environment.route('/generatingData',methods=['POST'])
def register():

		return register()

		

##FUNCTIONS		
def login():
	if request.method == "POST":
		user = request.form["username"]
		passw = request.form["password"]

		cursor = cur.cursor()
		cursor.execute('''SELECT * FROM users WHERE username =%s''', (user, ))
		check = cursor.fetchall()
		
		if bcrypt.check_password_hash(str(check[0][2]), passw) and user == check[0][1]:
			session['logged'] = True
			session['username'] = user
			return jsonify(dict(redirect='/dashboard'))
		
			cursor.close()
			cur.close()


def register():
	username = request.form["username"]
	password = request.form["password"]
	mail = request.form["mail"]
			
	if username and password and mail:
		cursor = cur.cursor()
		cursor.execute('''SELECT username FROM users WHERE username =%s OR mail=%s''', (username,mail, ))

		check = cursor.fetchall()
		if(len(check) > 0):
			return 'El nombre de usuario o correo ya esta ocupado'

				##FOR PYTHON 3 USE password_hash = bcrypt.generate_password_hash(_password).decode('utf8-8')
		password_hash = bcrypt.generate_password_hash(password)
		cursor.execute('''INSERT INTO users(username, password, mail) VALUES(%s,%s,%s)''',(username, password_hash, mail))
		data = cursor.fetchall()
			
		if len(data) is 0:
			cur.commit()
			return jsonify(dict(redirect='/'))
	
		else:
			return 'Error'


		

		cursor.close()
		cur.close()
		
@Environment.route('/session/destroy')
def logout():
	session.pop('username', None)
	session.pop('logged', None)
	return redirect(url_for('render_index'))


if __name__ == "__main__":
	print("M I N O")
	Environment.run(port=8080, debug=True)
