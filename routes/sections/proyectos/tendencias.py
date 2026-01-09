# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from collections import defaultdict
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased
from sqlalchemy import desc, and_
from bs4 import BeautifulSoup
from io import BytesIO
import os
import json
import re
import hashlib
import difflib
import requests
import random
import pytz
import string
import base64
from io import BytesIO
from google.api_core.client_options import ClientOptions
from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
from google import genai
import pandas as pd
import traceback # Asume que pandas está importado
import uuid
#llamar a config
from routes.models import db, Assets, Configuracion, Proyectos, Keywords
from routes.config.geniaconfig import bq_client, bq_table_seo_semrush, bq_table_seo_search, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

ptendencias_bp = Blueprint('ptendencias_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/tendencias/')
#===View===
@ptendencias_bp.route('/test')
@validar_sesion
def tendencias_main(brand_id,proyecto_id):
	return render_template('sections/proyectos/tendencias/main.html')
#===Create===
@ptendencias_bp.route('/', methods=['GET'])
@validar_sesion
def tendencias_dashboard(brand_id,proyecto_id):
	if request.method == 'GET':
		return render_template('sections/proyectos/tendencias/dashboard.html', proyecto_id=proyecto_id)
#===Save===
@ptendencias_bp.route('addkeyword', methods=['POST'])
@validar_sesion
def keyword_save(brand_id,proyecto_id):
	if request.method == 'POST':
		keyword_id = generarCodigo("KEY");
		keyword_pid = request.form.get('pid')
		keyword_name = request.form.get('keyword')
		keyword_estado = 1

		# Normalizar el keyword buscado
		keyword_normalizado = keyword_name.strip().lower() if keyword_name else ""
		encontrado = None
		#Semrush
		lista_semrush = listarSemrush()
		for item in lista_semrush:
			nombre_item = item.get('Keyword', '').strip().lower()
			if nombre_item == keyword_normalizado:
				encontrado = {
					'keyword': item.get('Keyword', ''),
					'keyword_metrica_name': 'volumen',
					'keyword_metrica_value': item.get('Search_Volume', 'N/A'),
					'keyword_indicador_name': 'posicion',
					'keyword_indicador_value': item.get('Posicion', 'N/A'), 
					'keyword_fuente': 'semrush'
				}
				break # Detener la búsqueda en Semrush si se encuentra
		#Search Console
		if not encontrado:
			lista_search_console = listarSearcConsole()
			for item in lista_search_console:
				nombre_item = item.get('query', '').strip().lower()
				if nombre_item == keyword_normalizado:
					encontrado = {
						'keyword': item.get('query', ''),
						'keyword_metrica_name': 'impresiones',
						'keyword_metrica_value': item.get('total_impressions', 'N/A'),
						'keyword_indicador_name': 'posicion',
						'keyword_indicador_value': item.get('avg_position_int', 'N/A'), 
						'keyword_fuente': 'google search'
					}
					break # Detener la búsqueda en Search Console
		if not encontrado:
			encontrado = {
				'keyword': keyword_name,
				'keyword_metrica_name': 'N/A',
				'keyword_metrica_value': 0,
				'keyword_indicador_name': 'N/A',
				'keyword_indicador_value': 0, 
				'keyword_fuente': 'custom'
			}
		#Respuesta
		if encontrado:
			# Usamos el diccionario 'encontrado' que ya está normalizado
			keyword = encontrado.get('keyword', 'N/A')
			keyword_metrica_name = encontrado.get('keyword_metrica_name', '')
			keyword_metrica_value = encontrado.get('keyword_metrica_value', '')
			keyword_indicador_name = encontrado.get('keyword_indicador_name', '')
			keyword_indicador_value = encontrado.get('keyword_indicador_value', '')
			keyword_fuente = encontrado.get('keyword_fuente', 'custom')
			# Creamos el HTML con los datos encontrados
			#html = f'\tKeyword: {keyword} | Posición: {posicion} | Métrica: {metrica} | Fuente: {fuente}\n'
			#Datos
			new_data = Keywords(
				keyword_id = keyword_id,
				keyword_name = keyword_name,
				keyword_metrica_name = keyword_metrica_name,
				keyword_metrica_value = keyword_metrica_value,
				keyword_indicador_name = keyword_indicador_name,
				keyword_indicador_value = keyword_indicador_value,
				keyword_fuente = keyword_fuente,
				keyword_estado = keyword_estado,
				proyecto_id = keyword_pid
			)
			db.session.add(new_data)
			db.session.commit()
			#return redirect('/brandkit/links')
			return "success"
