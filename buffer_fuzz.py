#!/usr/bin/env python2
"""
Usage:
  buffer_fuzz.py payload (--length=<length>)
  buffer_fuzz.py fuzz (--rhost=<rhost> --rport=<rport> --interface=<interface> --wait=<wait> --delta=<delta> --proto=<proto>)
  buffer_fuzz.py send (--rhost=<rhost> --rport=<rport> --length=<integer> --interface=<interface> --proto=<proto>)
  buffer_fuzz.py send_a (--rhost=<rhost> --rport=<rport> --length=<integer> --interface=<interface> --proto=<proto>)

Options:
  --rhost=<rhost>           Target to host
  --rport=<rport>           Port to fuzz on target
  --length=<length>         Integer representing length of payload to fuzz buffer
  --interface=<interface>   Source interface
"""


from time import sleep
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from netifaces import AF_INET, ifaddresses
from string import ascii_lowercase, ascii_uppercase, digits
from docopt import docopt


def gen_pattern_uniq(length):
    """Generate a unique pattern of N length with a max length of 20280."""
    print("Pattern length used: {}".format(length))
    pattern = []
    for a in ascii_lowercase:
        for b in ascii_uppercase:
            for d in digits:
                pattern.append(str(a))
                pattern.append(str(b))
                pattern.append(str(d))
    if length > 20280:
        print("Using max length of 20280")
        length = 20280  # Extra but more explicit as below list slice failsback to max length
    pattern_to_length = ''.join(pattern[0:int(length)])
    print("Pattern: {}".format(pattern_to_length))
    return pattern_to_length

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

def talk_to_service(rhost, rport, payload, iface, proto):
    print("Target: {}, Port: {}, Payload Length: {}, Iface: {}, Proto: {}".format(rhost, rport, len(payload), iface, proto))
    if proto.lower() == "tcp":
        send_tcp(rhost=rhost, rport=rport, iface=iface, payload=payload)
    elif proto.lower() == "udp":
        send_udp(rhost=rhost, rport=rport, iface=iface, payload=payload)
    else:
        print("protocol must be either udp or tcp, not {}".format(proto))

def fuzz_service(rhost, rport, iface, delta, wait, proto):
    pattern_length = 50
    while True:
        try:
            payload = gen_pattern_uniq(pattern_length)
            talk_to_service(rhost, rport, payload, iface, proto)
            pattern_length += int(delta)
            sleep(int(wait))
        except Exception as ex:
            print("Target service unresponsive")
            print(str(ex))
            break

def main():
    opts = docopt(__doc__)
    print("CLI options used: {}".format(opts))
    if opts['payload']:
        gen_pattern_uniq(
            length=int(opts['--length'])
            )
    elif opts['send']:
        payload = gen_pattern_uniq(opts['--length'])
        talk_to_service(
            rhost=opts['--rhost'],
            rport=opts['--rport'],
            payload=payload,
            iface=opts['--interface'],
            proto=opts['--proto']
            )
    elif opts['send_a']:
        payload = ("A" * int(length))
        talk_to_service(
            rhost=opts['--rhost'],
            rport=opts['--rport'],
            payload=payload,
            iface=opts['--interface'],
            proto=opts['--proto']
            )
    elif opts['fuzz']:
        fuzz_service(
            rhost=opts['--rhost'],
            rport=opts['--rport'],
            iface=opts['--interface'],
            wait=opts['--wait'],
            delta=opts['--delta'], 
            proto=opts['--proto']
            )

if __name__ == '__main__':
    main()
