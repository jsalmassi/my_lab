import hashlib
from helper import decode_base58, hash160

BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58decode(s):
    num = 0
    for c in s:
        num = num * 58 + BASE58.index(c)
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')

def wif_to_privkey(wif):
    decoded = b58decode(wif)

    payload = decoded[:-4]
    checksum = decoded[-4:]

    check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    if check != checksum:
        raise ValueError("Bad checksum")

    # remove version byte (0xef)
    payload = payload[1:]

    # remove compression flag (0x01)
    if payload[-1] == 0x01:
        payload = payload[:-1]

    return payload  # 32 bytes
##### using it ############
# we are using a testnet WIF private key, which starts with 'K' or 'L' and is 52 characters long
# which I grabbed from electrum wallet corresponding to teh adress: "tb1qulcfyq9arwn45fjjag5dwyy8u3wze2mw046r5g"
# wif = my_privKey.split(":")[-1] # if you have not removed the 'p2wpkh:' prefix from the WIF private key, you can do this to get the WIF private key
wif = 'cNM78qTBgM99a1Gs1VvG7sajPoGU1cVeE3dBs1MoQeY69VTdVo53'
#wif = 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rdcJfsz6iB4Q'
priv = wif_to_privkey(wif)
print(len(priv))   # must be 32
# now we have the private key in bytes, we can use it to get the public key in compressed format
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der as der_encode

sk = SigningKey.from_string(priv, curve=SECP256k1)
vk = sk.get_verifying_key()
# we can use the sk and vk to get the public key in compressed format, which is 33 bytes long,
#  and starts with 0x02 or 0x03 depending on the parity of the y coordinate
# if the y coordinate is even, we use 0x02, otherwise we use 0x03
# At this point we can use the sk and vk to sign messages and verify signatures,
#  but we just want to get the public key in compressed format, so we can use it
#  to get the address and the scriptPubKey for the transaction above.
pubkey = b'\x02' + vk.to_string()[:32] if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()[:32]
print('pubkey:', pubkey.hex())
####
# now we have the public key in compressed format, we can use it to get the address and the scriptPubKey for the transaction above.


# Now compute HASH160 of that pubkey and confirm it matches your address.
from helper import hash160 as my_hash160
hash160 = my_hash160(pubkey)
print('hash160 is: ',hash160.hex())
# now get the address from the hash160, which is is a segwit address,
#  which starts with 'tb1' for testnet and 'bc1' for mainnet, and is 42 characters long for testnet and 42
#  or 62 characters long for mainnet depending on the version of segwit used.
# ---- Create address ----
import bech32_addr_conversion as bech32 
witver = 0
program = hash160

data = [witver] + bech32.convertbits(program, 8, 5)
address = bech32.bech32_encode("tb", data)

print('the bech32 address:', address)
####### now we sign and then verify a message using the private key and the public key we just got, to confirm that we have the correct private key and public key pair.
message = b"Hello, Bitcoin!"

#sig = sk.sign_digest(message, sigencode=lambda r, s, order: der_encode(r, s))
#sig += b'\x01'  # SIGHASH_ALL

##signature = sk.sign(message)
from ecc import PrivateKey
from helper import (
    encode_varint,
    hash256,
    int_to_little_endian,
    little_endian_to_int,
    read_varint,
    SIGHASH_ALL,)
secret = 8675309
priv = PrivateKey(secret=secret)
h256 = hash256(message)
# convert the result to an integer using int.from_bytes(x, 'big')
message = int.from_bytes(h256, 'big')
der = priv.sign(message).der()
        # append the SIGHASH_ALL to der (use SIGHASH_ALL.to_bytes(1, 'big'))


signature = der + SIGHASH_ALL.to_bytes(1, 'big')

print('signature:', signature.hex())
# now we verify the signature using the public key
##assert vk.verify(signature, message)
##assert priv.point.verify(signature, message)