#===Listado Ajax===
@ptendencias_bp.route('view-table', methods=['GET', 'POST'])
@validar_sesion
def tendencias_listarTableAjax(brand_id,proyecto_id):
	pid = proyecto_id
	try:
		if request.method in ['GET', 'POST']:
			fuentes = request.values.getlist('fuentes[]')
			#print(f"Fuentes recibidas: {fuentes}")
			query = Keywords.query.filter(
				Keywords.keyword_estado == 1
			)
			if fuentes:
				query = query.filter(Keywords.keyword_fuente.in_(fuentes))
			query = query.order_by(Keywords.keyword_id)
			sql_generado = str(query.statement.compile())
			#print(f"SQL generado: {sql_generado}")
			lista = query.all()
			if lista:
				return render_template('sections/proyectos/tendencias/vista-table.html', lista=lista,pid=pid)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Listado Ajax Cards===
@ptendencias_bp.route('view-cards-old', methods=['GET', 'POST'])
@validar_sesion
def tendencias_listarCardsAjax(brand_id,proyecto_id):
	try:
		if request.method in ['GET', 'POST']:
			buscar = request.values.get('buscar')
			fuentes = request.values.getlist('fuentes[]')
			if not fuentes:
				fuentes = request.values.getlist('fuentes')
			listas = {}
			# Itera sobre CADA fuente seleccionada
			for fuente_seleccionada in fuentes:
				if fuente_seleccionada == "Semrush":
					listas.setdefault("semrush", {}) 
					listas["semrush"]["tipo"] = "Semrush"
					listas["semrush"]["lista"] = listarSemrush()
				elif fuente_seleccionada == "Google Search":
					listas.setdefault("google-search", {})
					listas["google-search"]["tipo"] = "Google Search"
					listas["google-search"]["lista"] = listarSearcConsole()
				elif fuente_seleccionada == "Google Trends":
					listas["google-trends"] = {"tipo": "Google Trends", "lista": []}
			if listas:
				return render_template('sections/proyectos/tendencias/vista-cards.html', listas=listas,convierteBase64=convierteBase64)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500

