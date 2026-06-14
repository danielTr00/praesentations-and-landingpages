#!/usr/bin/env python3
"""Simple HTTP server for managing files in /Users/Uni/Desktop/Coding."""
import os, json, shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT_DIR = "/Users/Uni/Desktop/Coding"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/list':
            items = []
            for e in os.scandir(ROOT_DIR):
                s = e.stat()
                items.append({'name':e.name,'isDir':e.is_dir(),'size':s.st_size if not e.is_dir() else 0,
                              'modified':s.st_mtime*1000,'selected':False})
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(items).encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/delete':
            cl = int(self.headers.get('Content-Length',0))
            body = json.loads(self.read(cl).decode())
            fnames = body.get('files',[])
            ok, errs = 0, []
            for f in fnames:
                p = os.path.join(ROOT_DIR, f)
                try:
                    if os.path.isdir(p): shutil.rmtree(p)
                    else: os.remove(p)
                    ok += 1
                except Exception as e: errs.append(f'{f}: {e}')
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success':True,'message':f'{ok} Elemente gelöscht','errors':errs}).encode())

    def log_message(self, *a): pass

if __name__ == '__main__':
    s = HTTPServer(('127.0.0.1',8900), Handler)
    print("🌐 Server running on http://localhost:8900")
    print("📁 Root: " + ROOT_DIR)
    s.serve_forever()
