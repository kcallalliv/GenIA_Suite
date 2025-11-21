# routes/alerts.py
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
from routes.models import db, Assets, Configuracion, Exclusiones, Sitemap
from routes.config.geniaconfig import bq_client, bq_table_config, bq_table_assets, bucket_name, storage_client, validar_sesion, fechaActual

bkwebscan_bp = Blueprint('bkwebscan_bp', __name__, url_prefix='/brand')

#===Paginas===
@bkwebscan_bp.route('/<string:brand_id>/webscan/')
@validar_sesion
def bkwebscan_main(brand_id):
	return render_template('sections/brandkit/webscan/main.html')

#===Pagina Excluidos===
@bkwebscan_bp.route('/<string:brand_id>/webscan/excluidos')
@validar_sesion
def bkwebscan_main_excluidos(brand_id):
	return render_template('sections/brandkit/webscan/main-excluidos.html')

#===Realizar scraping===
@bkwebscan_bp.route('/<string:brand_id>/webscan/scraping')
@validar_sesion
def scrapListUrls(brand_id):
	if request.method == 'GET':
		url = request.values.get('site')
		#url = "https://www.claro.com.pe/proteccion-datos/"
		site_name = clean_url_path(url)
		result = scrapeUrls(url)
		date_str = datetime.datetime.now(tz=tz_pe).strftime("%Y-%m-%d")
		file_name = f"sitemap/{site_name}-{date_str}.json"
		save_json = save_to_gcs(result,file_name);
		return jsonify({
			"json": result
		})

#===Listar Excluidos===
@bkwebscan_bp.route('/<string:brand_id>/webscan/list-excluidos')
@validar_sesion
def listarExcluidos(brand_id):
	try:
		query = Exclusiones.query.filter_by(exsite_estado='1')
		lista = query.all()
		#return lista
		return render_template('sections/brandkit/webscan/list-excluidos.html',lista= lista,verEstado=verEstado )
	except Exception as e:
		return jsonify({"error": str(e)}), 500

#===Listar url a scrapear===
@bkwebscan_bp.route('/<string:brand_id>/webscan/list-scraping')
@validar_sesion
def listarUrlsScraping(brand_id):
	try:
		fecha_actual = Sitemap.query.order_by(desc(Sitemap.site_fecha)).first().site_fecha
		query = Sitemap.query.filter(and_(Sitemap.site_fecha == fecha_actual))
		#query = Sitemap.query.filter_by(site_estado='1')
		lista = query.all()
		#return lista
		return render_template('sections/brandkit/webscan/list-scraping.html',lista= lista,verEstado=verEstado )
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@bkwebscan_bp.route('/<string:brand_id>/webscan/list-raw')
@validar_sesion
def listarUrlsRaw(brand_id):
	try:
		fecha_actual = Sitemap.query.order_by(desc(Sitemap.site_fecha)).first().site_fecha
		query = Sitemap.query.filter(Sitemap.site_fecha == fecha_actual,Sitemap.site_estado == 1)
		#query = Sitemap.query.filter(and_(Sitemap.site_fecha == fecha_actual))
		#query = Sitemap.query.filter_by(site_estado='1')
		lista = query.all()
		#return lista
		return render_template('sections/brandkit/webscan/list-raw.html',lista= lista,verEstado=verEstado )
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@bkwebscan_bp.route('/<string:brand_id>/webscan/remover-excluidos', methods=["GET", "POST"])
@validar_sesion
def removerExcluidosUrls(brand_id):
	try:
		if not request.is_json:
			return jsonify({"error": "La solicitud debe ser JSON"}), 400
		data = request.get_json()
		data_incluidos = data.get('incluidos')
		if not data_incluidos or not isinstance(data_incluidos, list):
			return jsonify({"error": "Falta la lista de datos 'incluidos'"}), 400
		# Recolecta las URLs y los IDs en una sola pasada
		urls_a_eliminar = [item.get('url') for item in data_incluidos]
		ids_a_actualizar = [item.get('id') for item in data_incluidos]
		# 1. Eliminación en lote
		Exclusiones.query.filter(Exclusiones.exsite_url.in_(urls_a_eliminar)).delete(synchronize_session='fetch')
		# 2. Actualización en lote
		fecha_actual = Sitemap.query.order_by(desc(Sitemap.site_fecha)).first().site_fecha
		Sitemap.query.filter(Sitemap.site_url.in_(urls_a_eliminar),Sitemap.site_fecha == fecha_actual).update(
			{"site_estado": 1},synchronize_session='fetch'
		)
		# 3. Confirma todos los cambios de una vez
		db.session.commit()
		return jsonify({
			"status": "success",
			"message": f"Se incluyeron y actualizaron {len(data_incluidos)} registros."
		}), 200
	except Exception as e:
		db.session.rollback() # Deshace cualquier cambio si ocurre un error
		return jsonify({"error": str(e)}), 500

