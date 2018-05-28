

def alternite_elif(operation,priv):
    return {
        'decimal': priv
        'bin': encode(priv,256,32)
        'bin_commpressed': encode(priv, 256, 32) + b'\x01'
        'hex': encode(priv, 16, 64)
        'hex_compressed':encode(priv, 16, 64)+'01'
        'wif': bin_to_b58check(encode(priv, 256, 32), 128+int(vbyte))
        "wif_compressed": bin_to_b58check(encode(priv, 256, 32)+b'\x01', 128+int(vbyte))
    }.get(operation)

def decode_privkey(priv,formt=None):
    if not formt: formt = get_privkey_format(priv)
    if formt == 'decimal': return priv
    elif formt == 'bin': return decode(priv, 256)
    elif formt == 'bin_compressed': return decode(priv[:32], 256)
    elif formt == 'hex': return decode(priv, 16)
    elif formt == 'hex_compressed': return decode(priv[:64], 16)
    elif formt == 'wif': return decode(b58check_to_bin(priv),256)
    elif formt == 'wif_compressed':
        return decode(b58check_to_bin(priv)[:32],256)
    else: raise Exception("WIF does not represent privkey")