# encoding: utf-8
from flask import Response, Flask, render_template, request, jsonify, redirect, url_for, session, json, flash, make_response, send_file
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import os
from datetime import datetime
import sys

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

# Create the Flask object for the application
app = Flask(__name__)
app.secret_key = 'ckpZQrmDFXXEkIfRYh3nxVa61ycYdoP6'
engine = create_engine('mysql://root:Antrust..,2020@localhost:3306/ruka_leufu')
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bemirag@gmail.com'
app.config['MAIL_PASSWORD'] = 'flancueces'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, username, password, nombre, apellido):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
    
    def save_to_db(self):
    	engine = create_engine('mysql://root:@localhost:3306/ruka_leufu')
    	cursor = engine.connect()
    	trans = cursor.begin()
    	try:
    		cursor.execute('INSERT INTO usuario (nombre, apellido, email, password) VALUES ("'+nombre+'", "'+apellido+'", "'+username+'", "'+password+'")')
    		trans.commit()
    	except:
    		raise UserNotFoundError('The table `users` did not exist, but it was created. Run the registration again.')
    		#cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    
    @classmethod
    def find_by_username(cls, username):
        cursor = engine.connect()
        
        try:
            data = cursor.execute('SELECT * FROM usuario WHERE email="'+username+'"').fetchone()
            if data:
                return cls(data[1], data[2])
        finally:
            print("")