@bkwebscan_bp.route('/<string:brand_id>/webscan/excluir', methods=["GET", "POST"])
@validar_sesion
def excluirUrls(brand_id):
	try:
		if not request.is_json:
			return jsonify({"error": "La solicitud debe ser JSON"}), 400
		data = request.get_json()
		data_excluidos = data.get('excluidos')
		if not data_excluidos or not isinstance(data_excluidos, list):
			return jsonify({"error": "Falta la lista de datos 'excluidos'"}), 400
		# Recopilar datos en una sola pasada
		registros_insertados = []
		ids_actualizados = []
		for item in data_excluidos:
			url = item.get('url')
			registro_id = item.get('id')
			# Crear el objeto Exclusiones y agregarlo a la lista de inserción
			new_data = Exclusiones(
				exsite_url = url,
				exsite_fecha = fechaActual(),
				exsite_estado = 1
			)
			registros_insertados.append(new_data)
			# Agregar el ID a la lista de actualización
			ids_actualizados.append(registro_id)
		# 1. Inserción en lote (todos a la vez)
		db.session.add_all(registros_insertados)
		# 2. Actualización en lote (todos a la vez)
		Sitemap.query.filter(Sitemap.site_id.in_(ids_actualizados)).update(
			{"site_estado": 0},
			synchronize_session='fetch'
		)
		# 3. Confirmar todos los cambios
		db.session.commit()
		return jsonify({
			"status": "success",
			"message": f"Se excluyeron y actualizaron {len(data_excluidos)} registros."
		}), 200
	except Exception as e:
		db.session.rollback()  # Deshacer cambios en caso de error
		return jsonify({"error": str(e)}), 500

@bkwebscan_bp.route('/<string:brand_id>/webscan/incluir', methods=["GET", "POST"])
@validar_sesion
def incluirUrls(brand_id):
	try:
		if not request.is_json:
			return jsonify({"error": "La solicitud debe ser JSON"}), 400
		data = request.get_json()
		data_incluidos = data.get('incluidos')
		if not data_incluidos or not isinstance(data_incluidos, list):
			return jsonify({"error": "Falta la lista de datos 'incluidos'"}), 400
		# Recolecta las URLs y los IDs en una sola pasada
		urls_a_eliminar = [item.get('url') for item in data_incluidos]
		ids_a_actualizar = [item.get('id') for item in data_incluidos]
		# 1. Eliminación en lote
		Exclusiones.query.filter(Exclusiones.exsite_url.in_(urls_a_eliminar)).delete(synchronize_session='fetch')
		# 2. Actualización en lote
		fecha_actual = Sitemap.query.order_by(desc(Sitemap.site_fecha)).first().site_fecha
		Sitemap.query.filter(Sitemap.site_id.in_(ids_a_actualizar),Sitemap.site_fecha == fecha_actual).update(
			{"site_estado": 1},synchronize_session='fetch'
		)
		# 3. Confirma todos los cambios de una vez
		db.session.commit()
		return jsonify({
			"status": "success",
			"message": f"Se incluyeron y actualizaron {len(data_incluidos)} registros."
		}), 200
	except Exception as e:
		db.session.rollback() # Deshace cualquier cambio si ocurre un error
		return jsonify({"error": str(e)}), 500

