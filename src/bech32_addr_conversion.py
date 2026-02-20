# Minimal Bech32 implementation (BIP-173)
# Works for SegWit addresses (v0 P2WPKH / P2WSH)
# js
import importlib , sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch13")
import script
#script = importlib.import_module('script')
#end js
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
CHARSET_MAP = {c: i for i, c in enumerate(CHARSET)}

def bech32_polymod(values):
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            chk ^= generator[i] if ((b >> i) & 1) else 0
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0,0,0,0,0,0]) ^ 1
    return [(polymod >> 5*(5-i)) & 31 for i in range(6)]

def bech32_verify_checksum(hrp, data):
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1

def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def bech32_decode(addr):
    addr = addr.lower()
    pos = addr.rfind('1')
    if pos < 1:
        return None, None
    hrp = addr[:pos]
    data = [CHARSET_MAP.get(c, -1) for c in addr[pos+1:]]
    if any(d == -1 for d in data):
        return None, None
    if not bech32_verify_checksum(hrp, data):
        return None, None
    return hrp, data[:-6]

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

if  __name__ == "__main__":
        # Example usage
    """ hrp, data = bech32_decode("01d5d92effa6ffba3efa379f9830d0f75618b13393827152d26e4309000e88b1")
    print("HRP:", hrp)
    print("Data:", data)
    encoded = bech32_encode(hrp, data)
    print("Encoded:", encoded)   """
    
    # addr = "tb1qq82ajthl5mlm50h6x70esvxs7atp3vfnjwp8z5kjdepsjqqw3zcsj5rufw"  # your address here
    # addr = "tb1qs944ezcekvv08atc3z6ugdy0gprxam0s7nsltu"  # your address here
    addr = "tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg"  # your address here

    hrp, data = bech32_decode(addr)

    version = data[0]
    program = bytes(convertbits(data[1:], 5, 8, False))

    print("HRP:", hrp)
    print("Version:", version)
    print("Program (hex):", program.hex())
    print("----------------------------------------------------")
    ################################################################
    witness_program = bytes.fromhex(
        #"01d5d92effa6ffba3efa379f9830d0f75618b13393827152d26e4309000e88b1"
        #'816b5c8b19b318f3f57888b5c4348f40466eedf0'
        'd52ad7ca9b3d096a38e752c2018e6fbc40cdf26f'

    )

    # SegWit v0
    version = 0

    data = [version] + convertbits(witness_program, 8, 5)
    address = bech32_encode("tb", data)

    print('address:', address)
    print("----------------------------------------------------")
    ############################################################
    script_pubkey = script.p2wpkh_script(bytes.fromhex('816b5c8b19b318f3f57888b5c4348f40466eedf0'))#(witness_program)
    print("ScriptPubKey (hex):", script_pubkey.serialize().hex())

    script_pubkey = script.p2wpkh_script(bytes.fromhex('da12351ee60283ed137271d85ea15f83409f9d99'))#(witness_program)
    print("ScriptPubKey (hex):", script_pubkey.serialize().hex())