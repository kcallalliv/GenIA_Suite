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
from routes.models import db, Assets, Assetsbrand, Configuracion
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

bimages_bp = Blueprint('bimages_bp', __name__, url_prefix='/brand')
base_api_url = "https://backend-api-1079186964678.us-central1.run.app"

#===Main===
@bimages_bp.route('/<string:brand_id>/images/')
@validar_sesion
def bkimages_main(brand_id):
	lista = listarImages()
	return render_template('sections/brand/images/main.html',lista= lista,generar_url_firmada=generar_url_firmada)
#===Listado===
@bimages_bp.route('/<string:brand_id>/images/list')
@validar_sesion
def bkimages_list(brand_id):
	lista = listarImages()
	return render_template('sections/brand/images/list.html',lista= lista,generar_url_firmada=generar_url_firmada)
def generar_url_firmada(bucket_name, blob_name):
	bucket = storage_client.bucket(bucket_name)
	blob_path = f"images/{blob_name}"
	blob = bucket.blob(blob_path)
	url = blob.generate_signed_url(
		version="v4",
		expiration=datetime.timedelta(minutes=15),
		method="GET",
	)
	#url = blob.generate_signed_url(expiration=3600)
	return url
def listarImages():
	try:
		query = Assetsbrand.query.filter_by(asset_type='images',asset_estado=1)
		lista = query.all()
		return lista
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===User Save===
@bimages_bp.route("/<string:brand_id>/images/save", methods=["GET", "POST"])
@validar_sesion
def bkimages_save(brand_id):
	if request.method == 'POST':
		existe_cambios = 0
		pid = request.form.get('pid')
		data_info = request.form.get('data_info')
		uploaded_files = request.files.getlist("photos[]")
		# Proceso de actualización
		if data_info:
			files_array = json.loads(data_info)
			# 1. Primero, actualiza todos los registros existentes a '0' en una sola consulta
			Assetsbrand.query.filter_by(asset_type='images').update({'asset_estado': 0})
			# 2. Recolecta los IDs de los registros que deben ser '1'
			ids_a_actualizar = []
			for item_data in files_array:
				item_id = item_data.get('id')
				if item_id:
					ids_a_actualizar.append(item_id)
			# 3. Realiza una única actualización en lote para poner '1' solo en los IDs recolectados
			if ids_a_actualizar:
				Assetsbrand.query.filter(Assetsbrand.asset_id.in_(ids_a_actualizar)).update(
					{"asset_estado": 1},
					synchronize_session='fetch'
				)
				existe_cambios = len(ids_a_actualizar)
			db.session.commit()
		# Proceso de archivos
		if not uploaded_files or not uploaded_files[0].filename:
			if existe_cambios > 0:
				return jsonify({"status": "success", "message": "Registros actualizados."})
			else:
				return jsonify({"status": "error", "message": "No se encontraron archivos en la solicitud."}), 400
		else:
			responses = []
			for file in uploaded_files:
				session_name = session['usuario']
				uploader_name = session_name.replace(".", "")
				#uploader_name = "usuario_ejemplo"
				upload_response = gsfile_upload(file, uploader_name, brand_id)
				responses.append(upload_response)
			return jsonify({"status": "success", "message": "Proceso de subida completado.", "results": responses})
	
	return jsonify({"status": "error", "message": "Método no permitido. Use POST."}), 405
def gsfile_upload(file, uploader,brand_id):
	try:
		if not file:
			return {"status": "error", "message": "No se proporcionó un archivo."}

		ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
		fecha = datetime.datetime.utcnow().strftime('%Y%m%d')
		name_archivo = f"{fecha}_{uploader}_{uuid.uuid4().hex}"
		name_fileext = f"{name_archivo}.{ext}"
		nombre_archivo = f"images/{name_fileext}"
		# Subir a Cloud Storage
		bucket = storage_client.bucket(bucket_name)
		blob = bucket.blob(nombre_archivo)
		file.seek(0)
		blob.upload_from_file(file)
		# 2. Llamar a la API de análisis
		api_result = procesar_file_ingest(file)
		# 3. Serializar el resultado para guardar en la DB
		if api_result.get('status') == 'success':
			asset_json_string = json.dumps(api_result)
			message = f"Archivo {nombre_archivo} subido y analizado."
		else:
			asset_json_string = json.dumps(api_result)
			message = f"Archivo subido, pero falló el análisis de la API."
		#datos
		asset_id = generarCodigo("AST")
		asset_name = file.filename
		asset_value = name_archivo
		asset_src = name_fileext
		asset_type = "images"
		asset_ext = ext
		asset_fecha = fechaActual()
		asset_estado = 1
		#save
		new_data = Assetsbrand(
			asset_id = asset_id,
			asset_name = asset_name,
			asset_src = asset_src,
			asset_value = asset_value,
			asset_type = asset_type,
			asset_ext = asset_ext,
			asset_fecha = asset_fecha,
			asset_estado = asset_estado,
			asset_tags = asset_json_string,
			brand_id=brand_id
		)
		db.session.add(new_data)
		db.session.commit()
		return {"status": "success", "message": f"Archivo {nombre_archivo} subido correctamente"}
	except Exception as e:
		return {"status": "error", "message": f"Error al subir el archivo: {e}"}

def procesar_file_ingest(file_object):
	endpoint = f"{base_api_url}/ingest/file"
	if not file_object.filename:
		return {"status": "error", "message": "Objeto de archivo inválido."}
		
	file_name = file_object.filename

	try:
		content_type = file_object.content_type if hasattr(file_object, 'content_type') else 'application/octet-stream'
		file_object.seek(0) 
		files = {'file': (file_name, file_object.stream, content_type)} 
		
		response = requests.post(endpoint, files=files)
		response.raise_for_status() 
		return response.json()
		
	except requests.exceptions.RequestException as e:
		error_detail = str(e)
		if 'response' in locals() and response is not None:
			 error_detail = f"Código {response.status_code}"
		return {"status": "error", "message": "Fallo al subir archivo", "detail": error_detail}
	except Exception as e:
		return {"status": "error", "message": f"Error inesperado: {str(e)}"}