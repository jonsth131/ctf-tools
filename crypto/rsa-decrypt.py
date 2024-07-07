#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes
import argparse


def decrypt(c, p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    return long_to_bytes(m).decode()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="RSA Decryptor")
    argparser.add_argument("-c", type=int, help="Ciphertext", required=True)
    argparser.add_argument("-p", type=int, help="First prime", required=True)
    argparser.add_argument("-q", type=int, help="Second prime", required=True)
    argparser.add_argument(
        "-e", type=int, help="Public exponent", default=65537)

    args = argparser.parse_args()
    c = args.c
    p = args.p
    q = args.q
    e = args.e

    pt = decrypt(c, p, q, e)
    print(pt)
