from flask import Blueprint
from routes.sections.brandkit.logos import bklogos_bp

def register_brandkit_bp(app):
	app.register_blueprint(bklogos_bp)