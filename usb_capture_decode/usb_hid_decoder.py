#!/usr/bin/env python3
import argparse
from scapy.all import *

usb_hid_keymap = {
    4: ['a', 'A'],
    5: ['b', 'B'],
    6: ['c', 'C'],
    7: ['d', 'D'],
    8: ['e', 'E'],
    9: ['f', 'F'],
    10: ['g', 'G'],
    11: ['h', 'H'],
    12: ['i', 'I'],
    13: ['j', 'J'],
    14: ['k', 'K'],
    15: ['l', 'L'],
    16: ['m', 'M'],
    17: ['n', 'N'],
    18: ['o', 'O'],
    19: ['p', 'P'],
    20: ['q', 'Q'],
    21: ['r', 'R'],
    22: ['s', 'S'],
    23: ['t', 'T'],
    24: ['u', 'U'],
    25: ['v', 'V'],
    26: ['w', 'W'],
    27: ['x', 'X'],
    28: ['y', 'Y'],
    29: ['z', 'Z'],
    30: ['1', '!'],
    31: ['2', '@'],
    32: ['3', '#'],
    33: ['4', '$'],
    34: ['5', '%'],
    35: ['6', '^'],
    36: ['7', '&'],
    37: ['8', '*'],
    38: ['9', '('],
    39: ['0', ')'],
    40: '<Enter>',
    41: '<esc>',
    42: '<del>',
    43: '<tab>',
    44: ' ',
    45: ['-', '_'],
    46: ['=', '+'],
    47: ['[', '{'],
    48: [']', '}'],
    49: ['\\', '|'],
    50: ['#', '~'],
    51: [';', ':'],
    52: ['\'', '"'],
    53: ['`', '~'],
    54: [',', '<'],
    55: ['.', '>'],
    56: ['/', '?'],
    57: 'CapsLock',
    79: 'RightArrow',
    80: 'LetfArrow',
    88: '<enter>',
    89: '1',
    90: '2',
    91: '3',
    92: '4',
    93: '5',
    94: '6',
    95: '7',
    96: '8',
    97: '9',
    98: '0',
    99: '.',
}


def read_packets(pcap):
    try:
        return rdpcap(pcap)
    except Exception as e:
        print(f'[-] Couldn\'t read capture file, {e}')
        exit(-1)


def read_values(packets):
    text = ''
    for packet in packets:
        value = packet.load[-6]
        if value in usb_hid_keymap:
            modifier = packet.load[-8]
            val = usb_hid_keymap[value]
            if modifier == 32:
                if len(val) == 2:
                    text += val[1]
                else:
                    text += val
            else:
                if len(val) == 2:
                    text += val[0]
                else:
                    text += val
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='USB HID Pcap decoder')
    parser.add_argument('-p', '--pcap', help='Packet capture file',
                        type=ascii, required=True)
    args = parser.parse_args()
    pcap = args.pcap.replace("'", "")

    packets = read_packets(args.pcap.replace("'", ''))
    text = read_values(packets)

    print(text)
