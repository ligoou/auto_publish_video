from flask import Flask
import logging.config

def create_app() -> Flask:
    """Create and configure the Flask application."""
    logging.config.fileConfig('src/logging.conf')
    app = Flask(__name__)

    @app.route('/')
    def hello_world() -> str:
        """Return a simple test message."""
        return 'test'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
