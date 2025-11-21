# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from google.genai import types
from google.api_core.client_options import ClientOptions
from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
from functools import wraps
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy.orm import aliased
from sqlalchemy import desc, and_
from bs4 import BeautifulSoup
from io import BytesIO
import sys
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
import mimetypes
import pathlib
import datetime
import pandas as pd
import traceback 
import uuid
import base64
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from werkzeug.utils import secure_filename
from google.cloud import aiplatform
#llamar a config
from routes.models import db, Assets, Configuracion, Proyectos, Imagesia
from routes.config.geniaconfig import bq_client, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

ia_articulo_bp = Blueprint('ia_articulo_bp', __name__)

# Variables Globales (GCP Project y Location deben estar definidos globalmente o en init)
GCP_PROJECT = os.environ.get('GCP_PROJECT', 'prd-claro-mktg-data-storage')
GCP_LOCATION = os.environ.get('GCP_REGION', 'us-central1')
secret_key = os.environ.get('SESSION_KEY', 'creative_claro_super_secret_key_prod')
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBjLIPcIzCY6zuWJdiikno0sWHpilbwLw4") 
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "tu-bucket-de-claro-imagenes")

# Inicialización de Vertex AI (Necesario para ImageGenerationModel)
aiplatform.init(project=GCP_PROJECT, location=GCP_LOCATION) 

# Diccionario de Modelos Disponibles (AGREGADO IMAGEN 3.0)
AVAILABLE_MODELS = {
	"gemini-2.5-flash-lite-preview-09-2025": {"name": "G2.5 Lite Preview", "description": "Rentable, baja latencia. Ideal para drafts masivos.", "priority": 9, "type": "Gemini_API"},
	"gemini-2.5-flash-preview-09-2025": {"name": "G2.5 Flash Preview", "description": "Modelo estándar con buen razonamiento. Balance costo/calidad.", "priority": 7, "type": "Gemini_API"},
	"gemini-2.5-flash-image": {"name": "G2.5 Flash Image (Nano Banana)", "description": "Generación y edición multimodal de imágenes. Buen balance para generación de imágenes.", "priority": 5, "type": "Gemini_API"},
	"gemini-2.5-pro": {"name": "G2.5 Pro", "description": "Modelo de razonamiento más avanzado. Máxima calidad. Alto costo.", "priority": 1, "type": "Gemini_API"},
	"imagen-3.0-generate-002": {"name": "Imagen 3.0 Standard", "description": "Modelo de generación estándar previo. Compatible con Vertex AI.", "priority": 3, "type": "Imagen_VertexAI"},
	"imagen-4.0-ultra-generate-001": {"name": "Imagen 4.0 Ultra", "description": "Máxima calidad FOTORREALISTA. Ideal para activos finales Premium de alto impacto.", "priority": 1, "type": "Imagen_VertexAI"},
	"imagen-4.0-generate-001": {"name": "Imagen 4.0 Standard", "description": "Alta fidelidad a marca y Aspect Ratio. Balance entre calidad y costo. Recomendado para banners.", "priority": 2, "type": "Imagen_VertexAI"},
	"imagen-4.0-stylize-001": {"name": "Imagen 4.0 Stylize", "description": "Modelo de nicho. Énfasis en estilos artísticos y conceptuales. Útil para branding abstracto.", "priority": 4, "type": "Imagen_VertexAI"},
	"veo-3.0-generate-001": {"name": "VEO 3.0 Video Generation", "description": "Generación de clips de video a partir de texto. Proceso Asíncrono (LRO).", "priority": 5, "type": "Veo_VertexAI"},
}

platform_specs = {
	"ig_post": {"name": "Instagram Post (Vertical)", "width": 1080, "height": 1350, "ratio": "4:5"},
	"fb_square": {"name": "Facebook Post / Square", "width": 1200, "height": 1200, "ratio": "1:1"},
	"story": {"name": "Instagram/TikTok Story", "width": 1080, "height": 1920, "ratio": "9:16"},
	"web_banner": {"name": "Web Banner Publicitario", "width": 1920, "height": 600, "ratio": "3.2:1"},
	"blog_cover": {"name": "Imagen para Blog (Cover 4.5:1)", "width": 1800, "height": 400, "ratio": "4.5:1"},
	"article_cover": {"name": "Imagen para Artículo (Social Link Preview)", "width": 1200, "height": 628, "ratio": "1.91:1"},
	"yt_thumb": {"name": "YouTube Thumbnail (16:9)", "width": 1280, "height": 720, "ratio": "16:9"},
	"x_post": {"name": "Twitter/X Post Image (16:9)", "width": 1200, "height": 675, "ratio": "16:9"},
	"linkedin_post": {"name": "LinkedIn Post Image (1.91:1)", "width": 1200, "height": 628, "ratio": "1.91:1"},
}

