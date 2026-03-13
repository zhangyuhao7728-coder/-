#!/usr/bin/env python3
"""
Launcher后端 - 处理launcher.html的各种请求
"""
import json
import os
import subprocess
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8888

class LauncherHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == '/api/stats':
            self.send_json(self.get_stats())
        elif path == '/api/status':
            self.send_json(self.get_system_status())
        elif path == '/api/open':
            app = query.get('app', [''])[0]
            self.send_json(self.open_app(app))
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_stats(self):
        """获取学习统计"""
        try:
            stats_file = os.path.expanduser("~/项目/Ai学习系统/learning/learning-data/stats.json")
            if os.path.exists(stats_file):
                with open(stats_file) as f:
                    return json.load(f)
        except:
            pass
        return {"level": 1, "total_time": 0, "problems": 0, "streak": 0}
    
    def get_system_status(self):
        """获取系统状态"""
        import requests
        
        status = {"gateway": False, "ollama": False, "models": []}
        
        try:
            resp = requests.get("http://127.0.0.1:18789/health", timeout=2)
            status["gateway"] = resp.json().get("ok", False)
        except:
            pass
        
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=2)
            if resp.ok:
                data = resp.json()
                status["ollama"] = True
                status["models"] = [m["name"] for m in data.get("models", [])]
        except:
            pass
        
        return status
    
    def open_app(self, app):
        """打开应用"""
        apps = {
            "streamlit": "~/项目/ai-coding-academy/start_app.sh",
            "dashboard": "~/项目/Ai学习系统/learning/dashboard/index_v2.html",
            "monitor": "python3 ~/.openclaw/scripts/openclaw_monitor.py --status",
        }
        
        if app == "streamlit":
            subprocess.Popen(["streamlit", "run", 
                os.path.expanduser("~/项目/ai-coding-academy/app/app.py")],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"success": True, "message": "启动Streamlit面板"}
        
        elif app == "dashboard":
            webbrowser.open("file://" + os.path.expanduser("~/项目/Ai学习系统/learning/dashboard/index_v2.html"))
            return {"success": True, "message": "打开仪表盘"}
        
        elif app == "monitor":
            result = subprocess.run(["python3", os.path.expanduser("~/.openclaw/scripts/openclaw_monitor.py"), "--status"],
                                 capture_output=True, text=True)
            return {"success": True, "output": result.stdout}
        
        return {"success": False, "message": "未知应用"}
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


def run_server():
    """运行服务器"""
    os.chdir(os.path.expanduser("~/项目/Ai学习系统/learning"))
    server = HTTPServer(("", PORT), LauncherHandler)
    print(f"🚀 Launcher服务器启动: http://localhost:{PORT}")
    print("   按 Ctrl+C 停止")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
