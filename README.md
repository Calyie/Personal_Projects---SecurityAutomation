# How to Use the Reverse Backdoor
NOTE: As these are just simple scripts to remotely connect to systems (can be used for malicious and benign purposes), it should evade most firewall detections.
 
# Before running listener.py:
Open the script and go to the second to the last line of code. <br>
Change "hacker_privateIP" to the private IP of your hacker machine. This ip address must be within the quotes "" as it is a string variable. <br>
Run listener.py on your hacker machine. This script should be executed before running reverse_backdoor.py on the victim machine. <br>
 
# Before running reverse_backdoor.py:
Open the script and go to the second to the last line of code.  
Change "hacker_publicIP" to the public IP of your hacker machine. This ip address must be within the quotes "" as it is a string variable. <br>
Run reverse_backdoor.py on the victim machine. <br>
 
# Acceptable commands:
Using the hacker machine (listener) to access the victim machine (backdoor), the following commands are possible.
 
1. All Linux and Windows OS commands (based on the victim machine's OS) such as cd, dir, ls, cat, etc.
2. Upload function allows you to upload files (e.g., malware) into the backdoor... <br)>
Syntax: <br>
>> upload <filename> <br>
Important: Ensure that the file you are uploading is in the same directory where you have executed the listener.py script
3. Download function allows you to exfiltrate files from the backdoor... <br>
Syntax: <br>
>> download <filename>
