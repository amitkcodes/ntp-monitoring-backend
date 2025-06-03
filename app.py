import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import ntplib
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for requests from your GitHub Pages domain
CORS(app, resources={r"/api/*": {"origins": "https://amitkcodes.github.io/ntp-monitoring"}})

# List of NTP servers (updated with reliable servers)
ntp_servers = [
    "pool.ntp.org",
    "time.google.com",
    "time.windows.com",
    "time.nist.gov",
    "asia.pool.ntp.org",
    "europe.pool.ntp.org",
    "north-america.pool.ntp.org"
]

# Function to query an NTP server
def query_ntp_server(server):
    try:
        client = ntplib.NTPClient()
        response = client.request(server)
        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(ist).isoformat()
        
        return {
            "server": server,
            "status": "Online",
            "offset_ms": f"{response.offset * 1000:.3f}",
            "delay_ms": f"{response.delay * 1000:.3f}",
            "root_delay_ms": f"{response.root_delay * 1000:.3f}",
            "root_dispersion_ms": f"{response.root_dispersion * 1000:.3f}",
            "response_time_ms": f"{(response.dest_time - response.orig_time) * 1000:.3f}",
            "precision_ms": f"{response.precision:.3f}",
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"Error querying {server}: {e}")
        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(ist).isoformat()
        return {
            "server": server,
            "status": "Error",
            "offset_ms": "0.000",
            "delay_ms": "0.000",
            "root_delay_ms": "0.000",
            "root_dispersion_ms": "0.000",
            "response_time_ms": "0.000",
            "precision_ms": "0.000",
            "timestamp": timestamp
        }

# Add a root route for health checks
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the NTP Monitoring Backend! Use /api/realtime or /api/history to access data."}), 200

# API endpoint for real-time data
@app.route('/api/realtime', methods=['GET'])
def get_realtime_data():
    data = [query_ntp_server(server) for server in ntp_servers]
    return jsonify(data)

# API endpoint for historical data (placeholder)
@app.route('/api/history', methods=['GET'])
def get_historical_data():
    # Placeholder: In a real app, you'd query this from a database
    server = request.args.get('server')
    if not server:
        return jsonify({"error": "Server parameter is required"}), 400
    # Mock historical data for now
    ist = pytz.timezone('Asia/Kolkata')
    historical_data = [
        {
            "server": server,
            "status": "Online",
            "offset_ms": "1.234",
            "delay_ms": "20.567",
            "root_delay_ms": "5.678",
            "root_dispersion_ms": "3.456",
            "response_time_ms": "15.789",
            "precision_ms": "0.001",
            "timestamp": datetime.now(ist).isoformat()
        }
    ]
    return jsonify(historical_data)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)