import http.server
import socketserver
import requests
import json
from html import escape

PORT = 8000

# Fetch data from the provided URL
url = "https://web.archive.org/cdx/search/cdx?url=*.nokia.com%2F*&collapse=urlkey&output=text&fl=original"
response = requests.get(url)
data = response.text.splitlines()

# HTML structure to display data with Bootstrap
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Archived Data</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Archived Data from *.nokia.com</h1>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th scope="col">URL</th>
                </tr>
            </thead>
            <tbody>
'''

# Add data rows to the table
for line in data:
    # Each line has the original URL (first column)
    html_template += f"<tr><td>{escape(line)}</td></tr>"

# Closing the table and body
html_template += '''
            </tbody>
        </table>
    </div>
</body>
</html>
'''

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_template.encode('utf-8'))
        else:
            super().do_GET()

# Set up the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
