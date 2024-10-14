#!/usr/bin/env python3
import argparse
import os.path
from scapy.all import *

usb_hid_keymap = {
    4: 'a',
    5: 'b',
    6: 'c',
    7: 'd',
    8: 'e',
    9: 'f',
    10: 'g',
    11: 'h',
    12: 'i',
    13: 'j',
    14: 'k',
    15: 'l',
    16: 'm',
    17: 'n',
    18: 'o',
    19: 'p',
    20: 'q',
    21: 'r',
    22: 's',
    23: 't',
    24: 'u',
    25: 'v',
    26: 'w',
    27: 'x',
    28: 'y',
    29: 'z',
    30: '1',
    31: '2',
    32: '3',
    33: '4',
    34: '5',
    35: '6',
    36: '7',
    37: '8',
    38: '9',
    39: '0',
    40: 'Enter',
    41: 'esc',
    42: 'del',
    43: 'tab',
    44: ' ',
    45: '-',
    47: '{',
    48: '}',
    56: '/',
    57: 'CapsLock',
    79: 'RightArrow',
    80: 'LetfArrow'
}


def read_packets(pcap):
    try:
        return rdpcap(pcap)
    except:
        print('[-] Couldn\'t read capture file')
        exit(-1)


def read_values(packets):
    text = ''
    for packet in packets:
        value = packet.load[-6]
        if value in usb_hid_keymap:
            text += usb_hid_keymap[value]
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='USB HID Pcap decoder')
    parser.add_argument('-p', '--pcap', help='Packet capture file',
                        type=ascii, required=True)
    args = parser.parse_args()

    packets = read_packets(args.pcap.replace("'", ''))
    text = read_values(packets)

    print(text)
