from flask import Blueprint
from .usuarios import usuarios_bp

def register_sistema_bp(app):
	app.register_blueprint(usuarios_bp)