@app.route('/')
def index():
	connection = engine.connect()
	contenido = connection.execute('SELECT * FROM contenido').fetchall()
	imagenes = connection.execute('SELECT * FROM imagen').fetchall()
	link = connection.execute('SELECT * FROM link').fetchall()
	telefono = ""
	correo = ""
	nosotros = []
	titulo = ""
	subtitulo = ""
	titulo_cabanas = ""
	titulo_tinajas = ""
	titulo_camping = ""
	titulo_atractivos = ""
	titulo_nosotros = ""
	titulo_tarifas = ""
	contenido_cabanas = []
	contenido_tinajas = []
	contenido_camping = []
	tarifa_temporada_alta = []
	tarifa_temporada_baja = []
	dict_contenido = {}
	dict_imagenes = {}
	titulo_servicios = ""
	titulo_inicio = ""
	titulo_como_llegar = ""
	titulo_contacto = ""
	titulo_seccion_atractivos = ""
	horario_pie_pagina = ""
	for c in contenido:
		if c.tag_contenido=="telefono1" or c.tag_contenido=="telefono2":
			if telefono!="":
				telefono += " / " + c.contenido+ " "
			else:
				telefono += c.contenido+ " "
		if c.tag_contenido=="correo":
			correo += c.contenido.decode('latin-1')
		if c.tag_contenido=="nosotros":
			nosotros = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="titulo":
			titulo = c.contenido.decode('latin-1')
		if c.tag_contenido=="subtitulo":
			subtitulo = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_cabanas":
			titulo_cabanas = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_tinajas":
			titulo_tinajas = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_camping":
			titulo_camping = c.contenido.decode('latin-1')
		if c.tag_contenido=="contenido_cabanas":
			contenido_cabanas = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="contenido_tinajas":
			contenido_tinajas = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="contenido_camping":
			contenido_camping = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="contenido_tarifa_temporada_alta":
			tarifa_temporada_alta = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="contenido_tarifa_temporada_baja":
			tarifa_temporada_baja = c.contenido.split("\r").decode('latin-1')
		if c.tag_contenido=="titulo_atractivos":
			titulo_atractivos = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_nosotros":
			titulo_nosotros = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_tarifas":
			titulo_tarifas = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_servicios":
			titulo_servicios = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_inicio":
			titulo_inicio = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_como_llegar":
			titulo_como_llegar = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_contacto":
			titulo_contacto = c.contenido.decode('latin-1')
		if c.tag_contenido=="titulo_seccion_atractivos":
			titulo_seccion_atractivos = c.contenido.decode('latin-1')
		if c.tag_contenido=="horario_pie_pagina":
			horario_pie_pagina = c.contenido.decode('latin-1')
	dict_contenido["telefono"] = telefono
	dict_contenido["correo"] = correo
	dict_contenido["nosotros"] = nosotros
	dict_contenido["titulo"] = titulo
	dict_contenido["subtitulo"] = subtitulo
	dict_contenido["titulo_cabanas"] = titulo_cabanas
	dict_contenido["titulo_tinajas"] = titulo_tinajas
	dict_contenido["titulo_camping"] = titulo_camping
	dict_contenido["contenido_cabanas"] = contenido_cabanas
	dict_contenido["contenido_tinajas"] = contenido_tinajas
	dict_contenido["contenido_camping"] = contenido_camping
	dict_contenido["tarifa_temporada_baja"] = tarifa_temporada_baja
	dict_contenido["tarifa_temporada_alta"] = tarifa_temporada_alta
	dict_contenido["titulo_atractivos"] = titulo_atractivos
	dict_contenido["titulo_nosotros"] = titulo_nosotros
	dict_contenido["titulo_tarifas"] = titulo_tarifas
	dict_contenido["titulo_servicios"] = titulo_servicios
	dict_contenido["titulo_inicio"] = titulo_inicio
	dict_contenido["titulo_como_llegar"] = titulo_como_llegar
	dict_contenido["titulo_contacto"] = titulo_contacto
	dict_contenido["titulo_seccion_atractivos"] = titulo_seccion_atractivos
	dict_contenido["horario_pie_pagina"] = horario_pie_pagina
	imagen_inicio = ""
	imagenes_cabanas = []
	imagenes_tinajas = []
	imagenes_camping = []
	imagenes_atractivos = []
	imagen_mapa = ""
	imagen_pr_cabanas = ""
	imagen_pr_tinajas = ""
	imagen_pr_camping = ""
	imagen_fondo_nosotros = ""
	imagen_txt_fondo_nosotros = ""
	imagen_logo_pr = ""
	img_fondo_pie_pagina = ""
	fondo_contacto = ""
	patron_shatered = ""
	imagenes_instagram = []
	for i in imagenes:
		if i.seccion=="inicio":
			imagen_inicio = i.imagen
		if i.subseccion=="cabanas":
			imagenes_cabanas.append((i.imagen, i.titulo))
		if i.subseccion=="tinajas":
			imagenes_tinajas.append((i.imagen, i.titulo))
		if i.subseccion=="camping":
			imagenes_camping.append((i.imagen, i.titulo))	
		if i.seccion=="atractivos":
			imagenes_atractivos.append((i.imagen, i.titulo, i.subtitulo))
		if i.seccion=="como_llegar":
			imagen_mapa = i.imagen
		if i.subseccion=="cabanas" and i.principal==1:
			imagen_pr_cabanas = i.imagen
		if i.subseccion=="tinajas" and i.principal==1:
			imagen_pr_tinajas = i.imagen
		if i.subseccion=="camping" and i.principal==1:
			imagen_pr_camping = i.imagen
		if i.subseccion=="fondo_nosotros":
			imagen_fondo_nosotros = i.imagen
		if i.subseccion=="fondo_texto_nosotros":
			imagen_txt_fondo_nosotros = i.imagen
		if i.subseccion=="logo_principal":
			imagen_logo_pr = i.imagen
		if i.subseccion=="fondo_pie_pagina":
			img_fondo_pie_pagina = i.imagen
		if i.subseccion=="fondo_contacto":
			fondo_contacto = i.imagen
		if i.subseccion=="patron_shatered":
			patron_shatered = i.imagen
		if i.seccion=="instagram":
			imagenes_instagram.append(i.imagen)
	dict_imagenes["imagen_inicio"] = imagen_inicio
	dict_imagenes["imagenes_cabanas"] = imagenes_cabanas
	dict_imagenes["imagenes_tinajas"] = imagenes_tinajas
	dict_imagenes["imagenes_camping"] = imagenes_camping
	dict_imagenes["imagenes_atractivos"] = imagenes_atractivos
	dict_imagenes["imagen_mapa"] = imagen_mapa
	dict_imagenes["imagen_pr_cabanas"] = imagen_pr_cabanas
	dict_imagenes["imagen_pr_tinajas"] = imagen_pr_tinajas
	dict_imagenes["imagen_pr_camping"] = imagen_pr_camping
	dict_imagenes["imagen_fondo_nosotros"] = imagen_fondo_nosotros
	dict_imagenes["imagen_txt_fondo_nosotros"] = imagen_txt_fondo_nosotros
	dict_imagenes["imagen_logo_pr"] = imagen_logo_pr
	dict_imagenes["img_fondo_pie_pagina"] = img_fondo_pie_pagina
	dict_imagenes["fondo_contacto"] = fondo_contacto
	dict_imagenes["patron_shatered"] = patron_shatered
	dict_imagenes["imagenes_instagram"] = imagenes_instagram
	print(dict_imagenes["imagenes_atractivos"])
	#try:
	#	User("huichaman.juan@gmail.com", generate_password_hash("antrust..,2020")).save_to_db()
	#except Exception as e:
	#	print(e)
	dict_link = {}
	link_waze = ""
	link_google_maps = ""
	link_facebook = ""
	link_instagram = ""
	link_lago_maihue = ""
	link_termas = ""
	link_feria = ""
	link_noticias = []
	for l in link:
		if l.tag=="waze":
			link_waze = l.link
		if l.tag=="google_maps":
			link_google_maps = l.link
		if l.tag=="facebook":
			link_facebook = l.link
		if l.tag=="instagram":
			link_instagram = l.link
		if l.tag=="lago_maihue":
			link_lago_maihue = l.link
		if l.tag=="termas_chihuio":
			link_termas = l.link
		if l.tag=="feria_chabranco":
			link_feria = l.link
		if l.seccion=="noticia":
			myTime = datetime.strptime(str(l.fecha), "%Y-%m-%d %H:%M:%S")

			myFormat = "%Y-%m-%d"
			new_fecha = myTime.strftime(myFormat)
			link_noticias.append((l.link, l.titulo, new_fecha))
	dict_link["waze"] = link_waze
	dict_link["google_maps"] = link_google_maps
	dict_link["facebook"] = link_facebook
	dict_link["instagram"] = link_instagram
	dict_link["link_lago_maihue"] = link_lago_maihue
	dict_link["link_termas"] = link_termas
	dict_link["link_feria"] = link_feria
	dict_link["link_noticias"] = link_noticias
	return render_template('index.html', dict_contenido=dict_contenido, dict_imagenes=dict_imagenes, dict_link=dict_link)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'loggedin' in session:
		connection = engine.connect()
		mensajes = connection.execute('SELECT count(*) as cantidad FROM mensaje').fetchall()
		return render_template('admin.html', user=session['username'], cant_mensajes=mensajes[0][0])
	return redirect(url_for('login'))

