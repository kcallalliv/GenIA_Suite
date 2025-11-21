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
from google.api_core.client_options import ClientOptions
from google.cloud import storage
from google.cloud import discoveryengine_v1 as discoveryengine
from google import genai
import datetime
import pandas as pd
import traceback # Asume que pandas está importado
import uuid
import base64
#llamar a config
from routes.models import db, Assets, Configuracion, Proyectos
from routes.config.geniaconfig import bq_client, bucket_name, storage_client, validar_sesion, fechaActual, generarCodigo

colecciones_bp = Blueprint('colecciones_bp', __name__, url_prefix='/brand/<string:brand_id>/proyectos/<string:proyecto_id>/colecciones/')
#===Tendencias===
@colecciones_bp.route('/')
@validar_sesion
def colecciones_colecciones(brand_id,proyecto_id):
	return render_template('sections/colecciones/listado.html',proyecto_id=proyecto_id)
#===Listado Ajax Cards===
@colecciones_bp.route('view-cards', methods=['GET', 'POST'])
@validar_sesion
def colecciones_listarAjax(brand_id,proyecto_id):
	proyecto_id = request.values.get('pid')
	return render_template('sections/colecciones/listado-ajax.html',proyecto_id=proyecto_id)
#===Funciones===
def convierteBase64(text: str) -> str:
	return base64.urlsafe_b64encode(text.encode('utf-8')).decode('ascii')