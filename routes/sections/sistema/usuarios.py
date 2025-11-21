# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, desc
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased
import os
import json
import re
import hashlib
import difflib
import requests
import random
import pytz
import requests
import string
from io import BytesIO
from google.api_core.client_options import ClientOptions
from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
from google import genai
import datetime
import pandas as pd
import traceback # Asume que pandas está importado
import uuid
#llamar a config
from routes.models import db, Configuracion, Users
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion

usuarios_bp = Blueprint('usuarios_bp', __name__)

#===Listado===
@usuarios_bp.route('/sistema/users')
@validar_sesion
def users():
	return render_template('sections/sistema/usuarios/listado.html')

#===Listado Ajax===
@usuarios_bp.route('/sistema/users/listado-ajax', methods=['GET', 'POST'])
@validar_sesion
def users_listarAjax():
	try:
		if request.method in ['GET', 'POST']:
			buscar = request.values.get('buscar')
			query = Users.query.filter(
				Users.user_estado == 1,
				Users.user_permiso != 'superadmin'
			)
			if buscar:
				query = query.filter(or_(
					Users.user_name.like(f'%{buscar}%'),
					Users.user_email.like(f'%{buscar}%')
				))
			query = query.order_by(Users.user_id)
			lista = query.all()
			if lista:
				return render_template('sections/sistema/usuarios/listado-ajax.html', lista=lista)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Papelera===
@usuarios_bp.route('/sistema/users/papelera')
@validar_sesion
def alertsPapelera():
	return render_template('sections/sistema/usuarios/papelera.html')

#===Papelera Ajax===
@usuarios_bp.route('/sistema/users/papelera-ajax', methods=['GET', 'POST'])
@validar_sesion
def users_papeleraAjax():
	if request.method in ['GET', 'POST']:
		buscar = request.values.get('buscar')
		query = Users.query.filter(
			Users.user_estado == 0,
			Users.user_permiso != 'superadmin'
		)
		if buscar:
			query = query.filter(or_(
				Users.user_name.like(f'%{buscar}%'),
				Users.user_email.like(f'%{buscar}%')
			))
		lista = query.all()
		if lista:
			return render_template('sections/sistema/usuarios/papelera-ajax.html', lista=lista)
		else:
			return 'No se encontraron campañas con los criterios especificados.'
	return 'Error en el método de solicitud'

#===Agregar===
@usuarios_bp.route('/sistema/users/agregar')
@validar_sesion
def users_add():
	return render_template('sections/sistema/usuarios/agregar.html',selectPermiso=selectPermiso)
#===Editar===
@usuarios_bp.route('/sistema/users/editar')
@validar_sesion
def users_edit():
	user_id = request.values.get('id')
	data = Users.query.filter_by(user_id=user_id).first()
	if data:
		return render_template('sections/sistema/usuarios/editar.html', data=data,selectPermiso=selectPermiso)
	else:
		return 'No se encontraron usuarios con los criterios especificados.'
#===Perfil===
@usuarios_bp.route('/perfil')
def users_perfil():
	user_name = session.get('usuario')
	user_id = session.get('id')
	data = Users.query.filter_by(user_id=user_id).first()
	if data:
		return render_template('sections/sistema/perfil/main.html', data=data)
	else:
		return 'No se encontraron usuarios con los criterios especificados.'
	#return render_template("perfil.html",user_name=user_name)
#===Save===
@usuarios_bp.route('/sistema/users/save', methods=['POST'])
@validar_sesion
def users_save():
	if request.method == 'POST':
		user_name = request.form.get('usu_usuario')
		user_email = request.form.get('usu_email')
		user_phone = request.form.get('usu_phone')
		user_pass = request.form.get('usu_password')
		user_passmd5 = encMD5(user_pass)
		user_permiso = request.form.get('cbo_permiso')
		user_estado = 1

		if usuarioExiste(user_email):
			session['mensaje'] = "El usuario ya existe. Por favor, usa otro email."
			return redirect('/usuarios/agregar')
		else:
			new_user = Users(
				user_name=user_name,
				user_phone=user_phone,
				user_email=user_email,
				user_pass=user_passmd5,
				user_permiso=user_permiso,
				user_estado=user_estado
			)
			db.session.add(new_user)
			db.session.commit()
			return redirect('/sistema/users')
	return 'Error en el método de solicitud'