@bkwebscan_bp.route('/<string:brand_id>/webscan/raw', methods=["GET", "POST"])
@validar_sesion
def readListUrls(brand_id):
	if request.method == 'GET':
		sitemap_url = request.values.get('site')
		#sitemap_url = "https://www.claro.com.pe/sitemap.xml"
		#remover registros previos
		#Sitemap.query.filter(Sitemap.client_id == client_id).delete()
		Sitemap.query.delete()
		#fecha
		my_fecha_actual =  fechaActual()
		extracted_urls = extractUrls(sitemap_url)
		# 1. Obtener URLs de exclusión de la base de datos de manera eficiente
		# Usamos una comprensión de lista para obtener solo las URLs, no los objetos completos.
		urls_excluidas_db = [item.exsite_url for item in Exclusiones.query.filter_by(exsite_estado=1).all()]
		filtered_urls = []
		for url in extracted_urls:
			is_excluded = False
			# 2. Verificar si la URL extraída está en la lista de exclusión de la base de datos
			# Esto es más rápido que el bucle anidado que tenías.
			if url in urls_excluidas_db:
				is_excluded = True
			else:
				# El resto de tu lógica para exclusiones, si es necesaria
				for exclusion_pattern in exclusiones:
					if exclusion_pattern in url.lower():
						is_excluded = True
						break
			# Si la URL no está excluida, la añadimos a la lista filtrada
			if not is_excluded:
				filtered_urls.append(url)
		# 3. Inserción de los registros de forma masiva (mejora de rendimiento)
		registros_a_insertar = []
		for url in filtered_urls:
			new_data = Sitemap(
				site_name = "",
				site_url = url,
				site_fecha = my_fecha_actual,
				site_estado = 1
			)
			registros_a_insertar.append(new_data)
		db.session.add_all(registros_a_insertar)
		db.session.commit()
		return jsonify({
			"urls": filtered_urls,
			"total_urls": len(filtered_urls),
			"tiempo2": my_fecha_actual,
		})
		
#Extraer urls sitemap
def extractUrls(sitemap_url, visited=None, max_depth=3):
	if visited is None:
		visited = set()
	urls = []
	def _walk(url, depth):
		if url in visited or depth > max_depth:
			return
		visited.add(url)
		print(f"Buscando sitemap en: {url}")
		try:
			response = requests.get(url, timeout=10)
			response.raise_for_status()
			xml_text = response.text
		except requests.exceptions.RequestException as e:
			print(f"[WARN] No pude leer {url}: {e}")
			return
		soup = BeautifulSoup(xml_text, "xml")
		# Es un sitemap_index? -> Recorrer sitemaps hijos
		sitemap_index = soup.find("sitemapindex")
		if sitemap_index:
			for sm in sitemap_index.find_all("sitemap"):
				loc = sm.find("loc")
				if loc:
					_walk(loc.get_text(strip=True), depth + 1)
			return
		# Es un urlset? -> Colectar URLs
		urlset = soup.find("urlset")
		if urlset:
			for u in urlset.find_all("url"):
				loc = u.find("loc")
				if loc:
					urls.append(loc.get_text(strip=True))
	_walk(sitemap_url, depth=0)
	return urls
