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
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client

bkimages_bp = Blueprint('bkimages_bp', __name__)

#fecha
tz_pe = pytz.timezone('America/Lima')
my_fecha = datetime.datetime.now(tz=tz_pe)
my_fecha_str = my_fecha.strftime('%Y-%m-%d %H:%M:%S')
#===Listado===
@bkimages_bp.route('/brandkit/images')
def bkimages_main():
	url_del_logo = generar_url_firmada("genia_information", "20250830_usuario_ejemplo_053ee4581fd34f5f829627253f88ea15.jpg")
	print(f"URL firmada para 'mi_logo.png': {url_del_logo}")
	print(datetime.datetime.now())
	lista = listarImages()
	return render_template('sections/brandkit/images/main.html',logo=url_del_logo, lista= lista,generar_url_firmada=generar_url_firmada)
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
	query = f"SELECT * FROM `{bq_table_assets}` WHERE asset_type = 'images'"
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		data = [dict(row.items()) for row in results]
		return data
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===User Save===
@bkimages_bp.route("/brandkit/images/save", methods=["GET", "POST"])
def bkimages_save():
	if request.method == 'POST':
		# El nombre del campo debe coincidir con el del frontend (formData.append('photos[]', file))
		uploaded_files = request.files.getlist("photos[]")

		if not uploaded_files:
			return jsonify({"status": "error", "message": "No se encontraron archivos en la solicitud."}), 400

		responses = []
		for file in uploaded_files:
			# Asume que 'uploader' es una variable de tu sesión o request
			# Por ahora, se usa un valor estático
			uploader_name = "usuario_ejemplo" 
			upload_response = gsfile_upload(file, uploader_name)
			responses.append(upload_response)
		
		# Opcional: Registrar metadatos en BigQuery para el lote completo si se necesita.
		# Por ahora, el registro se hace por cada archivo en gsfile_upload()

		return jsonify({"status": "success", "message": "Proceso de subida completado.", "results": responses})
	
	# Si la solicitud no es POST, redirige o retorna un mensaje de error
	return jsonify({"status": "error", "message": "Método no permitido. Use POST."}), 405
def gsfile_upload(file, uploader):
	"""Sube un solo archivo a Cloud Storage y registra metadatos en BigQuery."""
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
		blob.upload_from_file(file)
		#datos
		asset_id = generate_cod_id()
		asset_name = file.filename
		asset_value = name_archivo
		asset_src = name_fileext
		asset_type = "images"
		asset_fecha = my_fecha_str
		asset_estado = "1"
		data_info = {
			"asset_id": asset_id,
			"asset_name": asset_name,
			"asset_src": asset_src,
			"asset_value": asset_value,
			"asset_type": asset_type,
			"asset_fecha": asset_fecha,
			"asset_estado": asset_estado
		}
		status_code = bkassets_upsert(data_info)

		# Registrar en BigQuery (Ajusta la tabla si es necesario, BQ_TABLE no está definida en el original)
		# bq_client.insert_rows_json(BQ_TABLE, [{
		#     "file_name": nombre_archivo,
		#     "upload_time": datetime.datetime.utcnow().isoformat(),
		#     "uploader": uploader
		# }])

		return {"status": "success", "message": f"{status_code} Archivo {nombre_archivo} subido correctamente"}
	except Exception as e:
		return {"status": "error", "message": f"Error al subir el archivo: {e}"}
def bkassets_upsert(data_info):
	# Variables de prueba
	asset_id = data_info.get("asset_id")
	asset_name = data_info.get("asset_name")
	asset_src = data_info.get("asset_src")
	asset_value = data_info.get("asset_value")
	asset_type = data_info.get("asset_type")
	asset_fecha = data_info.get("asset_fecha")
	asset_estado = data_info.get("asset_estado")
	try:
		sql_query = f"""
		MERGE INTO `{bq_table_assets}` AS T
		USING (
			SELECT
				@asset_id AS asset_id,
				@asset_name AS asset_name,
				@asset_src AS asset_src,
				@asset_value AS asset_value,
				@asset_type AS asset_type,
				@asset_estado AS asset_estado,
				@asset_fecha AS asset_fecha
		) AS S
		ON T.asset_id = S.asset_id
		WHEN MATCHED THEN
			UPDATE SET
				asset_name = S.asset_name,
				asset_src = S.asset_src,
				asset_value = S.asset_value,
				asset_type = S.asset_type,
				asset_estado = S.asset_estado,
				asset_fecha = S.asset_fecha
		WHEN NOT MATCHED THEN
			INSERT (asset_id, asset_name, asset_src, asset_value, asset_type, asset_estado, asset_fecha) 
			VALUES (S.asset_id, S.asset_name, S.asset_src, S.asset_value, S.asset_type, S.asset_estado, S.asset_fecha)
		"""
		job_config = bigquery.QueryJobConfig(
			query_parameters=[
				bigquery.ScalarQueryParameter("asset_id", "STRING", asset_id),
				bigquery.ScalarQueryParameter("asset_name", "STRING", asset_name),
				bigquery.ScalarQueryParameter("asset_src", "STRING", asset_src),
				bigquery.ScalarQueryParameter("asset_value", "STRING", asset_value),
				bigquery.ScalarQueryParameter("asset_type", "STRING", asset_type),
				bigquery.ScalarQueryParameter("asset_estado", "STRING", asset_estado),
				# Pasar el objeto datetime a la consulta
				bigquery.ScalarQueryParameter("asset_fecha", "TIMESTAMP", asset_fecha),
			]
		)
		query_job = bq_client.query(sql_query,job_config=job_config)
		query_job.result()
		return {"status": "success", "message": "El registro se procesó exitosamente."}
	except Exception as e:
		return {"status": "error", "message": f"Hubo un error al procesar el registro: {e}"}
def generate_cod_id():
	new_uuid = uuid.uuid4()
	return new_uuid.hex