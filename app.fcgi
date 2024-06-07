#!/home/videovox2024/voxvideos.rubenmaestre.com/venv/bin/python3
from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()
