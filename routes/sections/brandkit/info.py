# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased
import os
import json
import re
import hashlib
import difflib
import requests
import random
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
from routes.models import db, Brands, Configuracion
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_brands, validar_sesion

bkdash_bp = Blueprint('bkdash_bp', __name__)
bkinfo_bp = Blueprint('bkinfo_bp', __name__, url_prefix='/brand')
#===Dashboard===
@bkdash_bp.route('/dashboard')
@validar_sesion
def bkdash_main():
	try:
		query = Brands.query.filter_by(brand_estado=1)
		lista = query.all()
		if lista:
			return render_template('sections/dashboard.html',lista=lista)
		else:
			#logger.debug('Usuario o contraseña incorrectos')
			#return redirect('/')
			return 'No se encontraron usuarios con los criterios especificados.'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Listado===
@bkinfo_bp.route('/<string:brand_id>/info/')
@validar_sesion
def bkinfo_main(brand_id):
	#brand_id = "BRD1fY24W5"
	try:
		data = Brands.query.filter_by(brand_id=brand_id).first()
		if data:
			valor_pais = data.brand_pais
			valor_industria = data.brand_subindustria
			selectPais_html = selectPais(valor_pais)
			selectIndustria_html = selectIndustria(valor_industria)
			return render_template('sections/brandkit/info/main.html',data=data,selectPais=selectPais_html,selectIndustria=selectIndustria_html)
		else:
			#logger.debug('Usuario o contraseña incorrectos')
			#return redirect('/')
			return 'No se encontraron usuarios con los criterios especificados.'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===User Save===
@bkinfo_bp.route("/<string:brand_id>/info/update", methods=["GET", "POST"])
@validar_sesion
def bkbrand_update(brand_id):
	if request.method == 'POST':
		brand_id = request.form.get('brand_id')
		brand_name = request.form.get('brand_name')
		brand_pais = request.form.get('brand_pais')
		brand_industria = request.form.get('brand_industria')
		brand_description = request.form.get('brand_description')
		brand_estado = "1"
		#save
		data = Brands.query.filter_by(brand_id=brand_id).first()
		if data:
			data.brand_name = brand_name
			data.brand_pais = brand_pais
			data.brand_subindustria = brand_industria
			data.brand_description = brand_description
			db.session.commit()
		#return {"message": f"Hubo un error al procesar el registro: {status_code}"}
		#return redirect('/brand/<string:brand_id>/info/')
		return redirect(f"/brand/{brand_id}/info/")
	else:
		return 'No se encontraron los campos'
#=============================
#===Otras funcionabilidades===
#=============================
def selectPais(myvalor=None):
	try:
		query = Configuracion.query.filter_by(conf_type='brand_pais',conf_estado=1)
		lista = query.all()
		html_select = "<select class='form-select' id='brand_pais' name='brand_pais'>"
		html_select += "<option value='' selected disabled hidden>Selecciona industria</option>"
		for item in lista:
			item_value = item.conf_value
			item_name = item.conf_name
			selected = "selected" if myvalor == item_name else ""
			html_select += f"<option value='{item_name}' {selected}>{item_value.capitalize()}</option>"
		html_select += "</select>"
		return html_select
	except Exception as e:
		traceback.print_exc()  # Muestra el error completo en el log
		return f"Error al ejecutar la consulta de sql: {e}", 500
def selectIndustria(myvalor=None):
	try:
		query = Configuracion.query.filter_by(conf_type='brand_industria')
		lista = query.all()
		html_select = "<select class='form-select' id='brand_industria' name='brand_industria'>"
		html_select += "<option value='' selected disabled hidden>Selecciona industria</option>"
		for item in lista:
			item_value = item.conf_value
			item_name = item.conf_name
			selected = "selected" if myvalor == item_name else ""
			html_select += f"<option value='{item_name}' {selected}>{item_value.capitalize()}</option>"
		html_select += "</select>"
		return html_select
	except Exception as e:
		traceback.print_exc()  # Muestra el error completo en el log
		return f"Error al ejecutar la consulta de sql: {e}", 500
def generate_cod_id():
	new_uuid = uuid.uuid4()
	return new_uuid.hex