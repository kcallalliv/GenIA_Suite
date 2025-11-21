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

storage_client = storage.Client()
bq_client = bigquery.Client()
BUCKET_NAME = os.environ.get("BUCKET_NAME", "genia_information")
BQ_TABLE = os.environ.get("BQ_TABLE", "genia_information.upload_logs")

client = bigquery.Client(project="prd-claro-mktg-data-storage")
genai_client = genai.Client(
	vertexai=True,
	project="prd-claro-mktg-data-storage",
	location="us-central1",
	http_options=HttpOptions(api_version="v1")
)

geniasource_bp = Blueprint('geniasource_bp', __name__)
#===Listado===
@geniasource_bp.route('/genia-source')
def geniasource():
	return render_template('/genia-source/index.html')
#===File Upload===
@geniasource_bp.route("/genia-source/upload", methods=["GET", "POST"])
def gsfile_upload():
	if request.method == "GET":
		return render_template("upload.html")

	file = request.files.get("file")
	uploader = request.form.get("uploader")

	if not file or not uploader:
		return "Archivo y nombre requeridos", 400

	ext = file.filename.split('.')[-1]
	fecha = datetime.datetime.utcnow().strftime('%Y%m%d')
	nombre_archivo = f"{fecha}_{uploader}_{uuid.uuid4().hex}.{ext}"

	# Subir a Cloud Storage
	bucket = storage_client.bucket(BUCKET_NAME)
	blob = bucket.blob(nombre_archivo)
	blob.upload_from_file(file)

	# Registrar en BigQuery
	bq_client.insert_rows_json(BQ_TABLE, [{
		"file_name": nombre_archivo,
		"upload_time": datetime.datetime.utcnow().isoformat(),
		"uploader": uploader
	}])

	return f"Archivo {nombre_archivo} subido correctamente"