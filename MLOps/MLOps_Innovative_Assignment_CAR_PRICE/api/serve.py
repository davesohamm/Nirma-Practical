"""
Waitress WSGI Server Entry Point for Flask Application
Usage: python -m api.serve
Nginx should reverse-proxy to the port configured here (default: 8000).
"""

from waitress import serve
from api.main import app

if __name__ == "__main__":
    print("=" * 60)
    print("  Starting Waitress WSGI Server")
    print("  Serving Flask app on http://127.0.0.1:8000")
    print("  Configure Nginx to reverse-proxy to this address")
    print("=" * 60)
    serve(app, host="127.0.0.1", port=8000, threads=4)
