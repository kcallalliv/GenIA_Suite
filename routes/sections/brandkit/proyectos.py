# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased
from sqlalchemy import desc, and_
from bs4 import BeautifulSoup
from io import BytesIO
import os
import json
import re
import hashlib
import difflib
import requests
import random
import pytz
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
from routes.models import db, Assets, Configuracion, Proyectos
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

proyectos_bp = Blueprint('proyectos_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/')
#===View===
@proyectos_bp.route('view')
@validar_sesion
def proyectos_view(brand_id):
	proyecto_id = request.values.get('id')
	session['proyecto_id'] = proyecto_id
	return render_template('sections/proyectos/main.html')
#===New===
@proyectos_bp.route('agregar')
@validar_sesion
def proyectos_add(brand_id):
	return render_template('sections/proyectos/agregar.html')
#===Edit===
@proyectos_bp.route('editar/<string:proyecto_id>')
@validar_sesion
def proyectos_edit(brand_id, proyecto_id):
	data = Proyectos.query.filter_by(proyecto_id=proyecto_id).first()
	if data:
		return render_template('sections/proyectos/editar.html', data=data)
	else:
		return 'No se encontraron usuarios con los criterios especificados.'
#===Tendencias===
@proyectos_bp.route('tendencias')
@validar_sesion
def proyectos_tendencias(brand_id):
	proyecto_id = request.values.get('id')
	session['proyecto_id'] = proyecto_id
	return render_template('sections/tendencias/main.html')
#===Save===
@proyectos_bp.route('save', methods=['POST'])
@validar_sesion
def proyectos_save(brand_id):
	if request.method == 'POST':
		proyecto_id = generarCodigo("PRO");
		proyecto_name = request.form.get('proyecto_name')
		proyecto_description = request.form.get('proyecto_description')
		proyecto_estado = 1

		if proyectoExiste(proyecto_name):
			session['mensaje'] = "El proyecto ya existe. Por favor, usa otro nombre."
			return redirect(url_for('proyectos_bp.proyectos_add', brand_id=brand_id))
		else:
			new_data = Proyectos(
				proyecto_id=proyecto_id,
				proyecto_name=proyecto_name,
				proyecto_description=proyecto_description,
				proyecto_estado=proyecto_estado
			)
			db.session.add(new_data)
			db.session.commit()
			session['mensaje'] = "Proyecto creado correctamente."
			return redirect(url_for('proyectos_bp.proyectos_main', brand_id=brand_id))
	return 'Error en el método de solicitud'
#===Update===
@proyectos_bp.route('update', methods=['POST'])
@validar_sesion
def proyectos_update(brand_id):
	if request.method == 'POST':
		proyecto_id = request.form.get('proyecto_id')
		proyecto_name = request.form.get('proyecto_name')
		proyecto_description = request.form.get('proyecto_description')
		proyecto_estado = 1

		if not proyectoExiste(proyecto_name, proyecto_id):
			proyecto = Proyectos.query.filter_by(proyecto_id=proyecto_id).first()
			if proyecto:
				proyecto.proyecto_name=proyecto_name
				proyecto.proyecto_description=proyecto_description
				db.session.commit()
			session['mensaje'] = "Se actualizaron los datos"
			return redirect('editar?id=' + str(proyecto_id))
		else:
			session['mensaje'] = "El proyecto ya existe. Por favor, usa otro nombre."+str(proyectoExiste(proyecto_name))
			return redirect('editar?id=' + str(proyecto_id))
	return 'Error en el método de solicitud'
#===Delete===
@proyectos_bp.route('delete')
@validar_sesion
def proyectos_delete(brand_id):
	proyecto_id = request.values.get('id')
	proyecto = Proyectos.query.filter_by(proyecto_id=proyecto_id).first()
	if proyecto:
		proyecto.proyecto_estado = 0
		db.session.commit()
	return redirect('/proyectos')

#===Recovery===
@proyectos_bp.route('recovery')
@validar_sesion
def proyectos_recovery(brand_id):
	proyecto_id = request.values.get('id')
	proyecto = Proyectos.query.filter_by(proyecto_id=proyecto_id).first()
	if proyecto:
		proyecto.proyecto_estado = 1
		db.session.commit()
	return redirect('papelera')
#===Paginas===
@proyectos_bp.route('/')
@validar_sesion
def proyectos_main(brand_id):
	mensaje = session.pop('mensaje', None)
	return render_template('sections/proyectos/listado.html', mensaje=mensaje)
#===Listado Ajax===
@proyectos_bp.route('listado-ajax', methods=['GET', 'POST'])
@validar_sesion
def proyectos_listarAjax(brand_id):
	try:
		if request.method in ['GET', 'POST']:
			buscar = request.values.get('buscar')
			query = Proyectos.query.filter(
				Proyectos.proyecto_estado == 1
			)
			if buscar:
				query = query.filter(
					Proyectos.proyecto_name.like(f'%{buscar}%')
				)
			query = query.order_by(Proyectos.proyecto_id)
			lista = query.all()
			if lista:
				return render_template('sections/proyectos/listado-ajax.html', lista=lista, brand_id=brand_id)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Papelera===
@proyectos_bp.route('papelera')
@validar_sesion
def proyectos_papelera(brand_id):
	return render_template('sections/proyectos/papelera.html')
#===Papelera Ajax===
@proyectos_bp.route('papelera-ajax', methods=['GET', 'POST'])
@validar_sesion
def users_papeleraAjax(brand_id):
	if request.method in ['GET', 'POST']:
		buscar = request.values.get('buscar')
		query = Proyectos.query.filter(
			Proyectos.proyecto_estado == 0
		)
		if buscar:
			query = query.filter(Proyectos.user_name.like(f'%{buscar}%'))
		lista = query.all()
		if lista:
			return render_template('sections/proyectos/papelera-ajax.html', lista=lista)
		else:
			return 'No se encontraron campañas con los criterios especificados.'
	return 'Error en el método de solicitud'
#===Funciones Auxiliares===
def proyectoExiste(data_name, data_id=None):
	query = Proyectos.query.filter_by(proyecto_name=data_name)
	if data_id:
		query = query.filter(Proyectos.proyecto_id != data_id)
	result = query.first()
	return result is not None
