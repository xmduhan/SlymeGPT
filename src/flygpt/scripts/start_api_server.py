import uvicorn
from flygpt.api import app
import sys

def main():
    proxy_server = None
    if len(sys.argv) > 1 and sys.argv[1] == "--proxy-server":
        proxy_server = sys.argv[2]
    app.proxy_server = proxy_server
    uvicorn.run(app, host="0.0.0.0")

if __name__ == "__main__":
    main()
