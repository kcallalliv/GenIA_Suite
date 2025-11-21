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
from routes.models import db, Configuracion, Links, Proyectos
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion

integraciones_bp = Blueprint('integraciones_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/integraciones/')

#===Listado===
@integraciones_bp.route('/')
@validar_sesion
def integracion_main(brand_id,proyecto_id):
	data = Proyectos.query.filter_by(proyecto_id=proyecto_id).first()
	json_integra = data.proyecto_integraciones
	#Config
	query = Configuracion.query.filter_by(conf_type='integracion')
	lista = query.all()
	return render_template('sections/integraciones/main.html',
		pid=proyecto_id,json_integra=json_integra,config=lista,integrationStatus=integrationStatus,integrationStatusCheck=integrationStatusCheck,verEstado=verEstado)
#save
@integraciones_bp.route('save', methods=['GET', 'POST'])
@validar_sesion
def integracion_save(brand_id,proyecto_id):
	pid = request.form.get('pid')
	integrations = {}
	for key, value in request.form.items():
		if key.startswith('integrations['):
			match = re.search(r'\[(\d+)\]\[(\w+)\]', key)
			if match:
				index = int(match.group(1))
				field = match.group(2)
				if index not in integrations:
					integrations[index] = {}
				integrations[index][field] = value
				
	integrations_list = [integrations[i] for i in sorted(integrations.keys())]
	integraciones_json_str = json.dumps(integrations_list)
	try:
		proyecto = Proyectos.query.filter_by(proyecto_id=pid).first()
		if proyecto:
			proyecto.proyecto_integraciones = integraciones_json_str
			db.session.commit()
			
			return jsonify({
				"pid": pid,
				"integrations_saved": integrations_list,
				"status": "success",
				"message": "Integraciones guardadas correctamente."
			})
		else:
			return jsonify({"status": "error", "message": f"Proyecto con ID {pid} no encontrado."}), 404

	except Exception as e:
		# Esto capturará errores de base de datos o de consulta
		db.session.rollback()
		return jsonify({"status": "error", "message": f"Error al guardar las integraciones: {str(e)}"}), 500
def integrationStatus(integrations_data, conf_value):
	integrations_list = []	
	if isinstance(integrations_data, str):
		try:
			integrations_list = json.loads(integrations_data)
		except json.JSONDecodeError:
			return "json_error"
	elif isinstance(integrations_data, list):
		integrations_list = integrations_data
	else:
		return "inactive"
	if isinstance(integrations_list, list):
		for item in integrations_list:
			if isinstance(item, dict) and item.get("value") == conf_value:
				return item.get("status", "N/A")
	return "inactive"
def integrationStatusCheck(integrations_data, conf_value):
	integrations_list = []	
	if isinstance(integrations_data, str):
		try:
			integrations_list = json.loads(integrations_data)
		except json.JSONDecodeError:
			return "json_error"
	elif isinstance(integrations_data, list):
		integrations_list = integrations_data
	else:
		return ""
	if isinstance(integrations_list, list):
		for item in integrations_list:
			if isinstance(item, dict) and item.get("value") == conf_value:
				return "checked"
	return ""
def verEstado(valor):
	if valor == 1:
		result = "active"
	elif valor == 0:
		result = "inactive"
	else:
		result = "desconocido"  # O el valor que prefieras para casos no manejados
	return result