# ========= Exclusiones =========
exclusiones = set([
	'hablando-claro','test','demo','institucional','bk','bkp','postpago-a','postpago-b','/vb/','oferta-secreta-portabilidad','_1/','v3','provincia2/','v1',
	"https://www.claro.com.pe/cobertura_geojson/",
	"https://www.claro.com.pe/conoce-tu-recibo/debito-automatico_1/",
	"https://www.claro.com.pe/demo-componentes/",
	"https://www.claro.com.pe/demo-componentes/banners_magazine/",
	"https://www.claro.com.pe/demo-componentes/cards/",
	"https://www.claro.com.pe/demo-componentes/componentes-adicionales/",
	"https://www.claro.com.pe/demo-componentes/componentes-nuevos/",
	"https://www.claro.com.pe/demo-componentes/entry-points/",
	"https://www.claro.com.pe/demo-componentes/highlights-beneficios/",
	"https://www.claro.com.pe/demo-componentes/informacion-adicional/",
	"https://www.claro.com.pe/demo-componentes/navigation/",
	"https://www.claro.com.pe/departamentos_test/",
	"https://www.claro.com.pe/empresas/avisos-dia-1/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/anti-ddos/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/sase/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/seguridad-administrada/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/seguridad-administrada-virtual/",
	"https://www.claro.com.pe/empresas/soluciones/ciberseguridad_1/seguridad-sse/",
	"https://www.claro.com.pe/error/",
	"https://www.claro.com.pe/gracias-crm/",
	"https://www.claro.com.pe/gracias-sorteo/",
	"https://www.claro.com.pe/hablando-claro/error404/",
	"https://www.claro.com.pe/institucional/centro-de-prensa/test-noticia/",
	"https://www.claro.com.pe/institucional/sustentabilidad/reciclaje-de-residuos-2/",
	"https://www.claro.com.pe/negocios/beneficios/fijos/oferta-internet-empresas-v2/",
	"https://www.claro.com.pe/negocios/beneficios/movil/oferta-olo-v2/",
	"https://www.claro.com.pe/negocios/fijos/internet/internet-fijo-inalambrico2/",
	"https://www.claro.com.pe/negocios/fijos/oferta-internet-empresas-v2/",
	"https://www.claro.com.pe/negocios/kit-tienda-virtual-p-v2/",
	"https://www.claro.com.pe/negocios/kit-tienda-virtual-v2/",
	"https://www.claro.com.pe/negocios/movil/oferta-olo-v2/",
	"https://www.claro.com.pe/negocios/soluciones/teletrabajo-negocios-v2/",
	"https://www.claro.com.pe/personas/beneficios/claro-club/canje-claro-puntos-bk/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/canje-clarovideo/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/canje-clarovideo_1/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/claro-club-premium/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/concursos/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/latam/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/latam_1/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/latam_2/",
	"https://www.claro.com.pe/personas/beneficios/claro-club_bkp/sorteo-vales-consumo/",
	"https://www.claro.com.pe/personas/beneficios/equipo-vale-plata-v2/",
	"https://www.claro.com.pe/personas/beneficios/full-claro-bkp/",
	"https://www.claro.com.pe/personas/beneficios/movil/norton-security_1/",
	"https://www.claro.com.pe/personas/beneficios/movil/sorteo-fiestas-patrias_1/",
	"https://www.claro.com.pe/personas/estamos-juntos/fraccionamiento-v2/",
	"https://www.claro.com.pe/personas/hogar/alianzas_bk/",
	"https://www.claro.com.pe/personas/hogar/guia-usuario-test/",
	"https://www.claro.com.pe/personas/hogar/internet-fibra-optica_bk/",
	"https://www.claro.com.pe/personas/hogar/oferta-fiija-2/",
	"https://www.claro.com.pe/personas/hogar/olo_1/",
	"https://www.claro.com.pe/personas/movil/alerta_v2/",
	"https://www.claro.com.pe/personas/movil/prepago/bono-provincia2/",
	"https://www.claro.com.pe/personas/movil/prepago/control-automatico-v3/",
	"https://www.claro.com.pe/personas/movil/prepago/paquetes_1/",
	"https://www.claro.com.pe/personas/movil/prepago/plan-prepagado_1/",
	"https://www.claro.com.pe/personas/movil/promociones/canje-smart_backup/",
	"https://www.claro.com.pe/personas/sorteo_gracias_test/",
	"https://www.claro.com.pe/personas/sorteo_test/",
	"https://www.claro.com.pe/personas/sorteo_test_v1/",
	"https://www.claro.com.pe/personas/sorteosv1/",
	"https://www.claro.com.pe/pruebashtml-havas-victor/",
	"https://www.claro.com.pe/qr/",
	"https://www.claro.com.pe/sitemap/",
	"https://www.claro.com.pe/test-componentes/",
	"https://www.claro.com.pe/test-componentes-cms/",
	"https://www.claro.com.pe/testpage/",
	"oferta-secreta",
	"https://www.claro.com.pe/constancia-del-registro-de-la-solicitud-de-envio-de-publicidad/",
	"https://www.claro.com.pe/igualdad/",
	"https://www.claro.com.pe/buscador/",
	"https://www.claro.com.pe/igbio/",
	"https://www.claro.com.pe/pruebacrm/",
	"https://www.claro.com.pe/claroshop/",
	"https://www.claro.com.pe/claroshop/login/",
	"https://www.claro.com.pe/claroshop/registro/",
	"https://www.claro.com.pe/claroshop/perfil/",
	"https://www.claro.com.pe/claroshop/perfil/mis-compras/",
	"https://www.claro.com.pe/claroshop/perfil/datos-personales/",
	"https://www.claro.com.pe/claroshop/perfil/cambio-contrasena/",
	"https://www.claro.com.pe/claroshop/catalogo/",
	"https://www.claro.com.pe/claroshop/catalogo/celulares/",
	"https://www.claro.com.pe/claroshop/catalogo/celulares/detalle/",
	"https://www.claro.com.pe/claroshop/catalogo/ropa/",
	"https://www.claro.com.pe/claroshop/catalogo/ropa/detalle/",
	"https://www.claro.com.pe/claroshop/catalogo/accesorios/",
	"https://www.claro.com.pe/claroshop/catalogo/accesorios/detalle/",
	"https://www.claro.com.pe/me-queda-claro/bases-concurso/",
	"https://www.claro.com.pe/me-queda-claro/privado/",
	"https://www.claro.com.pe/me-queda-claro/post/",
	"https://www.claro.com.pe/me-queda-claro/perfil/",
	"https://www.claro.com.pe/me-queda-claro/mis-cursos/",
	"https://www.claro.com.pe/personas2/",
	"https://www.claro.com.pe/personas2/movil/",
	"https://www.claro.com.pe/personas2/movil/postpago/",
])
#===Funciones===
def scrapeUrls(url: str):
	try:
		# Define el User-Agent para la solicitud
		headers = {"User-Agent": "Mozilla/5.0 (compatible; GeniaScraper/1.0)"}
		
		# Realiza la solicitud HTTP
		resp = requests.get(url, timeout=20, headers=headers)
		resp.raise_for_status()
		
		# Parsea el HTML
		soup = BeautifulSoup(resp.text, 'html.parser')

		# Elimina elementos no relevantes para el contenido
		for tag in soup(['header', 'footer', 'nav', 'aside', 'script', 'style']):
			tag.decompose()

		# Extrae el título de la página
		title = soup.title.string.strip() if soup.title and soup.title.string else ""

		# Extrae los subtítulos (h1, h2, h3)
		main = soup.find('article') or soup.find('main') or soup.body
		subtitles = [tag.get_text(strip=True) for tag in (main.find_all(['h1', 'h2', 'h3']) if main else [])]

		# Extrae los párrafos (p)
		paragraphs = [p.get_text(strip=True) for p in (main.find_all('p') if main else [])]

		# Extrae las FAQs (basado en schema.org)
		faqs = []
		faq_section = soup.find('section', {"itemtype": "https://schema.org/FAQPage"})
		if faq_section:
			questions = faq_section.find_all('div', itemtype="https://schema.org/Question")
			for q in questions:
				qname = q.find(itemprop="name")
				question_text = qname.get_text(strip=True) if qname else ""
				answer_div = q.find(itemprop="acceptedAnswer")
				answer_text = ""
				if answer_div:
					a_text = answer_div.find(itemprop="text")
					answer_text = a_text.get_text(strip=True) if a_text else ""
				if question_text and answer_text:
					faqs.append({"question": question_text, "answer": answer_text})
		
		# Retorna el resultado en un diccionario
		return {
			"id": str(uuid.uuid4()),
			"url": url,
			"title": title,
			"subtitles": subtitles,
			"paragraphs": paragraphs,
			"faqs": faqs
		}
	
	except requests.RequestException as e:
		print(f"Error de solicitud para {url}: {e}")
		return None
	except Exception as e:
		print(f"Error inesperado al procesar {url}: {e}")
		return None
	return jsonify({"status": "error", "message": "Método no permitido. Use POST."}), 405