@app.route('/config', methods=['GET', 'POST'])
def config():
	if 'loggedin' in session:
		connection = engine.connect()
		contenido = connection.execute('SELECT * FROM contenido').fetchall()
		imagenes = connection.execute('SELECT * FROM imagen').fetchall()
		contenido_inicio = []
		contenido_nosotros = []
		contenido_servicios = []
		contenido_atractivos = []
		contenido_como_llegar = []
		contenido_contacto = []
		dict_contenido = {}
		for c in contenido:
			if c.seccion=="inicio":
				contenido_inicio.append((c.titulo, c.tag_contenido, c.contenido))
			if c.seccion=="nosotros":
				contenido_nosotros.append((c.titulo, c.tag_contenido, c.contenido))
			if c.seccion=="servicios":
				contenido_servicios.append((c.titulo, c.tag_contenido, c.contenido))
			if c.seccion=="atractivos":
				contenido_atractivos.append((c.titulo, c.tag_contenido, c.contenido))
			if c.seccion=="como_llegar":
				contenido_como_llegar.append((c.titulo, c.tag_contenido, c.contenido))
			if c.seccion=="contacto":
				contenido_contacto.append((c.titulo, c.tag_contenido, c.contenido))
		dict_contenido["contenido_inicio"] = contenido_inicio
		dict_contenido["contenido_nosotros"] = contenido_nosotros
		dict_contenido["contenido_servicios"] = contenido_servicios
		dict_contenido["contenido_atractivos"] = contenido_atractivos
		dict_contenido["contenido_como_llegar"] = contenido_como_llegar
		dict_contenido["contenido_contacto"] = contenido_contacto
		return render_template('config.html', user=session['username'], dict_contenido=dict_contenido)
	return redirect(url_for('login'))

