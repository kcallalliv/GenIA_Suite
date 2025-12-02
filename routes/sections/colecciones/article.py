# routes/alerts.py
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from google.cloud import bigquery
from google import genai
from google.genai.types import HttpOptions
from google.api_core.client_options import ClientOptions
from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
from google.genai import types
from functools import wraps
from datetime import datetime
from datetime import timedelta
import datetime
import sys
import os
import json
import re
import hashlib
import difflib
import requests
import random
import string
from io import BytesIO
import mimetypes
from docx import Document
from docx.shared import Inches
import pandas as pd
import traceback # Asume que pandas está importado
import uuid
# Importaciones necesarias para la creación manual del hipervínculo:
import docx.opc.constants
import docx.oxml.shared
import docx.text.run
from docx.oxml.ns import qn
from docx.enum.dml import MSO_THEME_COLOR
from docx.shared import RGBColor, Pt 
#llamar a config
from routes.models import db, Assets, Keywords, Imagesia, Configuracion
from routes.config.geniaconfig import bq_client, bucket_name, storage_client, bq_table_config, genai_client, bq_table_brands, validar_sesion, fechaActual, generarCodigo

client = bigquery.Client(project="prd-claro-mktg-data-storage")

cltarticle_bp = Blueprint('cltarticle_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/colecciones/article/')

@cltarticle_bp.route('/')
@validar_sesion
def article_main(brand_id,proyecto_id):
	key_id = request.values.get('keyid')
	pid = proyecto_id
	data = Keywords.query.filter_by(keyword_id=key_id).first()
	return render_template('sections/colecciones/article/generate-main.html',data=data,pid=pid)

@cltarticle_bp.route('images', methods=['GET', 'POST'])
@validar_sesion
def article_images(brand_id,proyecto_id):
	pid = request.values.get('pid')
	lista = listarImages(pid)
	return render_template('sections/colecciones/article/images.html',lista=lista,generar_url_firmada=generar_url_firmada)