def gsfile_upload(file, uploader):
	try:
		if not file:
			return {"status": "error", "message": "No se proporcionó un archivo."}

		ext = file.filename.rsplit('.', 1)[-1] if '.' in file.filename else ''
		fecha = datetime.datetime.utcnow().strftime('%Y%m%d')
		name_archivo = f"{fecha}_{uploader}_{uuid.uuid4().hex}"
		name_fileext = f"{name_archivo}.{ext}"
		nombre_archivo = f"sitemap/{name_fileext}"
		# Subir a Cloud Storage
		bucket = storage_client.bucket(bucket_name)
		blob = bucket.blob(nombre_archivo)
		blob.upload_from_file(file)
		#datos
		asset_name = file.filename
		asset_value = name_archivo
		asset_src = name_fileext
		asset_type = "sitemap"
		asset_ext = ext
		asset_fecha = fechaActual()
		asset_estado = 1
		#save
		new_data = Assets(
			asset_name = asset_name,
			asset_src = asset_src,
			asset_value = asset_value,
			asset_type = asset_type,
			asset_ext = asset_ext,
			asset_fecha = asset_fecha,
			asset_estado = asset_estado
		)
		db.session.add(new_data)
		db.session.commit()
		return {"status": "success", "message": f"Archivo {nombre_archivo} subido correctamente"}
	except Exception as e:
		return {"status": "error", "message": f"Error al subir el archivo: {e}"}
