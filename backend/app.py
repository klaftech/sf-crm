from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import blueprints
from app.routes.tasks import task_bp
from app.routes.kpis import kpi_bp
from app.routes.targets import target_bp
from app.routes.erp import erp_bp

# Load environment variables
load_dotenv()


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    
    # CORS configuration
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # Register blueprints
    app.register_blueprint(task_bp)
    app.register_blueprint(kpi_bp)
    app.register_blueprint(target_bp)
    app.register_blueprint(erp_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'CRM API is running'}, 200
    
    @app.route('/')
    def index():
        return {
            'name': 'CRM API',
            'version': '1.0.0',
            'endpoints': {
                'tasks': '/api/tasks',
                'kpis': '/api/kpis',
                'targets': '/api/targets',
                'erp_customers': '/api/erp/customers',
                'erp_sales': '/api/erp/sales'
            }
        }, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    
    # Never enable debug mode in production
    is_development = os.getenv('FLASK_ENV', 'production') == 'development'
    debug = is_development and os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    if debug:
        print("WARNING: Running in debug mode. This should NEVER be used in production!")
    
    app.run(host=host, port=port, debug=debug)
