# oveflow_toolkit
These are a collection of tools I have written to help me learn how to develop and execute buffer overflow exploits.  This code does not contain exploit code in the form.  It does however provide a framework to send data to a destination.

# Warning
I am not responsible for your actions, this code is to be used at your own risk and against systems you have permission to target.

# Example
Note the MS02_039 exploit code needs to be added by you, to the shellcode.py file.  I am not currently providing exploit code as part of this toolkit

sudo python2 attack_skeleton.py --rhost <target_ip> --rport 1434 --proto udp --exploit MS02_039

# Note
I am uploading this code to use as a reference during my OSCP lab and exam report. There may be bugs, I may not update, it just need it accessible to offensive security instructors like a homework assignment.

# Reuse policy
This is nothing more than a cli tool that send data somewhere over tcp or udp, feel free to reuse as needed.  This code does not contain malicious code, and does not contain exploit code.
