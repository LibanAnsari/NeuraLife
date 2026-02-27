"""Simple HTTP server for Admin Portal"""
import http.server
import socketserver
import os

PORT = 9000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🛡️  NeuraLife Admin Portal 🛡️                  ║
║                                                           ║
║  Admin portal is now running!                            ║
║                                                           ║
║  📍 URL: http://localhost:{PORT}                           ║
║                                                           ║
║  🔐 Login Credentials:                                   ║
║     Username: admin1                                     ║
║     Password: 123456                                     ║
║                                                           ║
║  Press Ctrl+C to stop the server                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Admin portal stopped.")
