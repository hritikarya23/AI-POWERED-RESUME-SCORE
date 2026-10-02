import os
import sys
import traceback

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from app.main import app
    application = app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI()
    application = app
    err_tb = traceback.format_exc()
    dir_info = f"Current dir: {os.getcwd()}, Contents: {os.listdir('.')}, ROOT_DIR: {ROOT_DIR}"

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(path_name: str = ""):
        return HTMLResponse(
            status_code=500,
            content=f"""
            <html>
            <body style='font-family:monospace;padding:30px;background:#1e1e2e;color:#f38ba8;'>
                <h2>Vercel Startup Exception Captured</h2>
                <p><strong>Environment Info:</strong> {dir_info}</p>
                <pre style='background:#11111b;padding:20px;border-radius:8px;color:#cdd6f4;'>{err_tb}</pre>
            </body>
            </html>
            """
        )
