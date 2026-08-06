import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
import mimetypes
import traceback
from datetime import datetime

PORT = 3000
DB_FILE = 'database.db'

# Initialize SQL Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT NOT NULL,
            phone TEXT NOT NULL,
            solution_requirement TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class RequestHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # API: Get all leads from SQL Database
        if path == '/api/leads':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contact_leads ORDER BY created_at DESC')
            rows = cursor.fetchall()
            leads = [dict(row) for row in rows]
            conn.close()
            
            self._set_headers(200, 'application/json')
            self.wfile.write(json.dumps(leads).encode('utf-8'))
            return

        # ADMIN DASHBOARD PAGE
        if path == '/admin':
            self._set_headers(200, 'text/html; charset=utf-8')
            admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Radius Systems - Admin Leads Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Red+Hat+Display:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body { font-family: 'DM Sans', sans-serif; background: #F8FAFC; color: #1C2539; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #1C2539; color: #FFF; padding: 20px 30px; border-radius: 12px; margin-bottom: 30px; }
        .header h1 { font-family: 'Red Hat Display', sans-serif; font-size: 1.6rem; margin: 0; }
        .badge { background: #DF0A0A; color: #FFF; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; }
        .card { background: #FFF; border-radius: 12px; border: 1px solid #E2E8F0; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; margin-top: 16px; }
        th, td { padding: 14px; text-align: left; border-bottom: 1px solid #E2E8F0; font-size: 0.95rem; }
        th { background: #F1F5F9; font-weight: 700; color: #1C2539; }
        tr:hover { background: #F8FAFC; }
        .btn { background: #DF0A0A; color: #FFF; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block; }
        .btn:hover { background: #1C2539; }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fa-brands fa-apple"></i> Radius Systems - SQL Leads Database</h1>
        <div><a href="/" class="btn" style="background:#FFF; color:#1C2539;">Go To Website</a></div>
    </div>

    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h2>Submitted Contact & Consultation Leads</h2>
            <span id="leadCount" class="badge">Loading...</span>
        </div>
        <table id="leadsTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Full Name</th>
                    <th>Work Email</th>
                    <th>Company</th>
                    <th>Phone</th>
                    <th>Requirement</th>
                    <th>Date & Time</th>
                </tr>
            </thead>
            <tbody>
                <tr><td colspan="7" style="text-align:center;">Loading leads from SQL database...</td></tr>
            </tbody>
        </table>
    </div>

    <script>
        fetch('/api/leads')
            .then(res => res.json())
            .then(data => {
                const tbody = document.querySelector('#leadsTable tbody');
                document.getElementById('leadCount').innerText = data.length + ' Total Leads';
                if(data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#64748B;">No leads submitted yet. Fill out the contact form on the website!</td></tr>';
                    return;
                }
                tbody.innerHTML = data.map(lead => `
                    <tr>
                        <td>#${lead.id}</td>
                        <td><strong>${lead.full_name}</strong></td>
                        <td><a href="mailto:${lead.email}">${lead.email}</a></td>
                        <td>${lead.company}</td>
                        <td><a href="tel:${lead.phone}">${lead.phone}</a></td>
                        <td><span style="background:#FFECEC; color:#DF0A0A; padding:4px 8px; border-radius:4px; font-weight:600; font-size:0.85rem;">${lead.solution_requirement}</span></td>
                        <td>${new Date(lead.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');
            });
    </script>
</body>
</html>'''
            self.wfile.write(admin_html.encode('utf-8'))
            return

        # Serve static files (HTML, CSS, JS, Images)
        if path == '/':
            path = '/index.html'

        file_path = '.' + path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            self._set_headers(200, mime_type)
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(404, 'text/html')
            self.wfile.write(b'<h1>404 File Not Found</h1>')

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API: Save Lead to SQL Database
        if parsed_path.path == '/api/contact':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                raw_str = post_data.decode('utf-8')
                
                # Parse JSON or form data
                if self.headers.get('Content-Type', '').startswith('application/json'):
                    data = json.loads(raw_str)
                else:
                    data = dict(urllib.parse.parse_qsl(raw_str))

                full_name = str(data.get('full_name', '')).strip()
                email = str(data.get('email', '')).strip()
                company = str(data.get('company', '')).strip()
                phone = str(data.get('phone', '')).strip()
                solution_requirement = str(data.get('solution_requirement', '')).strip()

                if not full_name or not email or not phone:
                    self._set_headers(400, 'application/json')
                    self.wfile.write(json.dumps({'error': 'Missing required fields: full_name, email, or phone'}).encode('utf-8'))
                    return

                # Save into SQL database
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contact_leads (full_name, email, company, phone, solution_requirement)
                    VALUES (?, ?, ?, ?, ?)
                ''', (full_name, email, company, phone, solution_requirement))
                conn.commit()
                new_id = cursor.lastrowid
                conn.close()

                print(f"[SQL SUCCESS] New Lead #{new_id} inserted: {full_name} ({email}) - {company}")

                self._set_headers(200, 'application/json')
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': 'Your inquiry details have been saved successfully into SQL Database.',
                    'id': new_id
                }).encode('utf-8'))

            except Exception as e:
                print(f"[SQL ERROR] Traceback: {traceback.format_exc()}")
                self._set_headers(500, 'application/json')
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

if __name__ == '__main__':
    server = socketserver.TCPServer(('', PORT), RequestHandler)
    print(f"Server running with SQL Database at http://localhost:{PORT}")
    print(f"Admin Dashboard available at http://localhost:{PORT}/admin")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

