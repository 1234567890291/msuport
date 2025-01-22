import os
import platform
import subprocess
import sys
import hashlib
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Function to check if libraries are installed and install them if needed
def check_and_install_libraries():
    required_libraries = [
        "pyudev", "psutil", "pyusb", "libusb1", "fusepy", "scalpel", "pyexiv2",
        "python-magic", "pytz", "datetime", "pycrypto", "cryptography", "pywinusb",
        "syslog", "win32evtlog", "reportlab", "xlsxwriter", "pandas"
    ]
    
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"Library '{lib}' is not installed. Installing...")
            try:
                if platform.system() == "Windows":
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                elif platform.system() == "Darwin":  # For macOS
                    subprocess.check_call(["pip3", "install", lib])
                else:  # For Linux
                    subprocess.check_call(["sudo", "pip3", "install", lib])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {lib}: {str(e)}")

check_and_install_libraries()

# Flask route to handle home page
@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>USB Forensics</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h1 { color: #333; }
            input[type="file"], button { margin: 10px 0; }
            table { width: 100%; margin-top: 20px; border-collapse: collapse; }
            table, th, td { border: 1px solid black; padding: 10px; text-align: left; }
        </style>
    </head>
    <body>
        <h1>USB Forensics Tool</h1>

        <h2>Detect USB Devices</h2>
        <button id="detect-usb">Detect USB Devices</button>
        <ul id="usb-list"></ul>

        <h2>Check File Integrity</h2>
        <form id="integrity-form">
            <input type="file" id="integrity-file" name="file_path" required>
            <button type="submit">Check Integrity</button>
        </form>
        <div id="integrity-result"></div>

        <script>
            // Detect USB Devices
            $('#detect-usb').click(function() {
                $.get('/detect_usb', function(data) {
                    $('#usb-list').empty();
                    data.forEach(function(device) {
                        $('#usb-list').append('<li>' + device + '</li>');
                    });
                });
            });

            // Check File Integrity
            $('#integrity-form').submit(function(e) {
                e.preventDefault();
                var formData = new FormData(this);
                $.ajax({
                    url: '/check_integrity',
                    type: 'POST',
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data) {
                        if (data.sha256) {
                            $('#integrity-result').html('<strong>SHA-256:</strong> ' + data.sha256);
                        } else {
                            $('#integrity-result').html('<strong>Error:</strong> ' + data.error);
                        }
                    }
                });
            });
        </script>
    </body>
    </html>
    ''')

# Flask route for USB device detection
@app.route('/detect_usb', methods=['GET'])
def detect_usb_devices():
    usb_devices = []
    if platform.system() == "Linux":
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb'):
            usb_devices.append(str(device))
    elif platform.system() == "Windows":
        import psutil
        for device in psutil.disk_partitions():
            usb_devices.append(f"{device.device} | {device.mountpoint}")
    return jsonify(usb_devices)

# Flask route for file integrity check
@app.route('/check_integrity', methods=['POST'])
def check_data_integrity():
    file_path = request.form['file_path']
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return jsonify({"sha256": sha256_hash.hexdigest()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