@app.route('/users', methods=['GET', 'POST'])
def users():
	connection = engine.connect()
	usuario = connection.execute('SELECT * FROM usuario').fetchall()
	return render_template('users.html', user=session['username'], usuario=usuario)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['email']
    password = request.form['password']
    
    try:
        User(username, generate_password_hash(password)).save_to_db()
    except Exception as e:
        return jsonify({'error': e.message}), 500
    
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
	    username = request.form['email']
	    password = request.form['password']
	    connection = engine.connect()
	    user = connection.execute('SELECT * FROM usuario WHERE email = "'+username+'"').fetchone()

	    if user and check_password_hash(user.password, password):
	    	session['loggedin'] = True
	    	session['id'] = user.id
	    	session['username'] = user.email
	    	flash('Has iniciado sesión correctamente')
	    	return redirect(url_for('admin'))
	        #return jsonify({'message': 'Password is correct'})  # You'll want to return a token that verifies the user in the future
	    else:
	    	msg = 'Nombre de Usuario/Contraseña Incorrectos'
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/update_inicio', methods=['POST'])
def update_inicio():
	connection = engine.connect()
	telefono1 = request.form['telefono1']
	connection.execute('Update contenido set contenido = "'+telefono1+'" where tag_contenido = "telefono1"')
	telefono2 = request.form['telefono2']
	connection.execute('Update contenido set contenido = "'+telefono2+'" where tag_contenido = "telefono2"')
	correo = request.form['correo']
	connection.execute('Update contenido set contenido = "'+correo+'" where tag_contenido = "correo"')
	titulo = request.form['titulo']
	connection.execute('Update contenido set contenido = "'+titulo+'" where tag_contenido = "titulo"')
	subtitulo = request.form['subtitulo']
	connection.execute('Update contenido set contenido = "'+subtitulo+'" where tag_contenido = "subtitulo"')
	titulo_inicio = request.form['titulo_inicio']
	connection.execute('Update contenido set contenido = "'+titulo_inicio+'" where tag_contenido = "titulo_inicio"')
	flash('Actualización Inicio Exitosa')
	return redirect(url_for('config'))

@app.route('/update_nosotros', methods=['POST'])
def update_nosotros():
	connection = engine.connect()
	nosotros = request.form['nostros']
	connection.execute('Update contenido set contenido = "'+nosotros+'" where tag_contenido = "nosotros"')
	titulo_nosotros = request.form['titulo_nosotros']
	connection.execute('Update contenido set contenido = "'+titulo_nosotros+'" where tag_contenido = "titulo_nosotros"')
	flash('Actualización Nosotros Exitosa')
	return redirect(url_for('config'))

@app.route('/update_servicios', methods=['POST'])
def update_servicios():
	connection = engine.connect()
	titulo_cabanas = request.form['titulo_cabanas']
	connection.execute('Update contenido set contenido = "'+titulo_cabanas+'" where tag_contenido = "titulo_cabanas"')
	titulo_tinajas = request.form['titulo_tinajas']
	connection.execute('Update contenido set contenido = "'+titulo_tinajas+'" where tag_contenido = "titulo_tinajas"')
	titulo_camping = request.form['titulo_camping']
	connection.execute('Update contenido set contenido = "'+titulo_camping+'" where tag_contenido = "titulo_camping"')
	contenido_cabanas = request.form['contenido_cabanas']
	connection.execute('Update contenido set contenido = "'+contenido_cabanas+'" where tag_contenido = "contenido_cabanas"')
	contenido_tinajas = request.form['contenido_tinajas']
	connection.execute('Update contenido set contenido = "'+contenido_tinajas+'" where tag_contenido = "contenido_tinajas"')
	contenido_camping = request.form['contenido_camping']
	connection.execute('Update contenido set contenido = "'+contenido_camping+'" where tag_contenido = "contenido_camping"')
	contenido_tarifa_temporada_alta = request.form['contenido_tarifa_temporada_alta']
	connection.execute('Update contenido set contenido = "'+contenido_tarifa_temporada_alta+'" where tag_contenido = "contenido_tarifa_temporada_alta"')
	contenido_tarifa_temporada_baja = request.form['contenido_tarifa_temporada_baja']
	connection.execute('Update contenido set contenido = "'+contenido_tarifa_temporada_baja+'" where tag_contenido = "contenido_tarifa_temporada_baja"')
	titulo_tarifas = request.form['titulo_tarifas']
	connection.execute('Update contenido set contenido = "'+titulo_tarifas+'" where tag_contenido = "titulo_tarifas"')
	titulo_servicios = request.form['titulo_servicios']
	connection.execute('Update contenido set contenido = "'+titulo_servicios+'" where tag_contenido = "titulo_servicios"')
	flash('Actualización Servicios Exitosa')
	return redirect(url_for('config'))

