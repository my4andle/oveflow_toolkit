#!/usr/bin/env python3
"""
Usage:
  buffer_fuzz.py payload (--length=<length>)
  buffer_fuzz.py fuzz (--target=<target> --port=<port> --interface=<interface> --wait=<wait> --delta=<delta>)
  buffer_fuzz.py send (--target=<target> --port=<port> --length=<integer> --interface=<interface>)
  buffer_fuzz.py send_a (--target=<target> --port=<port> --length=<integer> --interface=<interface>)

Options:
  --target=<target>         Target to fuzz
  --port=<port>             Port to fuzz on target
  --length=<length>         Integer representing length of payload to fuzz buffer
  --interface=<interface>   Source interface
"""
import socket

from time import sleep
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
    pattern_to_bytes = pattern_to_length.encode()
    print("Pattern: {}".format(pattern_to_bytes))
    return pattern_to_bytes

#make generic socket function
def talk_to_service(target, port, iface, payload):
    print("Communicating with target {} on port {} with payload length {}".format(target, port, len(payload)))
    iface_ip = ifaddresses(iface)[AF_INET][0]['addr']
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.settimeout(2)
    soc.bind((iface_ip, 0))
    soc.connect((target, int(port)))
    soc.send(payload)
    response = soc.recv(1024)
    print(response)

# add method for one time call
def fuzz_service(target, port, iface, delta, wait):
    pattern_length = 50
    while True:
        try:
            payload = gen_pattern_uniq(pattern_length)
            talk_to_service(target, port, iface, payload)
            pattern_length += int(delta)
            # sleep(int(wait))
        except Exception as ex:
            print("Target service unresponsive")
            print(str(ex))
            break

def main():
    opts = docopt(__doc__)
    print("CLI options used: {}".format(opts))
    if opts['send']:
        length = int(opts['--length'])
        target = opts['--target']
        port = opts['--port']
        iface = opts['--interface']
        payload = gen_pattern_uniq(length)
        talk_to_service(target, port, iface, payload)
    elif opts['fuzz']:
        target = opts['--target']
        port = opts['--port']
        iface = opts['--interface']
        wait = opts['--wait']
        delta = opts['--delta']
        fuzz_service(target, port, iface, wait, delta)
    elif opts['payload']:
        gen_pattern_uniq(int(opts['--length']))
    elif opts['send_a']:
        length = int(opts['--length'])
        target = opts['--target']
        port = opts['--port']
        iface = opts['--interface']
        payload = ("A" * int(length)).encode()
        talk_to_service(target, port, iface, payload)


if __name__ == '__main__':
    main()
