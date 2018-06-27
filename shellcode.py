# https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/windows/mssql/ms02_039_slammer.rb
#Put your EXPLOIT CODE HERE and it can be imported into the framework for future use.
#You will need to piece together the exploit code which includes your shellcode in conjunction with any other bytes required to trigger an overflow.  You can do this by reverse engineering known exploits found in msf or exploit-db.
#Once you have working exploit code you can reuse here, but do not forget to create a handler for the specific shellcode.
#This will help when you can not use metasploit.
#Add print_status(Rex::Text.to_hex(buf)) to msf exploit to print your complete exploit code when executing
#use msfvenom to create shellcode, and then combine this with other required exploit code


ms02_039 = ("\x04\x41......."
"\x90\x90.........")


