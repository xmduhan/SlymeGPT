import subprocess

def main():
    command = "docker run -d --restart=always --shm-size=512m -p 6901:6901 -p 8000:8000 -e VNC_PW=password flygpt"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
