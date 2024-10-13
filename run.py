import os
from waitress import serve
from app import create_app
from config import ProductionConfig


# Create the app instance with the desired configuration
app = create_app(ProductionConfig)

if __name__ == '__main__':
    # Fetch host, port, debug mode, and threads from environment variables (with defaults)
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8080))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    threads = int(os.getenv('THREADS', 2))  # Set number of threads, default to 2

    if debug_mode:
        # Run the app in debug mode for development purposes
        app.run(host=host, port=port, debug=True)
    else:
        # Use Waitress to serve the application with the specified number of threads
        serve(app, host=host, port=port, threads=threads)
