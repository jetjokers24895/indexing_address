import os
import hashlib
import binascii
import sys
import re


is_python2 = sys.version_info.major
# publickey = "032d69da7e61f1cec076d1ace58d96d3ef4a2f3ae248eadbc99846d4aebb653a5d"

code_strings = {
        2: '01',
        10: '0123456789',
        16: '0123456789abcdef',
        32: 'abcdefghijklmnopqrstuvwxyz234567',
        58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
        256: ''.join([chr(x) for x in range(256)])
}

def get_pubkey_format(pub):
    if is_python2:
        two = '\x02'
        three = '\x03'
        four = '\x04'
    else:
        two = 2
        three = 3
        four = 4

    if isinstance(pub, (tuple, list)): return 'decimal'
    elif len(pub) == 65 and pub[0] == four: return 'bin'
    elif len(pub) == 130 and pub[0:2] == '04': return 'hex'
    elif len(pub) == 33 and pub[0] in [two, three]: return 'bin_compressed'
    elif len(pub) == 66 and pub[0:2] in ['02', '03']: return 'hex_compressed'
    elif len(pub) == 64: return 'bin_electrum'
    elif len(pub) == 128: return 'hex_electrum'
    else: raise Exception("Pubkey not in recognized format")

def bin_to_b58check(inp, type_chain='main', magicbyte=0):
    if type_chain == 'main':        
        if magicbyte == 0:
            inp = '\x00' + inp
        while magicbyte > 0:
            inp = chr(int(magicbyte % 256)) + inp
            magicbyte //= 256
        leadingzbytes = len(re.match('^\x00*', inp).group(0))
        checksum = bin_dbl_sha256(inp)[:4]
        return '1' * leadingzbytes + changebase(inp+checksum, 256, 58) # not yet test
    elif type_chain == 'testnet':
        if magicbyte == 0:
            inp = '\x6f' + inp
        while magicbyte > 0:
            inp = chr(int(magicbyte % 256)) + inp
            magicbyte //= 256
        # leadingzbytes = len(re.match('^\x6f*', inp).group(0))
        checksum = bin_dbl_sha256(inp)[:4]
        return changebase(inp+checksum, 256, 58)
        
def bin_dbl_sha256(s):
    bytes_to_hash = from_string_to_bytes(s)
    return hashlib.sha256(hashlib.sha256(bytes_to_hash).digest()).digest()

def bin_hash160(string):
    intermed = hashlib.sha256(string).digest()
    digest = ''
    try:
        digest = hashlib.new('ripemd160', intermed).digest()
        return digest
    except:
        raise TypeError("fail to ripemd160,let use alternitive function")

def pubkey_to_address(pubkey,type_chain, magicbyte=0): #from pybitcointools
    if isinstance(pubkey, (list, tuple)):
        pubkey = encode_pubkey(pubkey, 'bin')
    if len(pubkey) in [66, 130]:
        # bin_hash_160 = bin_hash160(binascii.unhexlify(pubkey))
        # print "%s : %s" % (type(bin_hash_160),bin_hash_160)
        return bin_to_b58check(
            bin_hash160(binascii.unhexlify(pubkey)),type_chain,magicbyte)
    return bin_to_b58check(bin_hash160(pubkey), magicbyte)

def from_string_to_bytes(s):
    return s

def get_code_string(base):
    return code_strings.get(base,"Invalid base!")

def lpad(msg, symbol, length):
    if len(msg) >= length:
        return msg
    return symbol * (length - len(msg)) + msg

def changebase(string, frm, to, minlen=0):
    if frm == to:
        return lpad(string, get_code_string(frm)[0], minlen)
    return encode(decode(string, frm), to, minlen)

def encode(val, base, minlen=0):
    base, minlen = int(base), int(minlen)
    code_string = get_code_string(base)
    result = ""
    while val > 0:
        result = code_string[val % base] + result
        val //= base
    return code_string[0] * max(minlen - len(result), 0) + result

def decode(string, base):
    base = int(base)
    code_string = get_code_string(base)
    result = 0
    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += code_string.find(string[0])
        string = string[1:]
    return result

