from flask import Flask
import os
def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=None)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app