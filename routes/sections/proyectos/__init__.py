from flask import Blueprint
from .keywords import pkeywords_bp
from .tendencias import ptendencias_bp

def register_proyectos_bp(app):
	app.register_blueprint(pkeywords_bp)
	app.register_blueprint(ptendencias_bp)