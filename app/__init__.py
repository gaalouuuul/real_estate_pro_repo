from flask import Flask, jsonify
from flasgger import Swagger
from app.extensions import db
from app.utils.errors import ApiError

from app.routes.auth_routes     import bp as auth_bp
from app.routes.user_routes     import bp as user_bp
from app.routes.property_routes import bp as property_bp
from app.routes.favorite_routes import bp as favorite_bp
from app.routes.visit_routes    import bp as visit_bp
from app.routes.admin_routes    import bp as admin_bp


def create_app():
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────
    app.config["SECRET_KEY"]                  = "change_me_in_production"
    app.config["SQLALCHEMY_DATABASE_URI"]     = "sqlite:///realestate.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Swagger ────────────────────────────────────────────────
    app.config["SWAGGER"] = {
        "title":     "Real Estate Microservice API",
        "uiversion": 3,
    }
    Swagger(app)

    # ── Extensions ─────────────────────────────────────────────
    db.init_app(app)

    # ── Blueprints ─────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(visit_bp)
    app.register_blueprint(admin_bp)

    # ── Gestionnaire d'erreurs global ──────────────────────────
    @app.errorhandler(ApiError)
    def handle_api_error(e):
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"error": "internal server error"}), 500

    # ── Création des tables ────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app