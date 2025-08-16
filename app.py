from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp, login_manager
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp
from routes.reports import reports_bp
from routes.categories import categories_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(categories_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
