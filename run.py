from app import create_app
from config import DevelopmentConfig, ProductionConfig
from waitress import serve

app = create_app(ProductionConfig)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