@cltarticle_bp.route('generated-title', methods=['GET', 'POST'])
def generaTitleIA(brand_id, proyecto_id):
	tipo_contenido = request.values.get('tipo')
	tema = request.values.get('tema')
	keyword = request.values.get('keyword')

	try:
		tipo_final_para_prompt = tipo_contenido
		# --- Construcción del Prompt (Instrucción simplificada) ---
		prompt = (
			"Eres un experto en SEO y Content Marketing con más de 20 años de experiencia, especializado en crear títulos de alto impacto y orientados al usuario peruano. "
			"Tu único objetivo es generar un título que sea atractivo, **que contenga obligatoriamente la Keyword Principal** y utilice el Tipo de Contenido y el Tema Específico como **contexto y guía creativa**.\n\n"
			
			# --- DELIMITADOR DE DATOS DE ENTRADA ---
			"**DATOS DE ENTRADA:**\n"
			f"Keyword Principal: {keyword}\n"
			f"Tipo de Contenido: {tipo_final_para_prompt}\n"
			f"Tema Específico: {tema}\n"
			"**FIN DE DATOS DE ENTRADA.**\n\n"
			
			# --- INSTRUCCIONES ESTRICTAS DE SALIDA ---
			"**INSTRUCCIÓN CLAVE:** Genera **SOLO** el texto del título principal. La salida debe ser una **única línea de texto**.\n"
			"**USO DE KEYWORD:** El título debe incluir la Keyword Principal, pero **NO es necesario que aparezca al inicio**. Intégrala de forma natural en cualquier parte de la frase que tenga sentido semántico.\n"
			"**FORMATO Y ESTRUCTURA:** El título debe ser una **frase fluida y natural**. **ESTÁ TERMINANTEMENTE PROHIBIDO** usar la estructura 'Tema: Título'. **SUSTITUCIÓN OBLIGATORIA:** Si vas a usar dos puntos (:) para separar una idea, **USA UNA COMA (,)** en su lugar. La coma es tu separador principal.\n"
			"**ESTILO DE TÍTULO:** Genera títulos informativos o de lista, **EVITANDO** el formato de pregunta directa (signos ¿?) y frases genéricas. Céntrate en el valor del tema.\n"
			"**ORTOGRAFÍA Y CAPITALIZACIÓN:** El título debe seguir las reglas ortográficas del español. Usa mayúscula **solo** al inicio de la frase y en nombres propios.\n"
			"**PROHIBICIÓN ABSOLUTA:** NO incluyas el carácter de **dos puntos (:)** bajo ninguna circunstancia. Si el título generado lo tiene, elimínalo y reestructura la frase.\n\n"
			
			# --- INSTRUCCIÓN FINAL DE ANIQUILACIÓN DE TEXTO DE RELLENO ---
			"**NO** incluyas ninguna explicación, introducción, comentario o frase de verificación de datos. **SOLO** el título final."
		)
		# --- Llamada a Gemini ---
		# Asegúrate de que 'genai_client' esté definido e inicializado correctamente antes de esta función
		# response = genai_client.models.generate_content(...) 
		
		# Simulando la respuesta para que el código sea funcional en este contexto
		# contenido_generado = "El Mejor título sobre **hogar** y **celulares** que contenga la palabra **claro**"
		
		# Usando la línea original, asumiendo que 'genai_client' está definido
		response = genai_client.models.generate_content(
			model="gemini-2.0-flash-001",
			contents=prompt
		)
		contenido_generado = response.text

		# --- Extracción y Retorno del Título (El parser) ---
		# Si pedimos negritas, buscamos el patrón: ** (Texto del título) **
		match = re.search(r'\*\*([^*]+)\*\*', contenido_generado)
		result_title = "" # Inicializar variable

		if match:
			result_title = match.group(1).strip()
		else:
			# Si la IA no usa negritas, devolvemos el texto completo y limpio
			result_title = contenido_generado.strip()
		
		# Verificación de longitud para manejo de errores de formato
		if len(result_title) < 5:
			# Si es muy corto, aún lo devolvemos, pero se puede considerar un error si es crítico
			pass

		return jsonify({
			"success": True,
			"title": result_title
		})
		
	except Exception as e:
		error_msg = f"ERROR: Fallo crítico en la función generaTitleIA: {e}"
		
		# 🚨 SOLUCIÓN: Usamos el logger estándar en lugar de st.error
		logging.error(error_msg) 
		
		result_title = f"Error de ejecución: {e}"
		return jsonify({
			"success": False,
			"title": result_title
		})