def save_to_gcs(data: dict, file_path: str):
	try:
		# Inicializa el cliente de GCS
		client = storage.Client()
		# Obtiene una referencia al bucket
		bucket = storage_client.bucket(bucket_name)
		# Obtiene una referencia al archivo (blob)
		blob = bucket.blob(file_path)
		# Convierte el diccionario a una cadena JSON con formato
		json_string = json.dumps(data, indent=4, ensure_ascii=False)
		# Sube la cadena JSON al archivo en GCS
		blob.upload_from_string(json_string, content_type='application/json')
		print(f"Archivo guardado en gs://{bucket_name}/{file_path}")
		return True
	except Exception as e:
		print(f"Error al guardar en GCS: {e}")
		return False
def clean_url_path(url: str) -> str:
	# Define la base del dominio a eliminar
	base_url = "https://www.claro.com.pe/"
	if url.endswith('/'):
		url = url[:-1]
	if url.startswith(base_url):
		cleaned_path = url.replace(base_url, "", 1)
		final_path = cleaned_path.replace("/", "_")
		return final_path
	return url
def verEstado(valor):
	if valor == 1:
		result = "active"
	elif valor == 0:
		result = "disabled"
	else:
		result = "desconocido"  # O el valor que prefieras para casos no manejados
	return result