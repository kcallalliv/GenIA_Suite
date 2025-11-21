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
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_brands, validar_sesion

bkbrands_bp = Blueprint('bkbrands_bp', __name__)

#===Listado===
@bkbrands_bp.route('/brandkit/brands')
@validar_sesion
def bklogos_main():
	return render_template('sections/usuarios/listado.html')

@bkbrands_bp.route("/brandkit/brands/update", methods=["GET", "POST"])
@validar_sesion
def bkbrand_upsert():
	# Variables de prueba
	brand_name = "claro peru new"
	brand_pais = "peru"
	brand_subindustria = "telecomunicaciones"
	brand_description = "es una empresa de telecomunicaciones"
	brand_estado = "1"
	# ID del registro a actualizar (o insertar si no existe)
	# Si quieres que se inserte una nueva fila, genera un nuevo ID.
	brand_id = "3396b5a9efac4ca8b4c93f5a1cff4415"
	#brand_id = generate_cod_id()

	try:
		sql_query = f"""
		MERGE INTO `{bq_table_brands}` AS T
		USING (
			SELECT
				'{brand_id}' AS brand_id,
				'{brand_name}' AS brand_name,
				'{brand_pais}' AS brand_pais,
				'{brand_subindustria}' AS brand_subindustria,
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

@bkbrands_bp.route("/brandkit/config/update", methods=["GET", "POST"])
@validar_sesion
def bkconfig_upsert():
	# Variables de prueba
	"""
	conf_name = "argentina"
	conf_value = "argentina"
	conf_symbol = ""
	conf_type = "brand_pais"
	conf_estado = "1"
	"""
	conf_name = "medios_entretenimiento"
	conf_value = "medios y entretenimiento"
	conf_symbol = ""
	conf_type = "brand_industria"
	conf_estado = "1"
	# ID del registro a actualizar (o insertar si no existe)
	# Si quieres que se inserte una nueva fila, genera un nuevo ID.
	conf_id = "074c5f1107bd403e91978e7c9e30764c"
	#conf_id = generate_cod_id()

	try:
		sql_query = f"""
		MERGE INTO `{bq_table_config}` AS T
		USING (
			SELECT
				'{conf_id}' AS conf_id,
				'{conf_name}' AS conf_name,
				'{conf_value}' AS conf_value,
				'{conf_symbol}' AS conf_symbol,
				'{conf_type}' AS conf_type,
				'{conf_estado}' AS conf_estado
		) AS S
		ON T.conf_id = S.conf_id
		WHEN MATCHED THEN
			UPDATE SET
				conf_name = S.conf_name,
				conf_value = S.conf_value,
				conf_symbol = S.conf_symbol,
				conf_type = S.conf_type,
				conf_estado = S.conf_estado
		WHEN NOT MATCHED THEN
			INSERT (conf_id, conf_name, conf_value, conf_symbol, conf_type, conf_estado)
			VALUES(S.conf_id, S.conf_name, S.conf_value, S.conf_symbol, S.conf_type, S.conf_estado)
		"""
		query_job = bq_client.query(sql_query)
		query_job.result()
		return {"status": "success", "message": "El registro se procesó exitosamente."}
	except Exception as e:
		return {"status": "error", "message": f"Hubo un error al procesar el registro: {e}"}
def generate_cod_id():
	new_uuid = uuid.uuid4()
	return new_uuid.hex