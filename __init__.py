from flask import Flask
from routes.index.routes import index_bp
from routes.panel.routes import panel_bp
from routes.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Registrar los Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(panel_bp)

    with app.app_context():
        db.create_all()

    return app
