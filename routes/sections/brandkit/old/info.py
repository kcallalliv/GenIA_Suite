# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime
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
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_brands

bkinfo_bp = Blueprint('bkinfo_bp', __name__)

#===Listado===
@bkinfo_bp.route('/brandkit/info')
def bklogos_main():
	brand_id = "3396b5a9efac4ca8b4c93f5a1cff4415"
	query = f"SELECT * FROM `{bq_table_brands}` WHERE brand_id = '{brand_id}'"
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		data = [dict(row.items()) for row in results]
		if data:
			valor_pais = data[0]['brand_pais']
			valor_industria = data[0]['brand_subindustria']
			selectPais_html = selectPais(valor_pais)
			selectIndustria_html = selectIndustria(valor_industria)
			return render_template('sections/brandkit/info/main.html',data=data,selectPais=selectPais_html,selectIndustria=selectIndustria_html)
		else:
			return 'No se encontraron usuarios con los criterios especificados.'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===User Save===
@bkinfo_bp.route("/brandkit/info/update", methods=["GET", "POST"])
def bkbrand_update():
	if request.method == 'POST':
		brand_id = request.form.get('brand_id')
		brand_name = request.form.get('brand_name')
		brand_pais = request.form.get('brand_pais')
		brand_industria = request.form.get('brand_industria')
		brand_description = request.form.get('brand_description')
		brand_estado = "1"
		data_info = {
			"brand_id": brand_id,
			"brand_name": brand_name,
			"brand_pais": brand_pais,
			"brand_industria": brand_industria,
			"brand_description": brand_description,
			"brand_estado": brand_estado
		}
		status_code = bkbrand_upsert(data_info)
		#return 'No se encontraron usuarios con los criterios especificados.'
		#return {"message": f"Hubo un error al procesar el registro: {status_code}"}
		return redirect('/brandkit/info')
	else:
		return 'No se encontraron los campos'
	#return redirect('/brandkit/info')
def bkbrand_upsert(data_info):
	# Variables de prueba
	brand_id = data_info.get("brand_id")
	brand_name = data_info.get("brand_name")
	brand_pais = data_info.get("brand_pais")
	brand_industria = data_info.get("brand_industria")
	brand_description = data_info.get("brand_description")
	brand_estado = data_info.get("brand_estado")
	try:
		sql_query = f"""
		MERGE INTO `{bq_table_brands}` AS T
		USING (
			SELECT
				'{brand_id}' AS brand_id,
				'{brand_name}' AS brand_name,
				'{brand_pais}' AS brand_pais,
				'{brand_industria}' AS brand_subindustria,
				'{brand_description}' AS brand_description,
				'{brand_estado}' AS brand_estado
		) AS S
		ON T.brand_id = S.brand_id
		WHEN MATCHED THEN
			UPDATE SET
				brand_name = S.brand_name,
				brand_pais = S.brand_pais,
				brand_subindustria = S.brand_subindustria,
				brand_description = S.brand_description,
				brand_estado = S.brand_estado
		WHEN NOT MATCHED THEN
			INSERT (brand_id, brand_name, brand_pais, brand_subindustria, brand_description, brand_estado)
			VALUES(S.brand_id, S.brand_name, S.brand_pais, S.brand_subindustria, S.brand_description, S.brand_estado)
		"""
		query_job = bq_client.query(sql_query)
		query_job.result()
		return {"status": "success", "message": "El registro se procesó exitosamente."}
	except Exception as e:
		return {"status": "error", "message": f"Hubo un error al procesar el registro: {e}"}
#=============================
#===Otras funcionabilidades===
#=============================
def selectPais(myvalor=None):
	query = f"SELECT * FROM `{bq_table_config}` WHERE conf_type='brand_pais'"
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		listado = [dict(row.items()) for row in results]
		# Select
		html_select = "<select class='form-select' id='brand_pais' name='brand_pais'>"
		html_select += "<option value='' selected disabled hidden>Selecciona un país</option>"
		
		for pais_data in listado:
			valor = pais_data.get('conf_value', '')
			nombre = pais_data.get('conf_name', '')
			selected = "selected" if myvalor == valor else ""
			html_select += f"<option value='{nombre}' {selected}>{valor.capitalize()}</option>"
		html_select += "</select>"

		# Retornar el HTML generado
		return html_select
	except Exception as e:
		print("ERROR EJECUTANDO CONSULTA BIGQUERY:")
		traceback.print_exc()  # Muestra el error completo en el log
		return f"Error al ejecutar la consulta de BigQuery: {e}", 500
def selectIndustria(myvalor=None):
	query = f"SELECT * FROM `{bq_table_config}` WHERE conf_type='brand_industria'"
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		listado = [dict(row.items()) for row in results]
		# Select
		html_select = "<select class='form-select' id='brand_industria' name='brand_industria'>"
		html_select += "<option value='' selected disabled hidden>Selecciona industria</option>"
		
		for pais_data in listado:
			valor = pais_data.get('conf_value', '')
			nombre = pais_data.get('conf_name', '')
			selected = "selected" if myvalor == valor else ""
			html_select += f"<option value='{nombre}' {selected}>{valor.capitalize()}</option>"
		html_select += "</select>"

		# Retornar el HTML generado
		return html_select
	except Exception as e:
		print("ERROR EJECUTANDO CONSULTA BIGQUERY:")
		traceback.print_exc()  # Muestra el error completo en el log
		return f"Error al ejecutar la consulta de BigQuery: {e}", 500
def generate_cod_id():
	new_uuid = uuid.uuid4()
	return new_uuid.hex