#===Listado Ajax Cards===
@ptendencias_bp.route('view-cards', methods=['GET', 'POST'])
@validar_sesion
def tendencias_listarCardsAjaxTest(brand_id, proyecto_id):
	url_api = "https://api-seo-consolidado-1079186964678.us-central1.run.app/list-keywords"
	
	# Parámetros según la documentación
	payload = {}
	if request.method == 'POST':
		keyword = request.form.get('keyword')

		fuentes_enviadas = request.values.getlist('fuentes[]')
		if not fuentes_enviadas:
			fuentes_enviadas = request.values.getlist('fuentes')
		dict_fuente_api = {f: "on" for f in fuentes_enviadas}
		print("Objeto dict_fuente_api enviado:", dict_fuente_api)

		fecini = request.form.get('fecini') or "2025-12-13"
		fecfin = request.form.get('fecfin') or "2025-12-18"

		
		if keyword: payload['keyword'] = keyword
		if fecini: payload['fecini'] = fecini
		if fecfin: payload['fecfin'] = fecfin
		if dict_fuente_api: payload["fuente"] = dict_fuente_api

		payload['fecini'] = "2025-12-13"
		payload['fecfin'] = "2025-12-18"

	data_estructurada = []

	try:
		# Petición POST a la API
		response = requests.post(url_api, json=payload, timeout=10)
		
		if response.status_code == 200:
			api_data = response.json()
			lista_original = api_data.get('data', []) #

			# 1. Agrupar por Keyword y Fuente
			# Usamos un diccionario temporal para organizar la jerarquía
			temp_dict = {}

			for item in lista_original:
				# Creamos una llave única combinando keyword y fuente
				key = (item.get('keyword'), item.get('fuente'))
				
				# Convertimos metrica_value a número (float o int)
				try:
					# Reemplazamos posibles caracteres no numéricos si fuera necesario
					valor_limpio = item.get('metrica_value', '0')
					valor_numerico = int(valor_limpio) if valor_limpio else 0
					valor_limpio02 = item.get('metrica2_value', '0')
					valor_numerico02 = int(valor_limpio02) if valor_limpio02 else 0
					valor_limpio03 = item.get('metrica3_value', '0')
					valor_numerico03 = int(valor_limpio03) if valor_limpio03 else 0
				except ValueError:
					valor_numerico = 0
					valor_numerico02 = 0
					valor_numerico03 = 0

				if key not in temp_dict:
					temp_dict[key] = {
						'keyword': item.get('keyword'),
						'fuente': item.get('fuente'),
						'max_metrica_value': valor_numerico,
						'max_metrica_type': item.get('metrica_type'),
						'max_metrica2_value': valor_numerico02,
						'max_metrica2_type': item.get('metrica2_type'),
						'max_metrica3_value': valor_numerico03,
						'max_metrica3_type': item.get('metrica3_type'),
						'dias': [] # Aquí enterán los objetos {date, otros campos}
					}
				else:
					if valor_numerico > temp_dict[key]['max_metrica_value']:
						temp_dict[key]['max_metrica_value'] = valor_numerico
						temp_dict[key]['max_metrica_type'] = item.get('metrica_type')
				# Insertamos el objeto de datos del día en el subarray 'dias'
				temp_dict[key]['dias'].append({
					'date': item.get('date'),
					'metrica_value': valor_numerico,
					'metrica_type': item.get('metrica_type'),
					'brand_type': item.get('brand_type'),
					'metrica2_type': item.get('metrica2_type'),
					'metrica2_value': valor_numerico02,
					'metrica3_type': item.get('metrica3_type'),
					'metrica3_value': valor_numerico03
				})

			# 2. Convertir el diccionario a una lista limpia
			data_estructurada = list(temp_dict.values())

			# 3. Ordenar: Primero por Keyword alfabéticamente y luego cada subarray por fecha
			#data_estructurada.sort(key=lambda x: x['keyword'])
			data_estructurada.sort(key=lambda x: (x['fuente'], x['max_metrica_value']))
			for grupo in data_estructurada:
				grupo['dias'].sort(key=lambda d: d['date']) # Orden ascendente de fecha
				grupo['valores_linea'] = lista_grafico(grupo['dias'], "metrica_value", fecini, fecfin)
				grupo['valores_linea2'] = lista_grafico(grupo['dias'], "metrica2_value", fecini, fecfin)
				grupo['valores_linea3'] = lista_grafico(grupo['dias'], "metrica3_value", fecini, fecfin)

	except requests.exceptions.RequestException as e:
		print(f"Error de conexión: {e}")
	return render_template(
		'sections/proyectos/tendencias/vista-table.html',
		listado=data_estructurada,fecini=fecini,fecfin=fecfin
	)