#===Tendencias===
@ia_articulo_bp.route('/proyectos/colecciones/image-article')
@validar_sesion
def colecciones_colecciones():
	proyecto_id = request.values.get('pid')
	paltaform_format = "blog_cover" 
	return render_template('sections/colecciones/ia-article/main.html',proyecto_id=proyecto_id, available_models=AVAILABLE_MODELS)

@ia_articulo_bp.route('/proyectos/colecciones/image-article/image', methods=["GET", "POST"])
def image_ia():
	form_params = request.args.to_dict()
	params = form_params
	#Forms
	PRODUCTO = params.get('producto', 'Producto Claro Perú')
	estilo = params.get('estilo_visual', 'clean, modern, premium advertising style')
	COLORES = params.get('colores_base', 'Brand colors: red (#E60000) background with white accents.')
	personas_input = params.get('incluir_personas', 'no')
	if personas_input.lower().startswith('sí') or personas_input.lower().startswith('yes'):
		ESCENA_DETAIL = params.get('elementos_visuales', 'Familia feliz en casa usando dispositivos conectados.')
		INTERACCION = params.get('interaccion_humana', 'Uso Indirecto') 
		ESCENA_CLAUSE = f"Scene detail: Include people. Model type: {personas_input}. Interaction: {INTERACCION}. The main concept is: {ESCENA_DETAIL}"
	else:
		ESCENA_DETAIL = params.get('elementos_visuales', 'Glowing fiber optic waves and advanced technology, implying speed.')
		ESCENA_CLAUSE = f"Scene detail: Focus on technology and abstract visuals without people. The main concept is: {ESCENA_DETAIL}"
	MARCA_ELEMENTOS = params.get('elementos_marca', '')
	if MARCA_ELEMENTOS:
		 ESCENA_CLAUSE += f" Integrate mandatory brand elements: {MARCA_ELEMENTOS}."
	# II & III. CLÁUSULAS TÉCNICAS Y COMPOSICIÓN AVANZADA
	adicionales = []
	if 'contexto_imagen' in params: adicionales.append(f"Lighting: {params['contexto_imagen']}")
	if 'estilo_artistico' in params: adicionales.append(f"Artistic Style: {params['estilo_artistico']}")
	#if 'textura_render' in params: adicionales.append(f"Render Quality: {params['textura_render']}")
	#if 'iluminacion' in params: adicionales.append(f"Lighting: {params['iluminacion']}")
	if 'angulo_camara' in params: adicionales.append(f"Camera Angle: {params['angulo_camara']}")
	if 'emocion_tono' in params: adicionales.append(f"Emotional Tone: {params['emocion_tono']}")
	if 'tipo_fondo' in params: adicionales.append(f"Background/Setting Type: {params['tipo_fondo']}")
	if 'tipo_composicion' in params: adicionales.append(f"Composition Rule: {params['tipo_composicion']}")
	if 'profundidad_campo' in params: adicionales.append(f"Depth of Field: {params['profundidad_campo']} (Bokeh effect).")
	if 'velocidad_implicita' in params and params['velocidad_implicita']:
		adicionales.append(f"Implied Speed: Use {params['velocidad_implicita']} to show dynamism.")
	if 'grado_abstraccion' in params: adicionales.append(f"Abstraction Level: {params['grado_abstraccion']}.")
	clausulas_adicionales = ", ".join(adicionales)
	if clausulas_adicionales:
		clausulas_adicionales = f"Composition and Technical Details: {clausulas_adicionales}."

	#Parametros
	#contexto_imagen = "celebracion de gamefest con personas festejando y consolas de fondo, estilo caricatura anime"
	aspect_ratio = '9:2'
	render_calidad = 'Render 8K'
	#colores_dominantes = 'vibrant red (#E60000) and black, with secondary accents of blue and white'
	#composicion_tecnica = 'The lighting is natural and even, with a normal, eye-level camera angle. Emotional tone conveyed is Speed and Dynamism, achieved through visual cues like lines of light and motion. Composition adheres to the Rule of Thirds, and a soft bokeh effect is applied (Depth of Field: 50). The abstraction level is 20.'
	critical_instructions = ("CRITICAL INSTRUCTIONS: The final output MUST BE A PURE IMAGE ONLY. ABSOLUTELY NO TEXT OVERLAYS, NO LOGOS (regardless of brand or style), ""NO WATERMARKS, NO UI CHROME, NO DEBUG ARTIFACTS, NO BOUNDING BOXES, NO ANNOTATIONS, NO GUIDES, AND NO EXTRA FRAMES. Ensure a pristine, clean image output.")

	# 2. Ensamblaje del Prompt (tal como lo definiste)
	mi_prompt = f"""
	Generate a image for Claro Perú about {PRODUCTO} with a {estilo}, {render_calidad}.
	{ESCENA_CLAUSE}
	{critical_instructions}
	{clausulas_adicionales}
	"""

	data_bytes, mime_type = generar_imagen_imagen4(mi_prompt)

	if data_bytes is None:
		return jsonify({"error": "Fallo al generar la imagen.", "details": "El modelo no devolvió datos."}), 500

	try:
		# 3. Guardar en Google Cloud Storage
		folder_path = "blog_cover" # Un identificador único para el nombre de archivo
		
		# 'name_fileext' es el nombre del archivo dentro del bucket (ej: 20251106_gamefest_banner_abc123.png)
		name_fileext = save_image_to_gcs(
			data=data_bytes, 
			mime_type=mime_type, 
			folder_path=folder_path
		)

		# 4. Generar URL Firmada
		# La función generar_url_firmada requiere el nombre del archivo (blob_name)
		url_firmada = generar_url_firmada(
			bucket_name=bucket_name,
			blob_name=name_fileext # Pasamos solo el nombre del archivo
		)
		# 4. Save
		imageia_id = generarCodigo("IA");
		imgia_name = name_fileext
		imgia_promt = mi_prompt
		imgia_type = "blog"
		imgia_fecha = fechaActual()
		proyecto_id = params.get('txt_pid', '')

		new_data = Imagesia(
			imgia_id = imageia_id,
			imgia_name = imgia_name,
			imgia_promt = imgia_promt,
			imgia_type = imgia_type,
			imgia_fecha = imgia_fecha,
			imgia_estado = 1,
			proyecto_id = proyecto_id
		)
		db.session.add(new_data)
		db.session.commit()
		# 5. Devolver la URL
		return jsonify({
			"success": True,
			"message": "Imagen generada y guardada en GCS.",
			"imagen_temporal": url_firmada,
			"nombre_archivo": name_fileext
		})

	except Exception as e:
		# Esto captura errores de GCS (conexión, permisos, etc.)
		return jsonify({"error": f"Error al guardar o firmar la URL: {str(e)}"}), 500

