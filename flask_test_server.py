#!/usr/bin/env python3
"""
Flask Server with Tor Hidden Service Support
Serves Flask app on both clearnet (localhost) and Tor (.onion address)
"""

import sys
import time
import logging
import threading
from dtor import TorHandler
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variables
tor_handler = None
onion_address = None
flask_port = 5000
tor_initialized = False
initialization_error = None

# HTML template for home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask + Tor Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #7d4698;
            padding-bottom: 10px;
        }
        .status {
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }
        .error {
            background: #ffebee;
            border-left-color: #f44336;
        }
        .info-box {
            background: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: monospace;
        }
        .label {
            font-weight: bold;
            color: #7d4698;
        }
        .onion {
            color: #7d4698;
            font-weight: bold;
            word-break: break-all;
        }
        .endpoints {
            margin-top: 30px;
        }
        .endpoint {
            background: #e3f2fd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
        }
        code {
            background: #333;
            color: #0f0;
            padding: 2px 6px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧅 Flask + Tor Server</h1>
        {% if tor_status == 'running' %}
        <div class="status">
            <strong>✓ Server Status:</strong> Running on both clearnet and Tor
        </div>
        {% elif tor_status == 'initializing' %}
        <div class="status">
            <strong>⏳ Server Status:</strong> Tor is initializing...
        </div>
        {% else %}
        <div class="status error">
            <strong>✗ Server Status:</strong> Tor initialization failed
            <br><small>{{ error_message }}</small>
        </div>
        {% endif %}
        <div class="info-box">
            <div><span class="label">Clearnet URL:</span> http://127.0.0.1:{{ port }}/</div>
            {% if onion_address %}
            <div><span class="label">Onion Address:</span> <span class="onion">http://{{ onion_address }}/</span></div>
            {% else %}
            <div><span class="label">Onion Address:</span> <em>Initializing...</em></div>
            {% endif %}
        </div>
        <div class="endpoints">
            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <strong>GET /</strong> - This page
            </div>
            <div class="endpoint">
                <strong>GET /status</strong> - JSON status information
            </div>
            <div class="endpoint">
                <strong>GET /api/echo?message=hello</strong> - Echo test
            </div>
            <div class="endpoint">
                <strong>POST /api/data</strong> - Accept JSON data
                <br><small>Example: <code>curl -X POST http://127.0.0.1:{{ port }}/api/data -H "Content-Type: application/json" -d '{"test":"data"}'</code></small>
            </div>
            <div class="endpoint">
                <strong>GET /api/time</strong> - Get current server time
            </div>
        </div>
        <div style="margin-top: 30px; color: #666; font-size: 0.9em;">
            <strong>Note:</strong> To access the .onion address, you need Tor Browser or configure your application to use Tor SOCKS proxy.
        </div>
    </div>
</body>
</html>
"""

def initialize_tor():
    """Initialize Tor handler and start service"""
    global tor_handler, onion_address, tor_initialized, initialization_error
    
    try:
        logger.info("="*80)
        logger.info("INITIALIZING TOR HANDLER")
        logger.info("="*80)
        
        # Create TorHandler instance
        logger.info("Creating TorHandler instance...")
        tor_handler = TorHandler(recover=True)  # Enable recovery to restore previous services
        tor_handler.debug = True
        
        # Create required directories
        logger.info("Creating required directories...")
        if not tor_handler.create_required_directories():
            raise Exception("Failed to create required directories")
        
        # Check if Tor binaries exist
        logger.info("Checking for Tor binaries...")
        if not tor_handler.check_tor_binaries_exist():
            logger.info("Tor binaries not found, downloading...")
            
            # Fetch latest Tor download information
            tor_info = tor_handler.fetch_latest_tor_download_url()
            if not tor_info or not tor_info.get('url'):
                raise Exception("Failed to fetch Tor download information")
            
            logger.info(f"Found Tor version {tor_info['version']}")
            logger.info(f"Downloading from: {tor_info['url']}")
            
            # Download and install Tor binaries
            if not tor_handler.download_and_install_tor_binaries():
                raise Exception("Failed to download and install Tor binaries")
            
            logger.info("✓ Tor binaries downloaded and installed successfully")
        else:
            logger.info("✓ Tor binaries already exist")
        
        # Configure ports with collision resolution
        logger.info("Configuring ports...")
        tor_handler.socks_port_collision_resolve = True
        tor_handler.control_port_collision_resolve = True
        
        if not tor_handler.socks_port:
            tor_handler.add_socks_port(9050)
        if not tor_handler.control_port:
            tor_handler.add_control_port(9051)
        
        logger.info(f"✓ Ports configured - SOCKS: {tor_handler.socks_port}, Control: {tor_handler.control_port}")
        
        # Check if Flask hidden service already exists in configuration
        flask_service_exists = False
        existing_onion = None
        
        logger.info("Checking for existing Flask hidden service...")
        if tor_handler.torrc_file.exists():
            # Load configuration to check for existing services
            tor_handler.load_torrc_configuration()
            
            # Look for service on port 80 targeting flask_port
            for service in tor_handler.hidden_services:
                if service.get('port') == 80 and service.get('target_port') == flask_port:
                    flask_service_exists = True
                    existing_onion = service.get('host')
                    if existing_onion:
                        logger.info(f"✓ Found existing hidden service: {existing_onion}")
                    break
        
        # Register persistent hidden service ONLY if it doesn't exist
        if not flask_service_exists:
            logger.info(f"Registering NEW persistent hidden service for Flask (port {flask_port})...")
            if not tor_handler.register_hidden_service(
                port=80,
                target_port=flask_port,
                pre_config=False
            ):
                raise Exception("Failed to register persistent hidden service")
            logger.info("✓ Persistent hidden service registered")
            
            # Save immediately after registering
            if not tor_handler.save_torrc_configuration():
                raise Exception("Failed to save torrc configuration after registration")
        else:
            logger.info("✓ Using existing persistent hidden service")
            # No need to save - configuration already loaded
        
        # Start Tor service
        logger.info("Starting Tor service...")
        if not tor_handler.start_tor_service():
            raise Exception("Failed to start Tor service")
        
        logger.info(f"✓ Tor service started successfully (PID: {tor_handler.tor_process_id})")
        
        # Wait for Tor to generate the hidden service
        logger.info("Waiting for hidden service generation...")
        time.sleep(3)
        
        # Refresh hidden services to get the onion address
        tor_handler.refresh_all_hidden_services()
        
        # Find our Flask service and get the onion address
        for service in tor_handler.hidden_services:
            if service.get('port') == 80 and service.get('target_port') == flask_port:
                onion_address = service.get('host', '')
                break
        
        if not onion_address:
            raise Exception("Failed to retrieve onion address")
        
        logger.info("="*80)
        logger.info("✓ TOR INITIALIZATION COMPLETE")
        logger.info("="*80)
        logger.info(f"Onion Address: {onion_address}")
        logger.info(f"Clearnet URL: http://127.0.0.1:{flask_port}/")
        logger.info("="*80)
        
        tor_initialized = True
        
    except Exception as e:
        initialization_error = str(e)
        logger.error("="*80)
        logger.error("✗ TOR INITIALIZATION FAILED")
        logger.error("="*80)
        logger.error(f"Error: {e}")
        logger.error("="*80)
        
        if tor_handler and tor_handler.debug:
            import traceback
            traceback.print_exc()

# Flask Routes

@app.route('/')
def home():
    """Home page with server information"""
    tor_status = 'running' if tor_initialized else ('initializing' if initialization_error is None else 'failed')
    
    return render_template_string(
        HOME_TEMPLATE,
        tor_status=tor_status,
        onion_address=onion_address,
        port=flask_port,
        error_message=initialization_error
    )

@app.route('/status')
def status():
    """JSON status endpoint"""
    return jsonify({
        "status": "running" if tor_initialized else "initializing",
        "tor_initialized": tor_initialized,
        "onion_address": onion_address,
        "clearnet_url": f"http://127.0.0.1:{flask_port}/",
        "flask_port": flask_port,
        "tor_running": tor_handler.running if tor_handler else False,
        "tor_pid": tor_handler.tor_process_id if tor_handler else None,
        "socks_ports": tor_handler.socks_port if tor_handler else [],
        "control_ports": tor_handler.control_port if tor_handler else [],
        "hidden_services_count": len(tor_handler.hidden_services) if tor_handler else 0,
        "runtime_services_count": len(tor_handler.temp_config['hidden_services']) if tor_handler else 0,
        "initialization_error": initialization_error
    })

@app.route('/api/echo')
def echo():
    """Echo endpoint - returns the message parameter"""
    message = request.args.get('message', 'No message provided')
    
    # Check if request came through Tor
    # When accessing via .onion, the Host header will contain .onion
    via_tor = (
        '.onion' in request.headers.get('Host', '') or
        request.headers.get('X-Forwarded-For') is not None or
        request.headers.get('X-Tor', '') == '1'
    )
    
    return jsonify({
        "echo": message,
        "timestamp": datetime.now().isoformat(),
        "via_tor": via_tor,
        "host_header": request.headers.get('Host', 'unknown'),
        "user_agent": request.headers.get('User-Agent', 'unknown')
    })

@app.route('/api/data', methods=['POST'])
def api_data():
    """Accept and echo JSON data"""
    data = request.get_json()
    
    # Check if request came through Tor
    via_tor = (
        '.onion' in request.headers.get('Host', '') or
        request.headers.get('X-Forwarded-For') is not None or
        request.headers.get('X-Tor', '') == '1'
    )
    
    return jsonify({
        "received": data,
        "timestamp": datetime.now().isoformat(),
        "content_type": request.content_type,
        "via_tor": via_tor,
        "host_header": request.headers.get('Host', 'unknown')
    })

@app.route('/api/time')
def api_time():
    """Return current server time"""
    # Check if request came through Tor
    via_tor = (
        '.onion' in request.headers.get('Host', '') or
        request.headers.get('X-Forwarded-For') is not None or
        request.headers.get('X-Tor', '') == '1'
    )
    
    return jsonify({
        "server_time": datetime.now().isoformat(),
        "unix_timestamp": int(time.time()),
        "via_tor": via_tor,
        "access_method": "tor_hidden_service" if via_tor else "clearnet"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    is_healthy = tor_initialized and (tor_handler.running if tor_handler else False)
    status_code = 200 if is_healthy else 503
    
    return jsonify({
        "healthy": is_healthy,
        "tor_running": tor_handler.running if tor_handler else False,
        "onion_available": onion_address is not None
    }), status_code

def shutdown_handler():
    """Cleanup on shutdown - gracefully stop only our Tor instance"""
    global tor_handler
    
    if tor_handler and tor_handler.running:
        logger.info("Shutting down Tor service gracefully...")
        try:
            # Only stop gracefully - don't force kill
            # This will only affect processes started with our config
            tor_handler.stop_tor_service()
            logger.info("✓ Tor service stopped")
        except Exception as e:
            logger.error(f"Error stopping Tor: {e}")
            # Even on error, don't force-kill as it might affect Tor Browser

def main():
    """Main entry point"""
    logger.info("\n" + "="*80)
    logger.info("FLASK + TOR SERVER")
    logger.info("="*80)
    logger.info(f"Flask Port: {flask_port}")
    logger.info("Initializing Tor in background thread...")
    logger.info("="*80 + "\n")
    
    # Start Tor initialization in background thread
    tor_thread = threading.Thread(target=initialize_tor, daemon=True)
    tor_thread.start()
    
    # Register cleanup handler
    import atexit
    atexit.register(shutdown_handler)
    
    try:
        # Start Flask server
        logger.info(f"Starting Flask server on http://127.0.0.1:{flask_port}/")
        logger.info("Note: Tor initialization will continue in the background")
        logger.info("Check http://127.0.0.1:{}/status for current status\n".format(flask_port))
        
        app.run(
            host='0.0.0.0',
            port=flask_port,
            debug=False,  # Disable debug mode in production
            use_reloader=False  # Disable reloader to avoid duplicate Tor instances
        )
    except KeyboardInterrupt:
        logger.info("\n\nReceived interrupt signal")
    except Exception as e:
        logger.error(f"Flask server error: {e}")
        sys.exit(1)
    finally:
        shutdown_handler()

if __name__ == '__main__':
    main()