@cltarticle_bp.route('article-content', methods=['GET', 'POST'])
def generaContenidoIA(brand_id, proyecto_id):
	# --- 1. Datos de Entrada ---
	tipo_contenido = request.values.get('tipo')
	tema = request.values.get('tema')
	title = request.values.get('titulo')
	keyword = request.values.get('keyword')

	# --- 2. Configuración y Contexto ---
	json_contenido = get_json_tipo_contenido()
	detalles_tipo = json_contenido.get(tipo_contenido, {})
	intencion = detalles_tipo.get("intencion", "Contratar o mejorar servicio")
	
	contexto_vertex = obtener_contexto_vertex(keyword)
	urls_df = get_urls_existentes()
	similares_df = get_urls_similares_por_keyword(keyword, urls_df)
	sugerencias_urls = elegir_urls_relevantes_con_gemini(keyword, similares_df)

	# --- 3. Lógica de Selección de Producto (Python) ---
	# Esto decide de qué hablar ANTES de llamar a la IA para asegurar el enfoque comercial.
	kw_lower = keyword.lower()
	instruccion_producto = ""

	if any(x in kw_lower for x in ['internet', 'wifi', 'velocidad', 'hogar', 'fibra', 'lento', 'router']):
		instruccion_producto = (
			"**ENFOQUE DE PRODUCTO (OBLIGATORIO):**\n"
			"El tema central debe ser la **Fibra Óptica de Claro**.\n"
			"- Destaca: Estabilidad, velocidad simétrica (subida=bajada) y cobertura.\n"
			"- Argumento: 'La red más estable para trabajar, estudiar y jugar sin lag'."
		)
	elif any(x in kw_lower for x in ['celular', 'movil', 'chip', 'datos', 'prepago', 'recarga', 'megas']):
		instruccion_producto = (
			"**ENFOQUE DE PRODUCTO (OBLIGATORIO):**\n"
			"El tema central debe ser **Claro Prepago** (énfasis en economía/recargas) o **Planes Postpago Max**.\n"
			"- Destaca: Cobertura nacional, apps ilimitadas y beneficios exclusivos."
		)
	elif any(x in kw_lower for x in ['tv', 'cine', 'pelicula', 'series', 'streaming', 'cable']):
		instruccion_producto = (
			"**ENFOQUE DE PRODUCTO (OBLIGATORIO):**\n"
			"El tema central debe ser **Claro TV+** y los beneficios de **Claro Video**.\n"
			"- Destaca: Que los planes incluyen acceso a contenido y Paramount+ (según vigencia)."
		)
	else:
		# Default si la keyword es muy genérica
		instruccion_producto = (
			"**ENFOQUE DE PRODUCTO:**\n"
			"Menciona sutilmente cómo la tecnología y conectividad de **Claro** resuelven la necesidad del usuario."
		)

	try:
		# --- 4. Construcción del Prompt (Optimizado) ---
		prompt = (
			f"Actúa como el **Redactor Senior de Productos y Ventas Digitales de Claro Perú**.\n"
			"Tu objetivo es crear un artículo útil, experto y altamente persuasivo que posicione a Claro como la mejor solución.\n\n"

			f"**DATOS DEL ARTÍCULO:**\n"
			f"- Keyword Principal: {keyword}\n"
			f"- Tema: {tema}\n"
			f"- Título Pre-aprobado: {title}\n"
			f"- URLs para sugerir al final: {sugerencias_urls}\n\n"

			f"{instruccion_producto}\n\n"

			f"**INFORMACIÓN DE BASE (Vertex AI):**\n{contexto_vertex}\n\n"

			"**REGLAS DE REDACCIÓN Y ESTILO (ESTRICTAS):**\n"
			"1. **CAPITALIZACIÓN (Sentence Case):** Está prohibido usar MAYÚSCULAS SOSTENIDAS en títulos[title] o subtítulos[subtitle]. Usa siempre 'Tipo oración' (Ej: 'Internet en casa: Lo que necesitas saber'). Solo la primera letra va en mayúscula.\n"
			"2. **PUNTUACIÓN:** NUNCA termines un título o subtítulo con dos puntos (:), punto (.) o punto y coma (;).\n"
			"3. **MARCA:** Menciona 'Claro' de forma natural. Convierte características técnicas en beneficios emocionales.\n"
			"4. **ENLACES:** Sugiere visitar otras secciones usando frases naturales como 'como te contamos en...', 'puedes ver más detalles en...'.\n\n"

			"**FORMATO DE SALIDA (ESTRICTO):**\n"
			"Usa EXACTAMENTE estas etiquetas:\n\n"

			"[title] <Escribe aquí el Título H1>\n"
			"Atractivo, CAPITALIZACIÓN (Sentence Case), sin dos puntos finales.\n\n"

			"[intro] <Párrafo introductorio>\n"
			"Enganche (máx 4 líneas). La keyword principal ('" + keyword + "') debe estar en negrita.\n\n"

			"[subtitle] <Primer Subtítulo H2>\n"
			"Sentence Case. Sin dos puntos.\n\n"

			"**Cuerpo del artículo:** Desarrolla el tema entre 600 y 1200 palabras. Todos los subtítulos dentro del cuerpo del artículo también deben estar en negrita (usando ****).\n"
			". Cada sección debe estar separada por saltos de línea (párrafos vacíos entre ellas).\n\n"
			"[text]\n"
			"Desarrolla el contenido aquí. Usa párrafos cortos.\n"
			"- **NO uses viñetas (bullets).** Si enumeras características, escribe: <strong>Característica:</strong> Descripción.\n"
			"- Si necesitas otro subtítulo, usa la etiqueta [subtitle] nuevamente, seguida de [text].\n"
			"- Integra la marca Claro de forma natural.\n\n"

			"Si hay URLs sugeridas muestra el title:\n"
			"[title] URLs Sugeridas\n"
			"Si hay URLs sugeridas arriba, lístalas así:\n"
			"[item-link=URL_AQUI]\n\n"

			"[meta_title]\n"
			"Título SEO (Máx 65 chars) | Hablando Claro\n\n"

			"[meta_description]\n"
			"Resumen SEO (Máx 155 chars).\n"
		)

		# --- 5. Llamada a Gemini ---
		response = genai_client.models.generate_content(
			model="gemini-2.0-flash-001",
			contents=prompt
		)
		
		contenido_generado = response.text.strip()

		# Validación simple
		if len(contenido_generado) < 50:
			 return "ERROR: Contenido insuficiente generado por la IA."

		return jsonify({
			"success": True,
			"title": contenido_generado 
		})
	except Exception as e:
		error_msg = f"ERROR en generaContenidoIA: {e}"
		print(error_msg)
		return f"Error: {e}"
