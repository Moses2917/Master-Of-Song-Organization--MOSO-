from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Port to serve the maintenance page
PORT = 5000

# The handler will look for maintenance.html in the current directory
class MaintenanceHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Always serve the maintenance page regardless of the request path
        self.path = "./templates/maintenance.html"
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    # Check if the maintenance.html file exists
    if not os.path.exists("C:/Users/Armne/OneDrive/Documents/Code/Python/templates/maintenance.html"):
        print("Error: maintenance.html file not found in the current directory")
        exit(1)
    
    # Create server
    server = HTTPServer(('', PORT), MaintenanceHandler)
    
    print(f"Serving maintenance page at http://0.0.0.0:{PORT}")
    
    try:
        # Start server
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
