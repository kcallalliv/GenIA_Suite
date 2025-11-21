from flask import Blueprint
from .logos import bklogos_bp
from .brands import bkbrands_bp
from .files import bkfiles_bp
from .fonts import bkfonts_bp
from .colors import bkcolors_bp
from .images import bkimages_bp
from .info import bkdash_bp, bkinfo_bp
from .links import links_bp
from .proyectos import proyectos_bp
from .tendencias import tendencias_bp
from .colecciones import colecciones_bp
from .integraciones import integraciones_bp

def register_brandkit_bp(app):
	app.register_blueprint(bklogos_bp)
	app.register_blueprint(bkbrands_bp)
	app.register_blueprint(bkfiles_bp)
	app.register_blueprint(bkfonts_bp)
	app.register_blueprint(bkcolors_bp)
	app.register_blueprint(bkimages_bp)
	app.register_blueprint(bkdash_bp)
	app.register_blueprint(bkinfo_bp)
	app.register_blueprint(links_bp)
	app.register_blueprint(proyectos_bp)
	app.register_blueprint(tendencias_bp)
	app.register_blueprint(colecciones_bp)
	app.register_blueprint(integraciones_bp)