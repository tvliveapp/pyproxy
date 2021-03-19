#!/usr/bin/env python
#coding: utf8

import base64
import hashlib
import binascii
from Crypto import Random
from Crypto.Cipher import AES

from os import urandom
import os

BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

import math
import random

"""
    AES: http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
    
    JavaScript: https://github.com/mdp/gibberish-aes

    Python: https://stackoverflow.com/questions/12221484/how-come-i-cant-decrypted-my-aes-encrypted-message-on-someone-elses-aes-decrypt
            https://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python
            https://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible


"""


def randArr ( num ):
    """
        JavaScript Code:

        var result = [], i;
        for (i = 0; i < num; i++) {
            result = result.concat(Math.floor(Math.random() * 256));
        }
        return result;
    """
    return map( lambda i: math.floor(random.random() * 256 ), xrange(num) )

def s2a(s, binary):
    """
        JavaScript Code:

        var array = [], i;
        if (! binary) {
            string = enc_utf8(string);
        }
        for (i = 0; i < string.length; i++) {
            array[i] = string.charCodeAt(i);
        }
        return array;
    """
    return map( lambda s: ord(s), list(s) )
    
def openSSLKey(passwordArr, saltArr, Nr, Nk):
    # Nr: Default to 256 Bit Encryption
    # // Number of rounds depends on the size of the AES in use
    # // 3 rounds for 256
    # //        2 rounds for the key, 1 for the IV
    # // 2 rounds for 128
    # //        1 round for the key, 1 round for the IV
    # // 3 rounds for 192 since it's not evenly divided by 128 bits


    # if !Nr: Nr = 14
    # if !Nk: Nk = 8

    # if Nr >= 12: rounds = 3
    # else: rounds = 2

    # key = []
    # iv = []
    # md5_hash = []
    # result = []
    # data00 = passwordArr + saltArr

    """
    JavaScript Code:

        var rounds = Nr >= 12 ? 3: 2,
        key = [],
        iv = [],
        md5_hash = [],
        result = [],
        data00 = passwordArr.concat(saltArr),
        i;
        md5_hash[0] = MD5(data00);
        result = md5_hash[0];
        for (i = 1; i < rounds; i++) {
            md5_hash[i] = MD5(md5_hash[i - 1].concat(data00));
            result = result.concat(md5_hash[i]);
        }
        key = result.slice(0, 4 * Nk);
        iv = result.slice(4 * Nk, 4 * Nk + 16);
        return {
            key: key,
            iv: iv
        };

    """
    pass

class AESCipher2:
    def __init__( self, key ):
        self.key = hashlib.sha256(key).digest()
    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        print(salt)
        d_i = hashlib.md5(str.encode(d_i + password + salt.decode('unicode_escape'))).digest()
        d += d_i.decode('unicode_escape')
    return d[:key_length], d[key_length:key_length+iv_length]


class AESCipher:
    def __init__(self):
        pass
    def encrypt(self, plaintext, password, key_length=32):
        data = ""
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))

        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        data += 'Salted__' + salt
        chunk = plaintext

        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)

        data += cipher.encrypt( chunk )
        return base64.b64encode(data)

    def decrypt(self, data, password, key_length=32):
        data = base64.b64decode(data)
        bs = AES.block_size
        salt = data[len("Salted__"): 16]
        data = data[len("Salted__")+len(salt): ]

        key, iv = derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        chunk = cipher.decrypt( data )
        padding_length = ord(chunk[-1])

        return chunk[:-padding_length]


OpenSSL_AES = AESCipher()


KEY = "imtest"

def encrypt(plaintext, key="imtest"):
    return OpenSSL_AES.encrypt(plaintext, key)

def decrypt(plaintext, key="imtest"):
    return OpenSSL_AES.decrypt(plaintext, key)


