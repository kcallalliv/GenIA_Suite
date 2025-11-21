from flask import Flask, render_template, request, session, redirect, url_for, g
from routes.sections.sistema import register_sistema_bp
from routes.sections.brand import register_brand_bp
from routes.sections.brandkit import register_brandkit_bp
from routes.sections.colecciones import register_colecciones_bp
from routes.sections.geniaauth import geniaauth_bp
from routes.geniatext import geniatext_bp
from routes.geniasource import geniasource_bp
from routes.sections.geniausers import geniausers_bp
from routes.config.geniaconfig import config_postgres
from routes.models import db, Users
import os
import hashlib

app = Flask(__name__)

# Configuración de la aplicación
app.secret_key = config_postgres.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config_postgres.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_postgres.SQLALCHEMY_TRACK_MODIFICATIONS

# Configura las opciones del motor si existen (para el conector de Cloud SQL)
if hasattr(config_postgres, 'SQLALCHEMY_ENGINE_OPTIONS'):
	app.config['SQLALCHEMY_ENGINE_OPTIONS'] = config_postgres.SQLALCHEMY_ENGINE_OPTIONS

db.init_app(app)


"""
@app.context_processor
def inject_request():
	from flask import request # Importa request aquí también para estar seguro
	return dict(query_params=request.args)
"""
@app.context_processor
def inject_globals():
	query_params = request.args
	# 2. Parámetros de Ruta (para brand_id, proyecto_id, etc.)
	# Esto extrae el {'brand_id': 'BRD1...'} de la URL
	url_args = request.view_args
	return dict(
		query_params=query_params,
		url_args=url_args
	)
# -------------------------------------------------

@app.route('/')
def index():
	return render_template('login.html')

app.register_blueprint(geniatext_bp)
app.register_blueprint(geniasource_bp)
app.register_blueprint(geniaauth_bp)
app.register_blueprint(geniausers_bp)
register_brand_bp(app)
register_brandkit_bp(app)
register_colecciones_bp(app)
register_sistema_bp(app)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()

	# Detección del entorno para la ejecución del servidor
	# La variable 'K_SERVICE' solo está presente en Google Cloud Run.
	is_cloud_env = os.getenv("K_SERVICE", None) is not None

	if is_cloud_env:
		# Modo de ejecución para Cloud (Cloud Run, etc.)
		# El puerto es dinámicamente asignado por el entorno.
		port = int(os.environ.get('PORT', 8080))
		app.run(host='0.0.0.0', port=port, debug=False)
		#app.run(host="0.0.0.0", port=8080, debug=True)
	else:
		# Modo de ejecución para desarrollo local
		# Usas el puerto por defecto de Flask.
		app.run(debug=True)