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
from routes.models import db, Assets, Configuracion
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion, fechaActual

bkcolors_bp = Blueprint('bkcolors_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/brandkit/colors/')

#===Listado===
@bkcolors_bp.route('/')
@validar_sesion
def bkcolors_main(brand_id,proyecto_id):
	pid = proyecto_id
	lista = listarLogos(pid)
	return render_template('sections/brandkit/colors/main.html',lista= lista,generar_url_firmada=generar_url_firmada,pid=pid)

#===User Save===
@bkcolors_bp.route("save", methods=["GET", "POST"])
@validar_sesion
def bkcolors_save(brand_id,proyecto_id):
	if request.method == 'POST':
		pid = request.form.get('pid')
		colors_json = request.form.get('colors')
		if not colors_json:
			return jsonify({"status": "error", "message": "No se recibieron datos de colores."}), 400
		try:
			colors_array = json.loads(colors_json)
		except json.JSONDecodeError:
			return jsonify({"status": "error", "message": "Formato JSON de colores inválido."}), 400
		#Update estado a "0"
		Assets.query.filter_by(asset_type='colors').update({'asset_estado': 0})
		# Itera sobre el array de colores para procesar cada uno
		for color_data in colors_array:
			color_id = color_data.get('id')
			color_value = color_data.get('color')
			#Si existe el did
			if color_id:
				data = Assets.query.filter_by(asset_id=color_id).first()
				if data:
					data.asset_name = color_value
					data.asset_value = color_value
					data.asset_fecha = fechaActual()
					data.asset_estado = 1
			else:
				asset_name = color_value
				asset_src = ""
				asset_value = color_value
				asset_type = "colors"
				asset_ext = ""
				asset_fecha = fechaActual()
				asset_estado = "1"
				session_id = pid
				# Crea un nuevo objeto Assets para cada color y lo guarda en la DB
				new_data = Assets(
					asset_name = asset_name,
					asset_src = asset_src,
					asset_value = asset_value,
					asset_type = asset_type,
					asset_ext = asset_ext,
					asset_fecha = asset_fecha,
					asset_estado = asset_estado,
					proyecto_id = session_id
				)
				db.session.add(new_data)
		# Realiza el commit una sola vez después de agregar todos los elementos
		db.session.commit()
		return jsonify({"status": "success", "message": "Colores guardados correctamente."})
	# Si la solicitud no es POST, redirige o retorna un mensaje de error
	return jsonify({"status": "error", "message": "Método no permitido. Use POST."}), 405

def generar_url_firmada(bucket_name, blob_name):
	bucket = storage_client.bucket(bucket_name)
	blob_path = f"fonts/{blob_name}"
	blob = bucket.blob(blob_path)
	url = blob.generate_signed_url(
		version="v4",
		expiration=datetime.timedelta(minutes=15),
		method="GET",
	)
	#url = blob.generate_signed_url(expiration=3600)
	return url
def listarLogos(data_id):
	try:
		query = Assets.query.filter_by(asset_type='colors',asset_estado=1,proyecto_id=data_id)
		lista = query.all()
		return lista
	except Exception as e:
		return jsonify({"error": str(e)}), 500