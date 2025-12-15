# routes/models/models.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from . import db

class Brands(db.Model):
	__tablename__ = 'brands'
	brand_id = db.Column(db.String(255), primary_key=True)
	brand_name = db.Column(db.String(255), nullable=False)
	brand_pais = db.Column(db.String(255), nullable=False)
	brand_subindustria = db.Column(db.String(255), nullable=False)
	brand_description = db.Column(db.Text, nullable=False)
	brand_estado = db.Column(db.Integer, nullable=True)

class Links(db.Model):
	__tablename__ = 'links'
	link_id = db.Column(db.Integer, primary_key=True)
	link_name = db.Column(db.String(255), nullable=False)
	link_url = db.Column(db.String(255), nullable=False)
	link_estado = db.Column(db.Integer, nullable=True)
	link_json = db.Column(db.Text, nullable=False)
	link_tipo = db.Column(db.String(255), nullable=False)
	proyecto_id = db.Column(db.String(255), primary_key=False)

class Configuracion(db.Model):
	__tablename__ = 'config'
	conf_id = db.Column(db.Integer, primary_key=True)
	conf_name = db.Column(db.String(255), nullable=False)
	conf_value = db.Column(db.String(255), nullable=False)
	conf_symbol = db.Column(db.String(255), nullable=False)
	conf_type = db.Column(db.String(255), nullable=False)
	conf_estado = db.Column(db.Integer, nullable=True)

class Assets(db.Model):
	__tablename__ = 'assets'
	asset_id = db.Column(db.Integer, primary_key=True)
	asset_name = db.Column(db.String(255), nullable=False)
	asset_src = db.Column(db.String(255), nullable=False)
	asset_value = db.Column(db.String(255), nullable=False)
	asset_type = db.Column(db.String(255), nullable=False)
	asset_ext = db.Column(db.String(255), nullable=False)
	asset_fecha = db.Column(db.DateTime, nullable=False)
	asset_tags = db.Column(db.Text, nullable=False)
	asset_estado = db.Column(db.Integer, nullable=True)
	proyecto_id = db.Column(db.String(255), nullable=False)

class Assetsbrand(db.Model):
	__tablename__ = 'assetsbrand'
	asset_id = db.Column(db.String(255), primary_key=True)
	asset_name = db.Column(db.String(255), nullable=False)
	asset_src = db.Column(db.String(255), nullable=False)
	asset_value = db.Column(db.String(255), nullable=False)
	asset_type = db.Column(db.String(255), nullable=False)
	asset_ext = db.Column(db.String(255), nullable=False)
	asset_tags = db.Column(db.Text, nullable=False)
	asset_fecha = db.Column(db.DateTime, nullable=False)
	asset_estado = db.Column(db.Integer, nullable=True)
	brand_id = db.Column(db.String(255), nullable=False)

class Sitemap(db.Model):
	__tablename__ = 'sitemap'
	site_id = db.Column(db.Integer, primary_key=True)
	site_name = db.Column(db.String(255), nullable=False)
	site_url = db.Column(db.String(255), nullable=False)
	site_fecha = db.Column(db.DateTime, nullable=False)
	site_estado = db.Column(db.Integer, nullable=True)

class Exclusiones(db.Model):
	__tablename__ = 'exclusiones'
	exsite_id = db.Column(db.Integer, primary_key=True)
	exsite_url = db.Column(db.String(255), unique=True, nullable=False)
	#exsite_url = db.Column(db.String(255), nullable=False)
	exsite_fecha = db.Column(db.DateTime, nullable=False)
	exsite_estado = db.Column(db.Integer, nullable=True)

class Users(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(255), nullable=False)
	user_phone = db.Column(db.String(255), nullable=False)
	user_email = db.Column(db.String(255), nullable=False)
	user_pass = db.Column(db.String(255), nullable=False)
	user_permiso = db.Column(db.String(255), nullable=False)
	user_estado = db.Column(db.Integer, nullable=True)

class Proyectos(db.Model):
	__tablename__ = 'proyectos'
	proyecto_id = db.Column(db.String(255), primary_key=True)
	proyecto_name = db.Column(db.String(255), nullable=False)
	proyecto_integraciones = db.Column(db.Text, nullable=False)
	proyecto_description = db.Column(db.String(255), nullable=False)
	proyecto_estado = db.Column(db.Integer, nullable=True)
	brand_id = db.Column(db.String(255), nullable=False)

class Tendencias(db.Model):
	__tablename__ = 'tendencias'
	tendencia_id = db.Column(db.String(255), primary_key=True)
	tendencia_name = db.Column(db.String(255), nullable=False)
	tendencia_estado = db.Column(db.Integer, nullable=True)
	tendencia_metrica_name = db.Column(db.String(255), nullable=False)
	tendencia_metrica_value = db.Column(db.Integer, nullable=True)
	tendencia_indicador_name = db.Column(db.String(255), nullable=False)
	tendencia_indicadot_value = db.Column(db.Integer, nullable=True)
	tendencia_fuente = db.Column(db.String(255), nullable=False)
	proyecto_id = db.Column(db.String(255), nullable=False)

class Keywords(db.Model):
	__tablename__ = 'keywords'
	keyword_id = db.Column(db.String(255), primary_key=True)
	keyword_name = db.Column(db.String(255), nullable=False)
	keyword_metrica_name = db.Column(db.String(255), nullable=False)
	keyword_metrica_value = db.Column(db.Integer, nullable=True)
	keyword_indicador_name = db.Column(db.String(255), nullable=False)
	keyword_indicador_value = db.Column(db.Integer, nullable=True)
	keyword_fuente = db.Column(db.String(255), nullable=False)
	keyword_estado = db.Column(db.Integer, nullable=True)
	proyecto_id = db.Column(db.String(255), nullable=False)

class Colecciones(db.Model):
	__tablename__ = 'colecciones'
	coleccion_id = db.Column(db.String(255), primary_key=True)
	coleccion_type = db.Column(db.String(255), nullable=False)
	coleccion_category = db.Column(db.String(255), nullable=False)
	coleccion_estado = db.Column(db.Integer, nullable=True)
	tendencia_id = db.Column(db.String(255), nullable=False)

class Imagesia(db.Model):
	__tablename__ = 'imagesia'
	imgia_id = db.Column(db.String(255), primary_key=True)
	imgia_promt = db.Column(db.Text, nullable=False)
	imgia_name = db.Column(db.String(255), nullable=False)
	imgia_type = db.Column(db.String(255), nullable=False)
	imgia_fecha = db.Column(db.DateTime, nullable=False)
	imgia_estado = db.Column(db.Integer, nullable=False)
	proyecto_id = db.Column(db.String(255), nullable=False)