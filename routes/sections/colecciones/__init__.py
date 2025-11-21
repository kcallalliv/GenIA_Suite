from flask import Blueprint
from .article import cltarticle_bp
from .ia_articulo import ia_articulo_bp
from .ia_test import ia_test_bp

def register_colecciones_bp(app):
	app.register_blueprint(cltarticle_bp)
	app.register_blueprint(ia_articulo_bp)
	app.register_blueprint(ia_test_bp)