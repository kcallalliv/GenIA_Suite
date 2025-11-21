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
from routes.models import db, Assets, Assetsbrand, Configuracion
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

bcolors_bp = Blueprint('bcolors_bp', __name__, url_prefix='/brand')

#===Listado===
@bcolors_bp.route('/<string:brand_id>/colors/')
@validar_sesion
def bkimages_main(brand_id):
	lista = listarLogos(brand_id)
	return render_template('sections/brand/colors/main.html',lista= lista)
#===Listado===
@bcolors_bp.route('/<string:brand_id>/colors/list')
@validar_sesion
def bkimages_list(brand_id):
	lista = listarLogos(brand_id)
	return render_template('sections/brand/colors/list.html',lista= lista)
#===User Save===
@bcolors_bp.route('/<string:brand_id>/colors/save', methods=["GET", "POST"])
@validar_sesion
def bkimages_save(brand_id):
	if request.method == 'POST':
		colors_json = request.form.get('colors')
		if not colors_json:
			return jsonify({"status": "error", "message": "No se recibieron datos de colores."}), 400
		try:
			colors_array = json.loads(colors_json)
		except json.JSONDecodeError:
			return jsonify({"status": "error", "message": "Formato JSON de colores inválido."}), 400
		#Update estado a "0"
		Assetsbrand.query.filter_by(asset_type='colors').update({'asset_estado': 0})
		# Itera sobre el array de colores para procesar cada uno
		for color_data in colors_array:
			color_id = color_data.get('id')
			color_value = color_data.get('color')
			print(f"Procesando Color ID: {color_id} color: {color_value}")
			#Si existe el did
			if color_id:
				dataupdate = Assetsbrand.query.filter_by(asset_id=color_id).first()
				if dataupdate:
					dataupdate.asset_name = color_value 
					dataupdate.asset_value = color_value
					dataupdate.asset_fecha = fechaActual()
					dataupdate.asset_estado = 1
			else:
				asset_id = generarCodigo("AST")
				asset_name = color_value
				asset_src = ""
				asset_value = color_value
				asset_type = "colors"
				asset_ext = ""
				asset_fecha = fechaActual()
				asset_estado = "1"
				# Crea un nuevo objeto Assets para cada color y lo guarda en la DB
				new_data = Assetsbrand(
					asset_id = asset_id,
					asset_name = asset_name,
					asset_src = asset_src,
					asset_value = asset_value,
					asset_type = asset_type,
					asset_ext = asset_ext,
					asset_fecha = asset_fecha,
					asset_estado = asset_estado,
					brand_id=brand_id
				)
				db.session.add(new_data)
		# Realiza el commit una sola vez después de agregar todos los elementos
		db.session.commit()
		return jsonify({"status": "success", "message": "Colores guardados correctamente."})
	# Si la solicitud no es POST, redirige o retorna un mensaje de error
	return jsonify({"status": "error", "message": "Método no permitido. Use POST."}), 405

def listarLogos(brand_id):
	try:
		query = Assetsbrand.query.filter_by(asset_type='colors',asset_estado=1,brand_id=brand_id)
		lista = query.all()
		return lista
	except Exception as e:
		return jsonify({"error": str(e)}), 500