@app.route('/update_atractivos', methods=['POST'])
def update_atractivos():
	connection = engine.connect()
	titulo_seccion_atractivos = request.form['titulo_seccion_atractivos']
	connection.execute('Update contenido set contenido = "'+titulo_seccion_atractivos+'" where tag_contenido = "titulo_seccion_atractivos"')
	titulo_atractivos = request.form['titulo_atractivos']
	connection.execute('Update contenido set contenido = "'+titulo_atractivos+'" where tag_contenido = "titulo_atractivos"')
	flash('Actualización Atractivos Exitosa')
	return redirect(url_for('config'))

@app.route('/update_como_llegar', methods=['POST'])
def update_como_llegar():
	connection = engine.connect()
	titulo_como_llegar = request.form['titulo_como_llegar']
	connection.execute('Update contenido set contenido = "'+titulo_como_llegar+'" where tag_contenido = "titulo_como_llegar"')
	flash('Actualización Cómo Llegar Exitosa')
	return redirect(url_for('config'))

@app.route('/update_contacto', methods=['POST'])
def update_contacto():
	connection = engine.connect()
	titulo_contacto = request.form['titulo_contacto']
	connection.execute('Update contenido set contenido = "'+titulo_contacto+'" where tag_contenido = "titulo_contacto"')
	flash('Actualización Contacto Exitosa')
	return redirect(url_for('config'))

@app.route('/images', methods=['GET', 'POST'])
def images():
	if 'loggedin' in session:
		connection = engine.connect()
		imagenes = connection.execute('SELECT * FROM imagen').fetchall()
		imagenes_inicio = []
		imagenes_nosotros = []
		imagenes_servicios = []
		imagenes_atractivos = []
		imagenes_como_llegar = []
		imagenes_contacto = []
		imagenes_logos = []
		imagenes_instagram = []
		dict_imagenes = {}
		list_inicio = os.listdir("static/images/inicio")
		list_nosotros = os.listdir("static/images/nosotros")
		list_servicios = os.listdir("static/images/servicios")
		list_atractivos = os.listdir("static/images/atractivos")
		list_como_llegar = os.listdir("static/images/como_llegar")
		list_contacto = os.listdir("static/images/contacto")
		list_logos = os.listdir("static/images/logos")
		list_instagram = os.listdir("static/images/instagram")

		for c in imagenes:
			if c.seccion=="inicio":
				imagenes_inicio.append((c.id, c.imagen, c.titulo, c.subtitulo, c.principal))
			if c.seccion=="nosotros":
				imagenes_nosotros.append((c.id, c.imagen, c.titulo, c.subtitulo, c.principal))
			if c.seccion=="servicios":
				imagenes_servicios.append((c.id, c.imagen, c.titulo, c.subtitulo, c.subseccion, c.principal))
			if c.seccion=="atractivos":
				imagenes_atractivos.append((c.id, c.imagen, c.titulo, c.subtitulo, c.principal))
			if c.seccion=="como_llegar":
				imagenes_como_llegar.append((c.id, c.imagen, c.titulo, c.subtitulo, c.principal))
			if c.seccion=="contacto":
				imagenes_contacto.append((c.id, c.imagen, c.titulo, c.subtitulo, c.principal))
			if c.seccion=="logos":
				imagenes_logos.append((c.id, c.imagen, c.titulo, c.subtitulo))
			if c.seccion=="instagram":
				imagenes_instagram.append((c.id, c.imagen, c.titulo, c.subtitulo))
		dict_imagenes["imagenes_inicio"] = imagenes_inicio
		dict_imagenes["imagenes_nosotros"] = imagenes_nosotros
		dict_imagenes["imagenes_servicios"] = imagenes_servicios
		dict_imagenes["imagenes_atractivos"] = imagenes_atractivos
		dict_imagenes["imagenes_como_llegar"] = imagenes_como_llegar
		dict_imagenes["imagenes_contacto"] = imagenes_contacto
		dict_imagenes["imagenes_logos"] = imagenes_logos
		dict_imagenes["imagenes_instagram"] = imagenes_instagram
		dict_imagenes["list_inicio"] = list_inicio
		dict_imagenes["list_nosotros"] = list_nosotros
		dict_imagenes["list_servicios"] = list_servicios
		dict_imagenes["list_atractivos"] = list_atractivos
		dict_imagenes["list_como_llegar"] = list_como_llegar
		dict_imagenes["list_contacto"] = list_contacto
		dict_imagenes["list_logos"] = list_logos
		dict_imagenes["list_instagram"] = list_instagram
		return render_template('images.html', user=session['username'], dict_imagenes=dict_imagenes)
	return redirect(url_for('login'))

