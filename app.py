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

# List of NTP servers
ntp_servers = [
    "157.20.66.8",
    "157.20.67.8",
    "14.139.60.103",
    "14.139.60.106",
    "14.139.60.107",
    "time.nplindia.in",
    "time.nplindia.org",
    "samay1.nic.in",
    "samay2.nic.in",
    "time.nist.gov",
    "pool.ntp.org",
    "time.windows.com",
    "time.google.com",
    "asia.pool.ntp.org",
    "uk.pool.ntp.org"
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
            "response_time_ms": f"{response.recv_time - response.sent_time:.3f}",
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