def get_json_tipo_contenido():
	base_dir = os.path.dirname(os.path.abspath(__file__))
	json_file_path = os.path.join(base_dir, '..', '..', '..', 'static', 'json', 'json_tipo-contenido.json')
	contenido_list = []
	try:
		with open(json_file_path, 'r', encoding='utf-8') as f:
			data = json.load(f) # Carga el JSON tal cual
		return data # Retorna el diccionario directamente
	except FileNotFoundError:
		print(f"Error: El archivo JSON no se encontró en la ruta: {json_file_path}")
		return []
	except json.JSONDecodeError:
		print(f"Error: No se pudo decodificar el archivo JSON '{json_file_path}'. Asegúrate de que sea un JSON válido.")
		return []
	except Exception as e:
		print(f"Ocurrió un error inesperado al cargar el JSON: {e}")
		return []
def get_urls_existentes():
	query = """
	SELECT * FROM prd-claro-mktg-data-storage.project_semantic_seo.hablando_claro_url
	"""
	return client.query(query).to_dataframe()
def elegir_urls_relevantes_con_gemini(keyword, urls_df):
	if urls_df.empty:
		return "No se encontraron URLs similares para sugerir."
	if 'page_url' not in urls_df.columns:
		return "Error interno: columna 'page_url' no encontrada."

	urls_texto = "\n".join([f"- {row['page_url']}" for _, row in urls_df.iterrows()])
	prompt = f"""
	Eres un experto en SEO. Tu tarea es identificar las 3 URLs más relevantes para una correcta implementación de enlaces internos.

	**Keyword Principal del Artículo:** '{keyword}'

	**Lista de URLs DISPONIBLES (SOLO puedes usar URLs de esta lista, NO inventes ni modifiques):**
	{urls_texto}

	**INSTRUCCIONES DE SALIDA ESTRICTAS:**
	Genera SOLO un listado numérico de 3 URLs. Cada URL debe estar en una nueva línea, precedida por su número y un punto, y sin ningún texto adicional o explicaciones.

	EJEMPLO DE FORMATO DE SALIDA (EXACTO):
	1. https://www.ejemplo.com/primera-url
	2. https://www.ejemplo.com/segunda-url
	3. https://www.ejemplo.com/tercera-url

	Asegúrate de que las URLs seleccionadas sean las más lógicamente relacionadas con la keyword principal.
	"""
	try:
		response = genai_client.models.generate_content(
			model="gemini-2.0-flash-001",
			contents=prompt
		)
		gemini_raw_response = response.text.strip()
		url_pattern = re.compile(r'^\d+\.\s*(https?://\S+)$', re.MULTILINE)
		suggested_urls = url_pattern.findall(gemini_raw_response)
		return suggested_urls if suggested_urls else "No se encontraron URLs relevantes para sugerir."
	except Exception as e:
		print(f"ERROR: elegir_urls_relevantes_con_gemini falló con una excepción: {e}")
		return "Error al generar sugerencias de URLs."
def get_urls_similares_por_keyword(keyword, urls_df):
	print(f"INFO: Buscando URLs similares para keyword: '{keyword}'")
	textos = urls_df["page_url"].tolist()
	# Asegúrate de que 'textos' no esté vacío antes de llamar a difflib.get_close_matches
	if not textos:
		print("ADVERTENCIA: No hay URLs en el DataFrame para buscar coincidencias.")
		return pd.DataFrame()
	matches = difflib.get_close_matches(keyword, textos, n=10, cutoff=0.2)
	print(f"INFO: Coincidencias de URLs encontradas: {matches}")
	return urls_df[urls_df["page_url"].isin(matches)].reset_index(drop=True)
