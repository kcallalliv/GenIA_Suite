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
from docx import Document
from bs4 import BeautifulSoup
from docx import Document
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

#import logging
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

def validar_sesion(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'permiso' not in session:
			return redirect('/')
		return f(*args, **kwargs)
	return decorated_function

geniaauth_bp = Blueprint('geniaauth_bp', __name__)

@geniaauth_bp.route('/procesar', methods=['POST'])
def gauth_procesar():
	if request.method == 'POST':
		user_user = request.form.get('txt_usuario')
		user_pass = request.form.get('txt_password')
		user_encpass = encMD5(user_pass)
		try:
			# Construir la consulta SQL para BigQuery
			query = f"""
				SELECT user_id, user_email, user_permiso, user_estado
				FROM `{BQ_TABLE_USERS}`
				WHERE user_email = @user_email AND user_pass = @user_pass AND user_estado = '1'
				LIMIT 1
			""",
			# Usar parámetros para evitar inyección SQL
			query_job = bq_client.query(query,
			job_config=bigquery.QueryJobConfig(
				query_parameters=[
					bigquery.ScalarQueryParameter("user_email", "STRING", user_user),
					bigquery.ScalarQueryParameter("user_pass", "STRING", user_encpass),
				]
			))
			# Ejecutar la consulta y obtener los resultados
			result = query_job.result()
			usuario = next(iter(result), None)
			#logger.debug(f"Objeto de usuario retornado: {usuario}")
			if usuario:
				session['id'] = usuario.user_id
				session['usuario'] = usuario.user_email
				session['permiso'] = usuario.user_permiso
				session['estado'] = usuario.user_estado
				return redirect('/my-perfil')
			else:
				#logger.debug('Usuario o contraseña incorrectos, la consulta no devolvió resultados.')
				return {"status": "error", "message": "Usuario o contraseña incorrectos."}, 401
				#return redirect('/')
		except Exception as e:
			print(f"Error en la consulta de autenticación: {e}")
			return {"status": "error", "message": "Hubo un error en el servidor."}, 500

@geniaauth_bp.route('/logout')
def gauth_logout():
	session.pop('id', None)
	session.pop('usuario', None)
	session.pop('permiso', None)
	session.pop('estado', None)
	return redirect('/')

def encMD5(password):
	password_bytes = password.encode('utf-8')
	md5_hash = hashlib.md5()
	md5_hash.update(password_bytes)
	hashed_password = md5_hash.hexdigest()
	return hashed_password

@geniaauth_bp.route('/my-perfil')
def gauth_perfil():
	user_name = session.get('usuario')
	return render_template("perfil.html",user_name=user_name)