import uvicorn
from flygpt.api import app
import sys

def main():
    wait_user_confirm = False
    proxy_server = None

    # Check for command line arguments
    if "--help" in sys.argv:
        print("Usage: python start_api_server.py [--wait-user-confirm] [--proxy-server <proxy_address>]")
        return

    # Parse command line arguments
    if "--wait-user-confirm" in sys.argv:
        wait_user_confirm = True
    if "--proxy-server" in sys.argv:
        index = sys.argv.index("--proxy-server")
        proxy_server = sys.argv[index + 1]

    # Set app configurations
    app.wait_user_confirm = wait_user_confirm
    app.proxy_server = proxy_server

    uvicorn.run(app, host="0.0.0.0")

if __name__ == "__main__":
    main()