def obtener_contexto_vertex(keyword):
	print(f"INFO: Obtener contexto de Vertex AI Search para keyword: '{keyword}'")
	project_id = "prd-claro-mktg-data-storage"
	location = "global"
	engine_id = "claro-peru_1748977843565"

	try:
		# Asegúrate de que todas las clases necesarias (ClientOptions, etc.) estén importadas en tu archivo.
		client_options = ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com") if location != "global" else None
		client = discoveryengine.ConversationalSearchServiceClient(client_options=client_options)

		serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_serving_config"

		answer_generation_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
			ignore_adversarial_query=True,
			ignore_non_answer_seeking_query=True,
			ignore_low_relevant_content=False,
			model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(model_version="stable"),
			prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
				preamble="Usa la información más relevante de tus fuentes indexadas, brinda el contexto necesario para usar info dentro de un articulo de Claro, comparte 3 urls relacionadas para que puedan buscar informacion mas detallada los usuarios."
			),
			include_citations=True,
			answer_language_code="es",
		)

		request = discoveryengine.AnswerQueryRequest(
			serving_config=serving_config,
			query=discoveryengine.Query(text=keyword),
			session=None,
			answer_generation_spec=answer_generation_spec,
		)

		print(f"INFO: Enviando solicitud a Vertex AI Search para keyword: '{keyword}'")
		response = client.answer_query(request)
		print(f"INFO: Respuesta de Vertex AI Search recibida. ¿Contiene respuesta?: {bool(response.answer)}")
		
		# Uso de acceso seguro (aunque ya lo tenías, lo mantenemos robusto)
		return response.answer.answer_text if response.answer and response.answer.answer_text else "No se pudo generar una respuesta de contexto relevante."
		
	except Exception as e:
		# 🛠️ CORRECCIÓN: Se elimina la línea 'st.error()' para evitar el NameError.
		# st.error(f"ERROR al obtener contexto de Vertex AI Search: {e}") 
		
		print(f"ERROR: obtener_contexto_vertex falló con: {e}")
		return f"Error al obtener contexto: {e}"
