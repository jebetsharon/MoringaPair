import os
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv

from backend.models import db, migrate, jwt
from backend.config import DevelopmentConfig, ProductionConfig, TestConfig

# Load environment variables
load_dotenv()

# Initialize Mail outside app context
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load the appropriate config
    env = os.getenv('FLASK_ENV', 'development').lower()

    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'test':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # ✅ Enable CORS for frontend (React app on Vite dev server)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}}, supports_credentials=True)

    # ✅ Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # ✅ Register all routes
    from backend.routes import register_routes
    register_routes(app)

    return app

# Create the app instance
app = create_app()

# ✅ Run the app if executed directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