#Semrush
def listarSemrush():
	query = f"SELECT * FROM `{bq_table_seo_semrush}`"
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		data = [dict(row.items()) for row in results]
		return data
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#Search Console
def listarSearcConsole():
	query = f"""SELECT query, SUM(impressions) AS total_impressions,
			SUM(clicks) AS total_clicks,
			CAST(AVG(CAST(sum_position AS BIGNUMERIC)) AS INT64) AS avg_position_int 
			FROM `{bq_table_seo_search}`
			WHERE
			-- Excluir keywords de marca y sus variantes/errores
				query NOT LIKE '%cl_ro%'
				AND query NOT LIKE '%calro%'
				AND query NOT LIKE '%claer%'
				AND query NOT LIKE '%clra%'
				AND query NOT LIKE '%mi claro%'
				AND query NOT LIKE '%app claro%'
				AND query NOT LIKE '%claro peru%'
				AND query NOT LIKE '%claro movil%'
				AND query NOT LIKE '%claro hogar%'
				AND query NOT LIKE '%claro empresas%'
				AND query NOT LIKE '%internet claro%'
				AND query NOT LIKE '%telefonia claro%'
				AND query NOT LIKE '%movil claro%'
				AND query NOT LIKE '%fibra optica claro%'
				AND query NOT LIKE '%celular claro%'
				AND query NOT LIKE '%datos claro%'
				AND query NOT LIKE '%plan claro%'
				AND query NOT LIKE '%portabilidad claro%'
				AND query NOT LIKE '%recarga claro%'
				AND query NOT LIKE '%chip claro%'
				AND query NOT LIKE '%tv claro%'
				AND query NOT LIKE '%cable claro%'
				AND query NOT LIKE '%pospago%'
				AND query NOT LIKE '%planes%'
				AND query NOT LIKE '%claeo%'
				AND data_date >= current_date() -30
			GROUP BY
				query
			HAVING
				CAST(AVG(CAST(sum_position AS BIGNUMERIC)) AS INT64) <= 10 and   CAST(AVG(CAST(sum_position AS BIGNUMERIC)) AS INT64) >= 10
			ORDER BY
				total_impressions DESC,
				avg_position_int ASC
			LIMIT 20
			"""
	try:
		query_job = bq_client.query(query)
		results = query_job.result()
		data = [dict(row.items()) for row in results]
		return data
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===============
#===Table Add===
#===============
@ptendencias_bp.route('agregar', methods=['GET', 'POST'])
def addKeyword(brand_id,proyecto_id):
	keyword_buscado = request.values.get('keyword')
	try:
		# Normalizar el keyword buscado
		keyword_normalizado = keyword_buscado.strip().lower() if keyword_buscado else ""
		encontrado = None
		# --- BÚSQUEDA EN SEMRUSH ---
		lista_semrush = listarSemrush()
		# Normalizar y buscar en Semrush
		for item in lista_semrush:
			# Mapeo a formato común para comparación y uso:
			# 'Keyword' -> 'keyword', 'Posicion' -> 'posicion', 'Search_Volume' -> 'metrica'
			nombre_item = item.get('Keyword', '').strip().lower()
			
			if nombre_item == keyword_normalizado:
				encontrado = {
					'keyword': item.get('Keyword', ''),
					'posicion': item.get('Posicion', 'N/A'), 
					'metrica': item.get('Search_Volume', 'N/A'),
					'fuente': 'Semrush'
				}
				break # Detener la búsqueda en Semrush si se encuentra
				
		# --- BÚSQUEDA EN GOOGLE SEARCH CONSOLE (Solo si no se encontró en Semrush) ---
		if not encontrado:
			lista_search_console = listarSearcConsole()
			
			# Normalizar y buscar en Search Console
			for item in lista_search_console:
				# Mapeo a formato común para comparación y uso:
				# 'query' -> 'keyword', 'avg_position_int' -> 'posicion', 'total_impressions' -> 'metrica'
				nombre_item = item.get('query', '').strip().lower()
				
				if nombre_item == keyword_normalizado:
					encontrado = {
						'keyword': item.get('query', ''),
						'posicion': item.get('avg_position_int', 'N/A'), 
						'metrica': item.get('total_impressions', 'N/A'),
						'fuente': 'Google Search'
					}
					break # Detener la búsqueda en Search Console
		
		# --- GENERACIÓN DE LA RESPUESTA ---
		if encontrado:
			# Usamos el diccionario 'encontrado' que ya está normalizado
			keyword = encontrado.get('keyword', 'N/A')
			posicion = encontrado.get('posicion', 'N/A')
			metrica = encontrado.get('metrica', 'N/A')
			fuente = encontrado.get('fuente', '')
			
			# Creamos el HTML con los datos encontrados
			html = f'\tKeyword: {keyword} | Posición: {posicion} | Métrica: {metrica} | Fuente: {fuente}\n'
			return html
		else:
			# Devolver un mensaje si la palabra clave no se encuentra
			return f"Keyword '{keyword_buscado}' no encontrado en ninguna de las fuentes.", 404
			
	except Exception as e:
		print(f"Ocurrió un error inesperado al procesar las listas: {e}")
		return "Error interno del servidor al buscar el keyword.", 500
