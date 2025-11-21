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
from routes.config.geniaconfig import bq_client, BQ_TABLE_USERS

geniausers_bp = Blueprint('geniausers_bp', __name__)

#===Listado===
@geniausers_bp.route('/usuarios')
def gusers_user_list():
	return render_template('sections/usuarios/listado.html')
#===Listado Ajax===
@geniausers_bp.route('/usuarios/listado-ajax', methods=['GET', 'POST'])
def gusers_user_listAjax():
	if request.method in ['GET', 'POST']:
		#buscar = request.values.get('buscar')
		buscar = "";
		query_parts = [
			f"SELECT * FROM prd-claro-mktg-data-storage.genia_information.users",
			"WHERE user_estado = '1' AND user_permiso != 'superadmin'"
		]
		if buscar:
			query_parts.append(f"AND user_name LIKE '%{buscar}%'")
		query = " ".join(query_parts)
		try:
			query_job = bq_client.query(query)
			results = query_job.result()
			listado = [dict(row.items()) for row in results]
			if listado:
				return render_template('sections/usuarios/listado-ajax.html', listado=listado,generate_custom_id=generate_user_id)
			else:
				return 'No se encontraron usuarios con los criterios especificados.'
		except Exception as e:
			print(f"Ocurrió un error al ejecutar la consulta: {e}")
			return 'Error en la solicitud.'
	return 'Error en el método de solicitud'
#===User Save===
@geniausers_bp.route("/usuarios/save", methods=["GET", "POST"])
def gusers_user_save():
	user_name = "admin"
	user_phone = "987654321";
	user_email = "admin@csalatam.com"
	user_pass = "admin"
	user_passmd5 = encMD5(user_pass)
	user_permiso = "admin"
	user_estado = "1"

	try:
		# Registrar en BigQuery
		bq_client.insert_rows_json(bq_table_users, [{
			"user_id":generate_user_id,
			"user_name":user_name,
			"user_phone":user_phone,
			"user_email":user_email,
			"user_pass":user_passmd5,
			"user_permiso":user_permiso,
			"user_estado":user_estado
		}])
		return {"status": "success", "message": "El usuario se subió exitosamente."}
	except Exception as e:
		# Retorna un diccionario con un estado de error
		return {"status": "error", "message": f"Hubo un error al subir el usuario: {e}"}

def generate_user_id():
    new_uuid = uuid.uuid4()
    return new_uuid.hex

def encMD5(password):
	password_bytes = password.encode('utf-8')
	md5_hash = hashlib.md5()
	md5_hash.update(password_bytes)
	hashed_password = md5_hash.hexdigest()
	return hashed_password