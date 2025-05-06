from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    from .routes import produtos, clientes, vendas
    app.register_blueprint(produtos.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(vendas.bp)

    return app
