from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from functools import wraps
from datetime import datetime
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
import datetime
import pandas as pd
import traceback # Asume que pandas está importado
import uuid
#llamar a config
from routes.models import db, Assets, Configuracion, Proyectos, Keywords
from routes.config.geniaconfig import bq_client, bq_table_seo_semrush, bq_table_seo_search, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

pkeywords_bp = Blueprint('pkeywords_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/keywords/')
#===View===
@pkeywords_bp.route('/test')
@validar_sesion
def keywords_main(brand_id,proyecto_id):
	return render_template('sections/proyectos/keywords/main.html')
#===Create===
@pkeywords_bp.route('/', methods=['GET'])
@validar_sesion
def keywords_keywords(brand_id,proyecto_id):
	if request.method == 'GET':
		return render_template('sections/proyectos/keywords/dashboard.html', proyecto_id=proyecto_id)
#===Save===
@pkeywords_bp.route('addkeyword', methods=['POST'])
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
			keyword_metrica_name = encontrado.get('keyword_metrica_name', ''),
			keyword_metrica_value = encontrado.get('keyword_metrica_value', ''),
			keyword_indicador_name = encontrado.get('keyword_indicador_name', ''),
			keyword_indicador_value = encontrado.get('keyword_indicador_value', ''), 
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
@pkeywords_bp.route('view-table', methods=['GET', 'POST'])
@validar_sesion
def keywords_listarTableAjax(brand_id,proyecto_id):
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
				return render_template('sections/proyectos/keywords/vista-table.html', lista=lista,pid=pid)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
#===Listado Ajax Cards===
@pkeywords_bp.route('view-cards', methods=['GET', 'POST'])
@validar_sesion
def keywords_listarCardsAjax():
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
				return render_template('sections/proyectos/keywords/vista-cards.html', listas=listas,convierteBase64=convierteBase64)
			else:
				return 'No se encontraron campañas con los criterios especificados.'
		return 'Error en el método de solicitud'
	except Exception as e:
		return jsonify({"error": str(e)}), 500
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
@pkeywords_bp.route('agregar', methods=['GET', 'POST'])
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
@pkeywords_bp.route('select-fuente', methods=['GET', 'POST'])
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