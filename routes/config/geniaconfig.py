import os
import pytz
import datetime
import base64
import time
import uuid
from flask import Blueprint, render_template, request, session, redirect, url_for, send_file, jsonify
from functools import wraps
from google.cloud import storage, bigquery
from google import genai
from google.genai.types import HttpOptions
from google.cloud.sql.connector import Connector, IPTypes

# La ruta del archivo JSON de la clave de servicio en tu sistema
routes_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(routes_dir))
ruta_credenciales = os.path.join(project_root, 'token', 'prd-claro-mktg-data-storage-2560da7d818c.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ruta_credenciales

# Inicializar clientes de Google Cloud
storage_client = storage.Client()
bq_client = bigquery.Client(project="prd-claro-mktg-data-storage")

# Configuración del proyecto y tablas
# Asegúrate de que las variables de entorno estén definidas o usa valores por defecto
bucket_name = os.environ.get("bucket_name", "genia_information")
bq_table_assets = os.environ.get("bq_table_assets", "genia_information.assets")
BQ_TABLE_USERS = os.environ.get("BQ_TABLE_USERS", "genia_information.users")
bq_table_brands = os.environ.get("bq_table_brands", "genia_information.brands")
bq_table_config = os.environ.get("bq_table_config", "genia_information.config")
bq_table_seo_semrush = os.environ.get("bq_table_seo_semrush", "project_semantic_seo.semrush_mayo_master")
bq_table_seo_search = os.environ.get("bq_table_seo_semrush", "searchconsole.searchdata_url_impression")
PROJECT_ID = "prd-claro-mktg-data-storage"

# El cliente de BigQuery se puede inicializar con el proyecto aquí
client = bigquery.Client(project=PROJECT_ID)

# Asumiendo un cliente para Gemini API, si la librería es diferente, ajusta la importación
genai_client = genai.Client(
	vertexai=True,
	project="prd-claro-mktg-data-storage",
	location="us-central1",
	http_options=HttpOptions(api_version="v1")
)

print("Configuración y clientes de Google Cloud inicializados.")
"""
class config_postgres:
	# La información de conexión se lee de variables de entorno para mayor seguridad.
	# Si no se encuentran, se usa un valor por defecto (útil para desarrollo local).
	
	DB_USER = os.environ.get('DB_USER', 'postgres')
	DB_PASS = os.environ.get('DB_PASS', 'Genia_suite2025')
	DB_HOST = os.environ.get('DB_HOST', '34.27.28.147')
	DB_PORT = os.environ.get('DB_PORT', '5432')
	DB_NAME = os.environ.get('DB_NAME', 'postgres')

	# La URL de la base de datos se construye con las variables de entorno.
	# El valor por defecto apunta a una configuración local para desarrollo.
	SQLALCHEMY_DATABASE_URI = (
		f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
		if os.environ.get('DATABASE_URL') is None
		else os.environ.get('DATABASE_URL')
	)

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY', 'csa')
"""
class config_postgres:
	SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure")
	#SECRET_KEY = os.getenv("SECRET_KEY", "csa")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	IS_CLOUD_ENV = os.getenv("K_SERVICE", None) is not None

	if IS_CLOUD_ENV:
		SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
		_connector = None

		@staticmethod
		def _getconn():
			icn = os.getenv("INSTANCE_CONNECTION_NAME")
			user = os.getenv("DB_USER")
			pwd = os.getenv("DB_PASS")
			db = os.getenv("DB_NAME")
			
			missing = [k for k, v in [("INSTANCE_CONNECTION_NAME", icn), ("DB_USER", user), ("DB_PASS", pwd), ("DB_NAME", db)] if not v]
			if missing:
				raise RuntimeError(f"Faltan variables de entorno para Cloud SQL: {', '.join(missing)}")
			
			if config_postgres._connector is None:
				config_postgres._connector = Connector(ip_type=IPTypes.PUBLIC)

			return config_postgres._connector.connect(
				icn,
				"pg8000",
				user=user,
				password=pwd,
				db=db
			)

		SQLALCHEMY_ENGINE_OPTIONS = {
			"creator": _getconn.__func__,
			"pool_pre_ping": True,
		}
	else:
		#DB_PASS = os.environ.get('DB_PASS', 'Genia_suite2025')
		#DB_HOST = os.environ.get('DB_HOST', '34.27.28.147')
		DB_USER = os.environ.get('DB_USER', 'postgres')
		DB_PASS = os.environ.get('DB_PASS', 'postgres')
		DB_HOST = os.environ.get('DB_HOST', 'localhost')
		DB_PORT = os.environ.get('DB_PORT', '5432')
		DB_NAME = os.environ.get('DB_NAME', 'postgres')

		SQLALCHEMY_DATABASE_URI = (
			f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
		)

def validar_sesion(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'permiso' not in session:
			return redirect('/')
		return f(*args, **kwargs)
	return decorated_function

def fechaActual():
	tz_pe = pytz.timezone('America/Lima')
	my_fecha = datetime.datetime.now(tz=tz_pe)
	return my_fecha.strftime('%Y-%m-%d %H:%M:%S')
	
def generarCodigo(prefijo="P"):
	uuid_bytes = uuid.uuid4().bytes
	datos_base = uuid_bytes[:8]
	codigo_codificado_bytes = base64.urlsafe_b64encode(datos_base)
	codigo_final = codigo_codificado_bytes.decode('ascii').rstrip('=')
	return f"{prefijo}{codigo_final[:7]}"