#===Update===
@usuarios_bp.route('/sistema/users/update', methods=['POST'])
@validar_sesion
def users_update():
	if request.method == 'POST':
		user_id = request.form.get('usu_id')
		user_name = request.form.get('usu_usuario')
		user_phone = request.form.get('usu_phone')
		user_email = request.form.get('usu_email')
		user_pass = request.form.get('usu_password')
		user_passmd5 = encMD5(user_pass) if user_pass else None
		user_permiso = request.form.get('cbo_permiso')
		user_id = int(user_id)

		if usuarioExisteUpdate(user_email, user_id):
			user = Users.query.filter_by(user_id=user_id).first()
			if user:
				user.user_name = user_name
				user.user_phone = user_phone
				user.user_email = user_email
				user.user_permiso = user_permiso
				if user_passmd5:
					user.user_pass = user_passmd5
				db.session.commit()
			session['mensaje'] = "Se actualizaron los datos"
			#return redirect('/sistema/users')
			return redirect('/sistema/users/editar?id=' + str(user_id))
		else:
			session['mensaje'] = "El usuario ya existe. Por favor, usa otro email."
			return redirect('/sistema/users/editar?id=' + str(user_id))
	return 'Error en el método de solicitud'

#===Perfil Update===
@usuarios_bp.route('/perfil/update', methods=['POST'])
@validar_sesion
def perfil_update():
	if request.method == 'POST':
		user_id = request.form.get('usu_id')
		user_name = request.form.get('usu_usuario')
		user_phone = request.form.get('usu_phone')
		user_email = request.form.get('usu_email')
		user_pass = request.form.get('usu_password')
		user_passmd5 = encMD5(user_pass) if user_pass else None
		user_id = int(user_id)

		if usuarioExisteUpdate(user_email, user_id):
			user = Users.query.filter_by(user_id=user_id).first()
			if user:
				user.user_name = user_name
				user.user_phone = user_phone
				user.user_email = user_email
				if user_passmd5:
					user.user_pass = user_passmd5
				db.session.commit()
			session['mensaje'] = "Se actualizaron los datos"
			#return redirect('/sistema/users')
			return redirect('/perfil?id=' + str(user_id))
		else:
			session['mensaje'] = "El usuario ya existe. Por favor, usa otro email."
			return redirect('/perfil?id=' + str(user_id))
	return 'Error en el método de solicitud'

#===Delete===
@usuarios_bp.route('/sistema/users/delete')
@validar_sesion
def users_delete():
	user_id = request.values.get('id')
	user_id = int(user_id)
	user = Users.query.filter_by(user_id=user_id).first()
	if user:
		user.user_estado = 0
		db.session.commit()
	return redirect('/sistema/users')

#===Recovery===
@usuarios_bp.route('/sistema/users/recovery')
@validar_sesion
def users_recovery():
	user_id = request.values.get('id')
	user_id = int(user_id)
	user = Users.query.filter_by(user_id=user_id).first()
	if user:
		user.user_estado = 1
		db.session.commit()
	return redirect('/sistema/users/papelera')

#===Funciones Auxiliares===
def selectPermiso(plataforma=None):
	#lblPlataforma = "hello"
	query = Configuracion.query.filter_by(conf_type='user_permiso', conf_estado=1)
	platforms = query.all()
	lblPlataforma = "<select class='form-select' id='cbo_permiso' name='cbo_permiso'>"
	lblPlataforma += "<option value='' selected disabled hidden>Permiso</option>"
	for platform in platforms:
		platform_value = platform.conf_value
		platform_name = platform.conf_name
		platform_symbol = platform.conf_symbol
		selected = "selected" if plataforma == platform_name else ""
		lblPlataforma += f"<option value='{platform_name}' {selected}>{platform_value.capitalize()}</option>"
	lblPlataforma += "</select>"
	return lblPlataforma
def usuarioExiste(email, user_id=None):
	query = Users.query.filter_by(user_email=email)
	if user_id:
		query = query.filter(Users.user_id != user_id)
	user = query.first()
	return user is not None
def usuarioExisteUpdate(email, user_id=None):
	query = Users.query.filter_by(user_email=email)
	
	if user_id is not None:
		# **SOLUCIÓN:** Asegurar que el ID sea un entero. 
		# Si llega como str (que es lo que causa el error), lo convertimos.
		try:
			user_id = int(user_id)
		except (ValueError, TypeError):
			# Manejo de error si el valor pasado no puede ser int
			print(f"Advertencia: user_id '{user_id}' no es un entero válido.")
			return False # Asume conflicto o manejo de error.

		query = query.filter(Users.user_id != user_id)
		
	usuario_existente = query.first()
	# Retorna True si NO existe un usuario con ese email (o si solo existe el actual)
	return usuario_existente is None

def encMD5(password):
	password_bytes = password.encode('utf-8')
	md5_hash = hashlib.md5()
	md5_hash.update(password_bytes)
	hashed_password = md5_hash.hexdigest()
	return hashed_password
def verEstado(valor):
	if valor == 1:
		result = "active"
	elif valor == 0:
		result = "disabled"
	else:
		result = "desconocido"  # O el valor que prefieras para casos no manejados
	return result