@app.route('/contact', methods=['POST'])
def contact():
	connection = engine.connect()
	nombre = request.form['nombre']
	email = request.form['email']
	mensaje = request.form['mensaje']
	fecha = str(datetime.now())
	try:
		connection.execute('INSERT INTO mensaje (nombre, email, mensaje, fecha) VALUES ("'+nombre+'", "'+email+'", "'+mensaje+'", "'+fecha+'")')
	except Exception as e:
		print(e)
	msg = Message('Contacto '+nombre, sender = email, recipients = ['bemirag@gmail.com'])
	msg.body = mensaje
	mail.send(msg)
	return json.dumps({'status':'OK'})

@app.route('/update_images_inicio', methods=['POST'])
def update_images_inicio():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="inicio"').fetchall()
	for c in imagenes:
		if c.seccion=="inicio":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/inicio/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Inicio Exitosa')
	return redirect(url_for('images'))

@app.route('/update_images_nosotros', methods=['POST'])
def update_images_nosotros():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="nosotros"').fetchall()
	for c in imagenes:
		if c.seccion=="nosotros":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/nosotros/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Nosotros Exitosa')
	return redirect(url_for('images'))

@app.route('/update_images_servicios', methods=['POST'])
def update_images_servicios():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="servicios"').fetchall()
	print("aca")
	for c in imagenes:
		if c.seccion=="servicios":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/servicios/"+imagen
			titulo = request.form['titulo'+str(c.id)]
			if request.form.get('principal'+str(c.id)):
				principal = request.form['principal'+str(c.id)]
			else:
				principal = 0
			connection.execute('Update imagen set titulo = "'+titulo+'", principal = '+str(principal)+' where id = '+str(c.id))
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Servicios Exitosa')
	return redirect(url_for('images'))


@app.route('/update_images_atractivos', methods=['POST'])
def update_images_atractivos():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="atractivos"').fetchall()
	print("aca")
	for c in imagenes:
		if c.seccion=="atractivos":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/atractivos/"+imagen
			titulo = request.form['titulo'+str(c.id)]
			subtitulo = request.form['subtitulo'+str(c.id)]
			connection.execute('Update imagen set titulo = "'+titulo+'", subtitulo = "'+subtitulo+'" where id = '+str(c.id))
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Atractivos Exitosa')
	return redirect(url_for('images'))


@app.route('/update_images_como_llegar', methods=['POST'])
def update_images_como_llegar():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="como_llegar"').fetchall()
	for c in imagenes:
		if c.seccion=="como_llegar":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/como_llegar/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Cómo Llegar Exitosa')
	return redirect(url_for('images'))

@app.route('/update_images_contacto', methods=['POST'])
def update_images_contacto():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="contacto"').fetchall()
	for c in imagenes:
		if c.seccion=="contacto":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/contacto/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Contacto Exitosa')
	return redirect(url_for('images'))

