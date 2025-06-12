from .seo_routes import seo_bp

def register_routes(app):
    app.register_blueprint(seo_bp, url_prefix="/api")