print("Signature is valid!")     
# though the above signing and verifying  in above code works, it is not the
#  same as the signing and verifying that is done in the transaction
#  signing, which uses the SIGHASH_ALL flag and the transaction data to
#  create the signature, and then verifies 
# but here is more complete signing and verifying 
########################
print('-------------------------------------------------------------------')
""" cache_file = '/home/jsalmassi/my_projects/my_lab/tx.cache'  #js
from helper import SIGHASH_ALL
from tx import TxIn, TxOut, Tx
import script
import my_tx_build_send3 as send3   
# create a dummy transaction input and output to sign
#tx_in = TxIn(bytes.fromhex('00'*32), 0, b'', 0xffffffff)

### prev_tx = bytes.fromhex('6b570a95f115b5ea884b32e17e1c1422470572e71cd67c2709f35cfdcb4e1439')
prev_index = 1
tx_in = TxIn(prev_tx, prev_index, b'', 0xffffffff)
### 
tx_out = TxOut(100000, b'')  # 100000 satoshis, empty scriptPubKey for simplicity
script_pubkey = script.p2wpkh_script(bytes(send3.decoded_segwit_addr2[1]))
tx_out = TxOut(100000, script_pubkey)  # 100000 satoshis, empty scriptPubKey for simplicity 

tx = Tx(1, [tx_in], [tx_out], 0, testnet=True, segwit=True)
#tx.serialize()  # this will compute the transaction hash and set the txid attribute of the transaction object, which is needed for signing
# sign the transaction input using the private key
signature = tx.sign_input(0, sk)#.to_string())#, SIGHASH_ALL) SIGHASH_ALL is included when we call the sign_input() method of the Tx class, which is the default behavior, so we dont need to pass it as an argument here.
print('transaction signature:', signature.hex())
# now we verify the signature using the public key
assert tx.verify_input(0)
print("Transaction signature is valid!")
 """
import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch13")
script = importlib.import_module('script') 
p2wpkh_script = script.p2wpkh_script

sys.path.append("/home/jsalmassi/my_projects/pybitcointools/cryptos")
segwit_addr = importlib.import_module('segwit_addr')

from tx import TxIn, TxOut, Tx

prev_tx = bytes.fromhex('96736e75daa32935536c4bb5edf783218cf1d317bfcb48c0c9c5c81cc8491133')
prev_index = 0

target_address= 'tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg' # both the target address and the change
#address are segwit addresses from the same wallet my 4.7 single-sig .
target_amount = 40000
change_address = 'tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c'
change_amount = 7000
#fee 50000-(40000+7000) = 3000 satoshis, which is a reasonable fee for a transaction with 1 input and 2 outputs, and the transaction size is around 200 bytes, so the fee rate is around 15 satoshis/byte, which is a reasonable fee rate for a transaction that we want to be confirmed in the next few blocks.

tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))
tx_outs = []

from helper import hash160 as my_hash160
decoded_segwit_addr = segwit_addr.decode_segwit_address("tb", "tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg")
print('version is: ',decoded_segwit_addr[0])
print("decoded_segwit_addr",decoded_segwit_addr[1])
script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr[1]))# same as h160, which is the same as the witness program, which is the same as the hash160 of the public key
print('script_pubkey for target  target address is: ', script_pubkey.serialize().hex())

target_satoshis = int(target_amount)
tx_outs.append(TxOut(target_satoshis, script_pubkey))

decoded_segwit_addr2 = segwit_addr.decode_segwit_address("tb", "tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c")
print('version is: ',decoded_segwit_addr2[0])
print("decoded_segwit_addr2",decoded_segwit_addr2[1])
script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr2[1]))
print('script_pubkey for change address is: ', script_pubkey.serialize().hex())


change_satoshis = int(change_amount)
tx_outs.append(TxOut(change_satoshis, script_pubkey))

tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True , segwit=True)
print(tx_obj.sign_input(0, priv))
print("-----------------------------------------------------    ")
print("signature of the transaction input is:", tx_obj.tx_ins[0].script_sig.cmds[0].hex())
assert priv.point.verify(tx_obj.tx_ins[0].script_sig.cmds[0], tx_obj.sig_hash(0))
print("------------------------------------------------")
print("here is the tx_obj.serialize().hex():", tx_obj.serialize().hex())