#Html Select json
@cltarticle_bp.route('select-tipo-contenido', methods=['GET', 'POST'])
def get_tipo_contenido(brand_id,proyecto_id):
	base_dir = os.path.dirname(os.path.abspath(__file__))
	#json_file_path = os.path.join(base_dir, '..', 'static', 'json', 'json_tipo-contenido.json')
	json_file_path = os.path.join(base_dir, '..', '..', '..', 'static', 'json', 'json_tipo-contenido.json')
	print(f"DEBUG: Intentando abrir el archivo en: {json_file_path}") 
	# ¡INICIALIZA la lista aquí!
	contenido_list = [] 
	try:
		with open(json_file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		# Listar y construir la lista de diccionarios
		for tipo, detalles in data.items():
			contenido_item = {
				"nombre_tipo": tipo,
				"intencion": detalles.get("intencion", "N/A"),
				"descripcion": detalles.get("descripcion", "N/A"),
				"ejemplo": detalles.get("ejemplo", "N/A")
			}
			contenido_list.append(contenido_item)

		html_output = '<select id="cbo_tipo_articulo" name="cbo_tipo_articulo">\n'
		html_output += '\t<option value="">Selecciona una palabra</option>\n'
		for item in contenido_list:
			nombre = item["nombre_tipo"]
			html_output += f'\t<option value="{nombre}">{nombre}</option>\n'
		html_output += '</select>'
		return html_output
	except FileNotFoundError:
		print(f"Error: El archivo '{json_file_path}' no se encontró.")
		return "Error: Archivo de tipos de contenido no encontrado.", 500 
	except json.JSONDecodeError:
		print(f"Error: No se pudo decodificar el archivo JSON '{json_file_path}'. Asegúrate de que sea un JSON válido.")
		return "Error: Formato de archivo de tipos de contenido inválido.", 500
	except Exception as e:
		print(f"Ocurrió un error inesperado al cargar el JSON: {e}")
		return f"Error interno del servidor: {e}", 500
#Crear Documento Word
def crear_docx(texto_contenido, name_file):
	document = Document()
	
	# El nombre del archivo se infiere del keyword (name_file)
	inferred_keyword = name_file.replace(".docx", "").replace("_", " ").title()
	
	# Lista de líneas
	lines = texto_contenido.strip().split('\n')
	
	# -----------------------------------------------------
	# 1. Procesamiento de Líneas con Marcado Personalizado
	# -----------------------------------------------------
	
	# Bandera para saber si estamos procesando la sección de URLs Sugeridas
	in_url_section = False
	
	for line in lines:
		line = line.strip()
		if not line:
			continue

		if line.startswith('[title]'):
			title_text = line.replace('[title]', '').strip()
			
			if "urls sugeridas" in title_text.lower():
				document.add_heading(title_text, level=3)
				in_url_section = True
			else:
				# Título principal del artículo (H1 en el HTML, H2 en el DOCX)
				document.add_heading(title_text, level=1)
				in_url_section = False

		elif line.startswith('[intro]'):
			intro_text = line.replace('[intro]', '').strip()
			# La introducción va como un párrafo destacado o con sangría
			# Nota: Si 'Intense Quote' tampoco existe, deberás usar style=None o 'Quote'.
			document.add_paragraph(intro_text, style='Intense Quote') 

		elif line.startswith('[subtitle]'):
			subtitle_text = line.replace('[subtitle]', '').strip()
			# Subtítulo de sección (H2 en el HTML, H3 en el DOCX)
			document.add_heading(subtitle_text, level=3)
			in_url_section = False

		elif line.startswith('[text]'):
			text_content = line.replace('[text]', '').strip()
			
			# ⚠️ Manejo de Enlaces (Link) dentro del [text]
			# Patrón: [link=URL]TEXTO DEL ENLACE[/link]
			link_regex = re.compile(r'\[link=(.*?)\](.*?)\[\/link\]')
			
			p = document.add_paragraph()
			last_idx = 0
			
			# Buscar y reemplazar todos los enlaces
			for match in link_regex.finditer(text_content):
				url = match.group(1)
				link_text = match.group(2)
				
				# Agregar el texto que está ANTES del enlace
				p.add_run(text_content[last_idx:match.start()])
				
				# Agregar el enlace usando la función auxiliar (¡CORRECCIÓN AQUÍ!)
				# Asumimos que add_hyperlink(p, url, link_text) ya está definida e implementada.
				add_hyperlink(p, url, link_text)
				
				last_idx = match.end()
			
			# Agregar el texto que queda DESPUÉS del último enlace
			p.add_run(text_content[last_idx:])
			in_url_section = False

		elif line.startswith('[item-link='):
			if in_url_section:
				# Patrón: [item-link=URL_AQUI]
				match = re.search(r'\[item-link=(.*?)\]', line)
				if match and match.group(1):
					url = match.group(1)
					
					# Añadir URL como un elemento de lista con Hyperlink
					p = document.add_paragraph(style='List Bullet')
					
					# 💥 CORRECCIÓN CRÍTICA: Se reemplaza la línea con error por la auxiliar
					add_hyperlink(p, url, url) # Texto del link es la URL misma
	
	# -----------------------------------------------------
	# 2. Guardar y Devolver el Buffer
	# -----------------------------------------------------

	# Opcional: Añadir un pie de página o metadatos de generación si es necesario
	document.add_page_break()
	document.add_heading("Metadatos de Generación", level=4)
	document.add_paragraph(f"Keyword: {inferred_keyword}")
	document.add_paragraph(f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

	buffer = BytesIO()
	document.save(buffer)
	buffer.seek(0)
	return buffer
def add_hyperlink(paragraph, url, text, color=None, underline=True):
	"""
	Agrega un hipervínculo a un objeto Paragraph sin depender del estilo 'Hyperlink'.
	"""
	# 1. Relacionar la URL externa con el documento (parte del XML de Word)
	part = paragraph.part
	r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

	# 2. Crear el elemento XML <w:hyperlink>
	hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
	hyperlink.set(qn('r:id'), r_id, )
	
	# 3. Crear el Run (el texto visible)
	new_run = docx.text.run.Run(
		docx.oxml.shared.OxmlElement('w:r'), paragraph
	)
	new_run.text = text

	# 4. Aplicar formato (azul y subrayado)
	new_run.font.underline = underline
	if not color:
		# Usar color azul por defecto de hipervínculo
		new_run.font.color.theme_color = MSO_THEME_COLOR.HYPERLINK
	else:
		new_run.font.color.rgb = color
	
	# 5. Insertar el Run dentro del Hyperlink, e insertar el Hyperlink en el párrafo
	hyperlink.append(new_run.element)
	paragraph._p.append(hyperlink)
	
	return new_run
@cltarticle_bp.route('/proyectos/colecciones/article/download-generated-article', methods=['POST'])
def download_generated_article():
	# Recuperar el contenido guardado en la sesión
	texto_plain_for_docx = request.values.get('content')
	keyword_for_docx = request.values.get('keyword')
	data_titulo = request.values.get('titulo')
	if not texto_plain_for_docx or not keyword_for_docx:
		# Si no hay contenido en la sesión, redirigir o mostrar un error
		return "No hay artículo para descargar. Por favor, genera un artículo primero.", 400
	name_file = f"{keyword_for_docx}_articulo.docx"
	# Llamar a crear_docx con los datos recuperados de la sesión
	docx_buffer = crear_docx(texto_plain_for_docx, name_file)
	# Retornar el archivo como una respuesta de Flask
	return send_file(
		docx_buffer,
		mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		as_attachment=True,
		download_name=name_file
	)



@cltarticle_bp.route('generated-image', methods=["GET", "POST"])
def generateImageIA(brand_id,proyecto_id):
	data_prompt = request.args.get('promt', '')
	data_bytes, mime_type = generar_imagen_imagen4(data_prompt)

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
		imgia_promt = data_prompt
		imgia_type = "blog"
		imgia_fecha = fechaActual()
		proyecto_id = request.values.get('txt_pid', '')

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

from flask import request, jsonify # Asegúrate de tener estas importaciones

@cltarticle_bp.route('generated-promt', methods=["GET"])
def generatePromtImageIA(brand_id, proyecto_id):
	# 1. RECUPERAR PARÁMETROS DE LA SOLICITUD GET
	tipo_articulo = request.args.get('tipo', '')
	tema_articulo = request.args.get('tema', '')
	keyword_articulo = request.args.get('keyword', '')
	titulo_articulo = request.args.get('titulo', '')
	motivo_articulo = request.args.get('motivo', '')
	# Valores fijos de ejemplo, reemplaza 'Claro Perú' según la lógica de tu aplicación
	producto_nombre = "Producto Claro Perú" 
	brand_name = "Claro Perú"
	
	# --- INICIO DE LA LÓGICA DE CONSTRUCCIÓN DEL PROMPT ---
	
	# Parámetros Fijos o Base
	background_setting = "Living de hogar moderno y cálido"
	render_calidad = 'Render 8K'
	
	# 2. Ajustar el Tono Emocional y Estilo Visual según el Tipo (Lógica existente)
	estilo_visual = "clean, modern, premium advertising style"
	tono_emocional = "Calma y Seguridad" # Valor por defecto ajustado a tu ejemplo

	if tipo_articulo.lower() == "educativo":
		estilo_visual = "minimalist, informative, friendly visual style"
		tono_emocional = "Confianza, Claridad y Aprendizaje"
	elif tipo_articulo.lower() == "guía":
		estilo_visual = "detailed, structured, high-quality rendering style"
		tono_emocional = "Organización, Eficiencia y Logro"

	# 3. Preparar Cláusulas para Ensamblaje
	
	# Secciones principales del prompt
	producto = f"producto: {producto_nombre}"
	concepto_principal = f"The main concept is: {tema_articulo}, emphasizing the use of the {keyword_articulo} service."
	
	# Modificación para elementos visuales base y keyword
	elementos_visuales_final = f"debe incorporar de forma sutil elementos visuales relacionados con la palabra clave '{keyword_articulo}'."
	
	# a. CLÁUSULAS PRINCIPALES (Scene Clause)
	escena_clausulas = [
		producto,
		f"estilo_visual: {estilo_visual}",
		"Model type: si",
		"Interaction: Uso Indirecto",
		concepto_principal,
		f"elementos_visuales: {elementos_visuales_final}"
	]
	if titulo_articulo:
		escena_clausulas.append(f"El contexto de la imagen debe visualizar el concepto principal de: '{titulo_articulo}'")
	if motivo_articulo:
		escena_clausulas.append(f"Motivo y Enfoque de la imagen: la imagen se genera para: '{motivo_articulo}'")
	else:
		elementos_visuales_base = "Familia tradicional (padres hombre y mujer) en casa usando dispositivos conectados."
		escena_clausulas.append(f"Motivo y Enfoque de la imagen: la imagen se genera para: '{elementos_visuales_base}'")
	escena_clause_str = ", ".join(escena_clausulas)
	# b. DETALLES DE COMPOSICIÓN Y TÉCNICOS (Technical Details Clause)
	# Se ajustan las cláusulas a tu ejemplo, eliminando las que no estaban o ajustando el formato
	adicionales = [
		"Contexto Imagen: ",  # Se mantienen las dos cláusulas vacías
		"Contexto Imagen: ",
		"Artistic Style: realistic",
		"Lighting: Luz de estudio suave",
		"Camera Angle: Normal (Eye-level)",
		f"Emotional Tone: {tono_emocional}",
		f"Background/Setting Type: {background_setting}",
		"Composition Rule: Regla de Tercios",
		"Depth of Field: 50 (Bokeh effect)."
		# Se eliminan: Implied Speed, Abstraction Level (no estaban en tu ejemplo estricto)
	]
	
	clausulas_adicionales_str = ", ".join(adicionales)
	# Ensamblaje de la sección de detalles técnicos, solo si hay contenido
	if clausulas_adicionales_str:
		clausulas_adicionales_final = f"Composition and Technical Details: {clausulas_adicionales_str}"
	else:
		clausulas_adicionales_final = ""


	# c. INSTRUCCIONES CRÍTICAS
	critical_instructions = ("CRITICAL INSTRUCTIONS: The final output MUST BE A PURE IMAGE ONLY. ABSOLUTELY NO TEXT OVERLAYS, NO LOGOS (regardless of brand or style), "
							 "NO WATERMARKS, NO UI CHROME, NO DEBUG ARTIFACTS, NO BOUNDING BOXES, NO ANNOTATIONS, NO GUIDES, AND NO EXTRA FRAMES. Ensure a pristine, clean image output.")

	# 4. ENSAMBLAJE FINAL DEL PROMPT
	# Se sigue la estructura de tu prompt de ejemplo
	mi_prompt = f"""
Generate a image for {brand_name} about {producto} with a {estilo_visual}, {render_calidad}.
{escena_clause_str}
{critical_instructions}
{clausulas_adicionales_final}
"""
	# Se eliminan los saltos de línea y espacios excesivos para mantener la limpieza
	mi_prompt = mi_prompt.strip()

	# --- FIN DE LA LÓGICA DE CONSTRUCCIÓN DEL PROMPT ---
	
	# 5. DEVOLVER EL PROMPT EN LA RESPUESTA JSON
	return jsonify({
		"success": True,
		"promt": mi_prompt 
	})

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


#------------------------
#-------Funciones
#------------------------

def generar_url_firmada(bucket_name, blob_name):
	bucket = storage_client.bucket(bucket_name)
	blob_path = f"generate/blog/{blob_name}"
	blob = bucket.blob(blob_path)
	url = blob.generate_signed_url(
		version="v4",
		expiration=timedelta(minutes=15),
		method="GET",
	)
	#url = blob.generate_signed_url(expiration=3600)
	return url
def listarImages(data_id):
	try:
		query = Imagesia.query.filter_by(imgia_type='blog',imgia_estado=1,proyecto_id=data_id)
		lista = query.all()
		return lista
	except Exception as e:
		return jsonify({"error": str(e)}), 500