def generar_imagen_imagen4(prompt: str):
	try:
		# Aquí debes asegurarte de que la clave API esté disponible
		# Nota: Es altamente inseguro dejar la clave API dura en el código. Úsala solo para desarrollo/prueba.
		clave_secreta_gemini = os.environ.get("GEMINI_API_KEY", "AIzaSyBjLIPcIzCY6zuWJdiikno0sWHpilbwLw4")
		if not clave_secreta_gemini:
			print("Error: Clave GEMINI_API_KEY no configurada.", file=sys.stderr)
			return None, None
			
		client = genai.Client(api_key=clave_secreta_gemini)
		
		response = client.models.generate_images(
			model='imagen-4.0-generate-001',
			prompt=prompt,
			config=types.GenerateImagesConfig(
				number_of_images=1,
				#  CAMBIO 1: Usamos el parámetro aspect_ratio en la configuración
				aspect_ratio='16:9',
			)
		)

		if response.generated_images:
			img_bytes = response.generated_images[0].image.image_bytes
			mime_type = 'image/png'
			
			#  CAMBIO 2: Devuelve los bytes y el tipo MIME (para GCS)
			return img_bytes, mime_type
		else:
			print("No se pudo generar la imagen. La respuesta no contiene imágenes generadas.", file=sys.stderr)
			return None, None

	except Exception as e:
		print(f"Ocurrió un error en la generación: {e}", file=sys.stderr)
		return None, None

# --- FUNCIONES AUXILIARES (Sin Cambios Relevantes) ---
def save_image_to_gcs(data, mime_type, folder_path) -> str:
	if isinstance(data, str):
		data_bytes = base64.b64decode(data)
	else:
		data_bytes = data
	ext = mimetypes.guess_extension(mime_type)
	ext = ext.lstrip('.') if ext else "png" 
	fecha_utc = datetime.datetime.utcnow().strftime('%Y%m%d')
	name_archivo = f"{fecha_utc}_{folder_path}_{uuid.uuid4().hex}"
	name_fileext = f"{name_archivo}.{ext}"
	nombre_archivo = f"generate/blog/{name_fileext}" 
	bucket = storage_client.bucket(bucket_name)
	blob = bucket.blob(nombre_archivo)
	blob.upload_from_string(data_bytes, content_type=mime_type)
	return name_fileext

def generar_url_firmada(bucket_name, blob_name):
	bucket = storage_client.bucket(bucket_name)
	blob_path = f"generate/blog/{blob_name}"
	blob = bucket.blob(blob_path)
	url = blob.generate_signed_url(
		version="v4",
		expiration=datetime.timedelta(minutes=15),
		method="GET",
	)
	return url