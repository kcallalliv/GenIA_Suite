# routes/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importa los modelos aquí después de definir db
from .models import Assets, Assetsbrand, Links, Brands, Sitemap, Exclusiones, Configuracion, Proyectos, Users
from .models import Tendencias, Colecciones, Keywords, Imagesia

