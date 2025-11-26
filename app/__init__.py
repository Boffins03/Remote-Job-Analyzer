from flask import Flask
from app.db import SessionLocal
from app.models import Base
from sqlalchemy.orm import scoped_session

def create_app():
    app = Flask(__name__)

    # Database session per request
    app.session = scoped_session(SessionLocal)

    # Register blueprints
    from app.routes.jobs import jobs_bp
    from app.routes.companies import companies_bp
    from app.routes.stats import stats_bp

    app.register_blueprint(jobs_bp, url_prefix="/api")
    app.register_blueprint(companies_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    # Register frontend dashboard
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app
