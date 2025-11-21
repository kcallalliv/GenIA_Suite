from flask import Blueprint
from .logos import blogos_bp
from .files import bfiles_bp
from .fonts import bfonts_bp
from .colors import bcolors_bp
from .images import bimages_bp
from .webscan import bkwebscan_bp

def register_brand_bp(app):
	app.register_blueprint(blogos_bp)
	app.register_blueprint(bfiles_bp)
	app.register_blueprint(bfonts_bp)
	app.register_blueprint(bcolors_bp)
	app.register_blueprint(bkwebscan_bp)
	app.register_blueprint(bimages_bp)