#============
#===Select===
#============
@ptendencias_bp.route('select-fuente', methods=['GET', 'POST'])
def selectKeyword(brand_id,proyecto_id):
	fuente = request.values.get('fuente')
	contenido_list = []
	clave_keyword = None  # Variable para almacenar la clave correcta ('Keyword' o 'query')
	try:
		fuente_normalizada = fuente.lower() if fuente else "" 
		if fuente_normalizada == "semrush":
			contenido_list = listarSemrush()
			clave_keyword = 'Keyword' 
		elif fuente_normalizada == "search-console":
			contenido_list = listarSearcConsole()
			clave_keyword = 'query'
		html_output = '<select id="cbo_keyword" name="cbo_keyword">\n'
		html_output += '\t<option value="">Selecciona una palabra</option>\n'

		if clave_keyword:
			for item in contenido_list:
				nombre = item.get(clave_keyword, "") 
				if nombre:
					html_output += f'\t<option value="{nombre}">{nombre}</option>\n'
		html_output += '</select>'
		return html_output
		
	except Exception as e:
		print(f"Ocurrió un error inesperado al cargar el JSON o al obtener la lista: {e}")
		# Se recomienda un mensaje de error menos técnico para el usuario final
		return "Error interno del servidor. Por favor, revisa los logs.", 500
#===============
#===Funciones===
#===============
def convierteBase64(text: str) -> str:
	return base64.urlsafe_b64encode(text.encode('utf-8')).decode('ascii')

def lista_grafico(dias_array, metrica_name, fecini_str, fecfin_str):
	"""
	Transforma datos parciales en una serie completa para el gráfico.
	metrica_name: puede ser 'metrica_value', 'metrica2_value', etc.
	"""
	try:
		fecini = datetime.strptime(fecini_str, '%Y-%m-%d')
		fecfin = datetime.strptime(fecfin_str, '%Y-%m-%d')
	except Exception as e:
		print(f"Error en formato de fechas: {e}")
		return []

	dias_semana = {
		'Monday': 'Lun', 'Tuesday': 'Mar', 'Wednesday': 'Mié',
		'Thursday': 'Jue', 'Friday': 'Vie', 'Saturday': 'Sáb', 'Sunday': 'Dom'
	}

	# 1. Crear el mapeo dinámico usando la métrica especificada
	mapeo_datos = {}
	for d in dias_array:
		try:
			# Usamos metrica_name en lugar de la llave fija
			valor_numerico = int(float(d.get(metrica_name, 0)))
			mapeo_datos[d['date']] = valor_numerico
		except (ValueError, TypeError):
			continue

	# 2. Generar la lista completa día por día
	datos_grafico = []
	fecha_actual = fecini

	while fecha_actual <= fecfin:
		str_fecha = fecha_actual.strftime('%Y-%m-%d')
		nombre_dia_en = fecha_actual.strftime('%A')
		nombre_dia_es = dias_semana.get(nombre_dia_en, nombre_dia_en)
		
		valor = mapeo_datos.get(str_fecha, 0)
		datos_grafico.append([nombre_dia_es, valor])
		
		fecha_actual += timedelta(days=1)

	return datos_grafico
