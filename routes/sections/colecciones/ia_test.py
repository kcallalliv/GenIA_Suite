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
from PIL import Image
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

ia_test_bp = Blueprint('ia_test_bp', __name__)
@ia_test_bp.route('/proyectos/testia')
def test_ia():
	contexto_imagen = "celebracion de gamefest con personas festejando y consolas de fondo, estilo caricatura anime"
	aspect_ratio = '9:2'
	estilo = 'Clean and Modern'
	render_calidad = 'Render 8K'
	colores_dominantes = 'vibrant red (#E60000) and black, with secondary accents of blue and white'
	composicion_tecnica = 'The lighting is natural and even, with a normal, eye-level camera angle. Emotional tone conveyed is Speed and Dynamism, achieved through visual cues like lines of light and motion. Composition adheres to the Rule of Thirds, and a soft bokeh effect is applied (Depth of Field: 50). The abstraction level is 20.'
	critical_instructions = ("CRITICAL INSTRUCTIONS: The final output MUST BE A PURE IMAGE ONLY. ABSOLUTELY NO TEXT OVERLAYS, NO LOGOS (regardless of brand or style), ""NO WATERMARKS, NO UI CHROME, NO DEBUG ARTIFACTS, NO BOUNDING BOXES, NO ANNOTATIONS, NO GUIDES, AND NO EXTRA FRAMES. Ensure a pristine, clean image output.")

	# 2. Ensamblaje del Prompt (tal como lo definiste)
	mi_prompt = f"""
	Generate a high-quality, {render_calidad} promotional image. The style is {estilo}. Dominant colors are {colores_dominantes}.	
	The scene depicts: {contexto_imagen}
	Technical Details: {composicion_tecnica}
	{critical_instructions}
	"""

	#mi_prompt = "Generate a high-quality, Render 8K promotional image. The style is Clean and Modern. Dominant colors are vibrant red (#E60000) and black, with secondary accents of blue and white. The canvas dimensions are exactly 1800x400 pixels (Aspect Ratio: 9:2). The scene depicts a modern, warm living room. A Latino family, wearing sports jerseys with a red and white diagonal stripe pattern (similar to Peru national team jerseys), is shown in the setting, indirectly engaging with connectivity. The central concept illustrates dynamic, glowing waves of light, representing high-speed data flow, subtly connecting various digital devices, including a prominent white Wi-Fi 6 Router. The lighting is natural and even, with a normal, eye-level camera angle. The emotional tone conveyed is Speed and Dynamism, achieved through visual cues like lines of light and motion. Composition adheres to the Rule of Thirds, and a soft bokeh effect is applied (Depth of Field: 50). The abstraction level is 20.CRITICAL INSTRUCTIONS: The final output MUST BE A PURE IMAGE ONLY. ABSOLUTELY NO TEXT OVERLAYS, NO LOGOS (regardless of brand or style), NO WATERMARKS, NO UI CHROME, NO DEBUG ARTIFACTS, NO BOUNDING BOXES, NO ANNOTATIONS, NO GUIDES, AND NO EXTRA FRAMES. Ensure a pristine, clean image output."
	#mi_prompt = "Un perro astronauta de estilo ilustración cómic, leyendo un libro en la luna"

	# Llama a la función, que ahora devuelve BytesIO o None
	img_io = generar_imagen_imagen4(mi_prompt)
	
	if img_io:
		# Flask ahora tiene una respuesta válida (el archivo binario)
		return send_file(
			img_io,
			mimetype='image/png',
			as_attachment=False # Muestra la imagen directamente en el navegador
		)
	else:
		# Devuelve un mensaje de error válido para Flask
		return jsonify({"error": "No se pudo generar la imagen o faltaba la API Key."}), 500

def generar_imagen_imagen4(prompt: str): # Nota: Eliminamos 'nombre_archivo'
	"""
	Genera una imagen usando 'imagen-4.0-generate-001' y devuelve un objeto BytesIO.

	Args:
		prompt (str): La instrucción de texto (prompt) para la generación.
	Returns:
		BytesIO: Objeto BytesIO con la imagen PNG, o None en caso de error.
	"""
	try:
		# Aquí debes asegurarte de que la clave API esté disponible
		clave_secreta_gemini = os.environ.get("GEMINI_API_KEY","AIzaSyBjLIPcIzCY6zuWJdiikno0sWHpilbwLw4") 
		if not clave_secreta_gemini:
			# Evitar error de API, pero devolver None
			print("Error: Clave GEMINI_API_KEY no configurada.")
			return None 
			
		client = genai.Client(api_key=clave_secreta_gemini)
		
		response = client.models.generate_images(
			model='imagen-4.0-generate-001',
			prompt=prompt,
			config=types.GenerateImagesConfig(
				number_of_images=1,
				aspect_ratio='16:9',
			)
		)

		if response.generated_images:
			img_bytes = response.generated_images[0].image.image_bytes
			
			img_io = BytesIO(img_bytes)
			img_io.seek(0)
			
			# ¡Devuelve el objeto BytesIO!
			return img_io 
		else:
			print("No se pudo generar la imagen.", file=sys.stderr)
			return None

	except Exception as e:
		print(f"Ocurrió un error en la generación: {e}", file=sys.stderr)
		return None