@app.route('/update_images_logos', methods=['POST'])
def update_images_logos():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="logos"').fetchall()
	for c in imagenes:
		if c.seccion=="logos":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/logos/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Logos Exitosa')
	return redirect(url_for('images'))

@app.route('/update_images_instagram', methods=['POST'])
def update_images_instagram():
	connection = engine.connect()
	imagenes = connection.execute('SELECT * FROM imagen where seccion="instagram"').fetchall()
	for c in imagenes:
		if c.seccion=="instagram":
			imagen = request.form['imagen'+str(c.id)]
			new_img = "static/images/instagram/"+imagen
			if imagen!="":
				connection.execute('Update imagen set imagen = "'+new_img+'" where id = '+str(c.id))
	flash('Actualización Imagenes Logos Exitosa')
	return redirect(url_for('images'))

@app.route('/upload_images', methods=['POST'])
def upload_images():
	connection = engine.connect()
	carpeta = request.form['carpeta']
	path = "static/images/"+carpeta+"/"
	if carpeta=="servicios":
		servicio = request.form['servicio']
		slider = request.form['slider']
		fecha = str(datetime.now())
		for uploaded_file in request.files.getlist('files'):
			if uploaded_file.filename != '':
				print(uploaded_file.filename)
				uploaded_file.save(path+uploaded_file.filename)
				if slider=="si":
					try:
						file = path+uploaded_file.filename
						connection.execute('INSERT INTO imagen (imagen, usuario, modificado, seccion, subseccion) VALUES ("'+file+'", 1, "'+fecha+'", "servicios", "'+servicio+'")')
					except Exception as e:
						print(e)
	else:
		for uploaded_file in request.files.getlist('files'):
			if uploaded_file.filename != '':
				print(uploaded_file.filename)
				uploaded_file.save(path+uploaded_file.filename)
	flash('Imagenes subidas exitosamente')
	return redirect(url_for('upload_files'))


@app.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
	if 'loggedin' in session:
		return render_template('upload_files.html')
	return redirect(url_for('login'))


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	connection = engine.connect()
	email = request.form['email']
	password = request.form['password']
	nombre = request.form['nombre']
	apellido = request.form['apellido']
	try:
		pass2 = generate_password_hash(password)
		connection.execute('INSERT INTO usuario (nombre, apellido, email, password) VALUES ("'+nombre+'", "'+apellido+'", "'+email+'", "'+pass2+'")')
	except Exception as e:
		print(e)
	flash('Usuario creado exitosamente')
	return redirect(url_for('users'))

@app.route('/messages', methods=['GET', 'POST'])
def messages():
	if 'loggedin' in session:
		connection = engine.connect()
		mensajes = connection.execute('SELECT * FROM mensaje').fetchall()
		return render_template('messages.html', user=session['username'], mensajes=mensajes)
	return redirect(url_for('login'))


@app.route('/config_link', methods=['GET', 'POST'])
def config_link():
	if 'loggedin' in session:
		connection = engine.connect()
		links = connection.execute('SELECT * FROM link').fetchall()
		return render_template('link.html', user=session['username'], links=links)
	return redirect(url_for('login'))

@app.route('/update_enlaces', methods=['POST'])
def update_enlaces():
	connection = engine.connect()
	links = connection.execute('SELECT * FROM link').fetchall()
	for l in links:
		if l.seccion=="noticia":
			titulo = request.form['titulo'+str(l.id)]
			link = request.form['link'+str(l.id)]
			fecha = str(datetime.now())
			connection.execute('Update link set link = "'+link+'", titulo = "'+titulo+'", fecha = "'+fecha+'" where id = '+str(l.id))
			sql = "UPDATE link SET link = %s, titulo = %s, fecha = %s WHERE id = %s"
			val = (link, titulo, fecha, str(l.id))
			connection.execute(sql, val)
		else:
			link = str(request.form['link'+str(l.id)])
			sql = "UPDATE link SET link = %s WHERE id = %s"
			val = (link, str(l.id))
			connection.execute(sql, val)
	flash('Actualización de Enlaces Exitosa')
	return redirect(url_for('config_link'))

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    #app.run("0.0.0.0", port="8080")
    app.run()