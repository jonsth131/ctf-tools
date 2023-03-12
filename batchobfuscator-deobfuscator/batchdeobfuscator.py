"""
    Deobfuscator for https://github.com/moom825/batch-obfuscator-made-in-python
"""

import argparse
import sys


def remove_header(data):
    """Remove first two bytes of file to fix the characters"""
    return data[2:]


def remove_carets(data):
    """Remove optional carets"""
    return data.replace(b'^', b'')


def replace_variable_chars(data):
    """Replace all characters found in the R variable in obfuscated script"""
    data = data.replace(b'%r:~0,1%', b'J')
    data = data.replace(b'%r:~5,1%', b'G')
    data = data.replace(b'%r:~1,1%', b'g')
    data = data.replace(b'%r:~2,1%', b'i')
    data = data.replace(b'%r:~16,1%', b'I')
    data = data.replace(b'%r:~4,1%', b't')
    data = data.replace(b'%r:~6,1%', b'X')
    data = data.replace(b'%r:~7,1%', b'z')
    data = data.replace(b'%r:~14,1%', b'S')
    data = data.replace(b'%r:~8,1%', b's')
    data = data.replace(b'%r:~9,1%', b'w')
    data = data.replace(b'%r:~10,1%', b'b')
    data = data.replace(b'%r:~11,1%', b'h')
    data = data.replace(b'%r:~15,1%', b'H')
    data = data.replace(b'%r:~12,1%', b'm')
    data = data.replace(b'%r:~13,1%', b'u')
    data = data.replace(b'%r:~17,1%', b'O')
    return data


def remove_added_data(data):
    """Remove code added by obfuscator"""
    data = data.replace(b'&cls\n@%pUBlIc:~89,83%%PUBLic:~5,1%CHo of%PuBlIC:~46,16%f\n', b'')
    data = data.replace(b'SEt R=Jg%pUBLIc:~13,1%gtGXz%pUBLIc:~4,1%w%pUBLIc:~11,1%hm%pUBLIc:~10,1%SHIOA\n', b'')
    data = data.replace(b'%pUBlIC:~14,1%L%pUBliC:~55,17%%publIc:~4,1%\n@ecHO On\n', b'')
    data = data.replace(b'\n@echo off\nset a = %%~i', b'')
    data = data.replace(b'\nset a = % + %~i"%', b'')
    data = data.replace(b'%~i"%', b'')
    data = data.replace(b'\nset a = %a%\n:aaaaaaaaaaaaaaaaaaaaaaaaaaaaab', b'')
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deobfuscator for "batch obfuscator by moom825"')
    parser.add_argument('-i', '--input', help='Obfuscated bat file',
                        type=argparse.FileType('rb'), required=True)
    parser.add_argument('-o', '--output', help='File to save deobfuscated bat',
                        type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    file = args.input.read()

    file = remove_header(file)
    file = remove_carets(file)
    file = replace_variable_chars(file)
    file = remove_added_data(file)

    args.output.write(file.decode())

