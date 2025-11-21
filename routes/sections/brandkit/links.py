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
from routes.models import db, Configuracion, Links
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion

links_bp = Blueprint('links_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/brandkit/links/')

#===Listado===
@links_bp.route('/')
@validar_sesion
def bklinks_main(brand_id,proyecto_id):
	pid = proyecto_id
	return render_template('sections/brandkit/links/listado.html',pid=pid)

#===Listado Ajax===
@links_bp.route('listado-ajax', methods=['GET', 'POST'])
@validar_sesion
def bklinks_listarAjax(brand_id,proyecto_id):
	try:
		if request.method in ['GET', 'POST']:
			pid = request.values.get('pid')
			buscar = request.values.get('buscar')
			query = Links.query.filter(
				Links.link_estado == 1,
				Links.proyecto_id == pid
			)
			if buscar:
				query = query.filter(Links.link_name.like(f'%{buscar}%'))
			query = query.order_by(Links.link_id)
			lista = query.all()
			if lista:
				return render_template('sections/brandkit/links/listado-ajax.html', lista=lista,verEstado=verEstado,pid=pid)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Papelera===
@links_bp.route('papelera')
@validar_sesion
def links_papelera(brand_id,proyecto_id):
	pid = proyecto_id
	return render_template('sections/brandkit/links/papelera.html',pid=pid)

#===Papelera Ajax===
@links_bp.route('papelera-ajax', methods=['GET', 'POST'])
@validar_sesion
def links_papeleraAjax(brand_id,proyecto_id):
	if request.method in ['GET', 'POST']:
		buscar = request.values.get('buscar')
		query = Links.query.filter(
			Links.link_estado == 0,
		)
		if buscar:
			query = query.filter(Links.link_name.like(f'%{buscar}%'))
		lista = query.all()
		if lista:
			return render_template('sections/brandkit/links/papelera-ajax.html', lista=lista,verEstado=verEstado)
		else:
			return 'No se encontraron campañas con los criterios especificados.'
	return 'Error en el método de solicitud'

#===Agregar===
@links_bp.route('agregar')
@validar_sesion
def links_add(brand_id,proyecto_id):
	pid = proyecto_id
	return render_template('sections/brandkit/links/agregar.html',selectPermiso=selectPermiso,pid=pid)
#===Editar===
@links_bp.route('editar')
@validar_sesion
def links_edit(brand_id,proyecto_id):
	pid = request.values.get('pid')
	link_id = request.values.get('id')
	data = Links.query.filter_by(link_id=link_id).first()
	if data:
		return render_template('sections/brandkit/links/editar.html', data=data,selectPermiso=selectPermiso,pid=pid)
	else:
		return 'No se encontraron usuarios con los criterios especificados.'
#===Save===
@links_bp.route('save', methods=['POST'])
@validar_sesion
def links_save(brand_id,proyecto_id):
	if request.method == 'POST':
		link_name = request.form.get('link_name')
		link_url = request.form.get('link_url')
		link_estado = 1
		pid = request.values.get('txt_pid')

		if linkExiste(link_url):
			session['mensaje'] = "El link ya existe. Por favor, usa otro email."
			return redirect('/usuarios/agregar')
		else:
			new_data = Links(
				link_name=link_name,
				link_url=link_url,
				link_estado=link_estado,
				proyecto_id = pid
			)
			db.session.add(new_data)
			db.session.commit()
			return redirect('../links/')
	return 'Error en el método de solicitud'

#===Update===
@links_bp.route('update', methods=['POST'])
@validar_sesion
def links_update(brand_id,proyecto_id):
	if request.method == 'POST':
		link_id = request.form.get('link_id')
		link_name = request.form.get('link_name')
		link_url = request.form.get('link_url')
		pid = request.values.get('txt_pid')

		if not linkExiste(link_url, link_id):
			link = Links.query.filter_by(link_id=link_id).first()
			if link:
				link.link_name = link_name
				link.link_url = link_url
				db.session.commit()
			session['mensaje'] = "Se actualizaron los datos"
			#return redirect('/brandkit/links')
			return redirect('editar?id=' + str(link_id))
		else:
			session['mensaje'] = "El usuario ya existe. Por favor, usa otro email."
			return redirect('editar?id=' + str(link_id))
			#return redirect(f"/brand/{brand_id}/info/")
	return 'Error en el método de solicitud'

#===Delete===
@links_bp.route('delete')
@validar_sesion
def links_delete(brand_id,proyecto_id):
	pid = proyecto_id
	link_id = request.values.get('id')
	link = Links.query.filter_by(link_id=link_id).first()
	if link:
		link.link_estado = 0
		db.session.commit()
	return redirect('../links')

#===Recovery===
@links_bp.route('recovery')
@validar_sesion
def links_recovery(brand_id,proyecto_id):
	pid = request.values.get('pid')
	link_id = request.values.get('id')
	link = Links.query.filter_by(link_id=link_id).first()
	if link:
		link.link_estado = 1
		db.session.commit()
	return redirect('papelera')

#===Funciones Auxiliares===
def selectPermiso(plataforma=None):
	#lblPlataforma = "hello"
	query = Configuracion.query.filter_by(conf_type='link_permiso', conf_estado=1)
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
def linkExiste(email, link_id=None):
	query = Links.query.filter_by(link_url=email)
	if link_id:
		query = query.filter(Links.link_id != link_id)
	user = query.first()
	return user is not None
def verEstado(valor):
	if valor == 1:
		result = "active"
	elif valor == 0:
		result = "disabled"
	else:
		result = "desconocido"  # O el valor que prefieras para casos no manejados
	return result