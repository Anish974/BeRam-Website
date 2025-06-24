#!/usr/bin/env python3
"""
Simple HTTP server for viewing the BeRAM static website on any device.
This script starts a local web server that can be accessed from any device on the same network.
"""

import os
import sys
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse
import socket

# Configuration
PORT = 8000
STATIC_SITE_DIR = "beram_static_site"  # Directory containing the static site

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"  # Fallback to localhost

def main():
    """Start the HTTP server"""
    # Check if the static site directory exists
    if not os.path.exists(STATIC_SITE_DIR):
        print(f"Error: Static site directory '{STATIC_SITE_DIR}' not found.")
        print("Please run the static site generator first.")
        sys.exit(1)
    
    # Change to the static site directory
    os.chdir(STATIC_SITE_DIR)
    
    # Get the local IP address
    local_ip = get_local_ip()
    
    # Create the server
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    # Print access information
    print(f"\nBeRAM Static Website Server")
    print(f"===========================")
    print(f"\nServer started at:")
    print(f"- Local access: http://localhost:{PORT}")
    print(f"- Network access: http://{local_ip}:{PORT}")
    print(f"\nTo view the website on other devices (phones, tablets, etc.):")
    print(f"1. Make sure the device is connected to the same network")
    print(f"2. Open a browser and navigate to: http://{local_ip}:{PORT}")
    print(f"\nPress Ctrl+C to stop the server.\n")
    
    # Open the browser automatically
    webbrowser.open(f"http://localhost:{PORT}")
    
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    main()
