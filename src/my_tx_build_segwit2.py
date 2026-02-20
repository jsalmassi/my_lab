# this script is just a copy of the my_tx_build_segwit.py file, the diff between the two files is in
#  the my_tx_build_segwit.py file, is that I am not using the private key codes from the pybitcointools library to get the
#  private key and the public key, and I am grabbing it from the electrum wallet.
from helper import decode_base58, SIGHASH_ALL
from ecc import PrivateKey
from helper import hash160 as my_hash160
import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch13")
script = importlib.import_module('script') 
p2wpkh_script = script.p2wpkh_script

sys.path.append("/home/jsalmassi/my_projects/pybitcointools/cryptos")
segwit_addr = importlib.import_module('segwit_addr')

#p2pkh_script = script.p2pkh_script

# from test_txfrom test_tx import TxIn, TxOut, Tx
from tx import TxIn, TxOut, Tx

cache_file = '/home/jsalmassi/my_projects/my_lab/tx.cache'  #js


# create 1 TxIn and 2 TxOuts
# 1 of the TxOuts should be back to your address
# the other TxOut should be to this address

# get the private key from the exercise in Chapter 4
# change address should be the address generated from Chapter 4

# get the prev_tx and prev_index from the transaction where you got
# some testnet coins
# create a transaction input for the previous transaction with
# the default ScriptSig and sequence

# target amount should be 60% of the output amount
# set the fee to some reasonable amount
# change amount = amount from the prev tx - target amount - fee

# create a transaction output for the target amount and address
# create a transaction output for the change amount and address
# create the transaction object

# sign the one input in the transaction object using the private key
# print the transaction's serialization in hex
##################################################
#**************************************
# Very important note: usually this code is done based on the assumption that the public key
# in the previous transaction is in compressed sec format, which is the default.
# If it were in uncompressed sec format, which is the case here, then in the test_tx.py file, in the sign_input()
# method of the Tx class, the line:
# sec = private_key.point.sec()
# should be changed to:
# sec = private_key.point.sec( compressed=False)
#**************************************
prev_tx = bytes.fromhex('96736e75daa32935536c4bb5edf783218cf1d317bfcb48c0c9c5c81cc8491133')
prev_index = 0

secret = 8675309
priv = PrivateKey(secret=secret)

# the follwing is what I have done:
# worked out the public key in uncompressed sec format (hex) to be:
#priv.point.sec(compressed=False).hex() # here is went wrong, when I used compressed=False, becuase the 
# public key in the tx above is in compressed format by default.
# '04935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b673296fb8e372dec2f72836d46f17abd994218feefccefd89b6a3dc2b2da9a6375'

# priv.point.sec(compressed=True).hex()
#: '03935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67'
# this pubkes is used to give hash160 (witness program) for the segwit address generation
# to be:
#  'tb1q654d0j5m85yk5w882tpqrrn0h3qvmun0eeade2' #have 50000sats
#
#  which is used to get segwit address.from the bech32_addr_conversion.py so this is out WALLET for now.
#  So we send some sats to it, and then we will spend those coins in this transaction,
#  and send some of the coins to the target address, and the rest back to our change 
# address, which is also a segwit address. 

#priv.point.address(compressed=True,testnet=True)
#: 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'

# also worked the private key in WIF format to be 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rdcJfsz6iB4Q'
# by doing: priv.wif(compressed=True, testnet=True)
#------ above is just notes to myself ----------------------
target_address= 'tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg' # both the target address and the change
#address are segwit addresses from the same wallet my 4.7 single-sig .
target_amount = 40000
# change_address = 'tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c'
change_address = 'tb1q654d0j5m85yk5w882tpqrrn0h3qvmun0eeade2'
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

# decoded_segwit_addr2 = segwit_addr.decode_segwit_address("tb", "tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c")
decoded_segwit_addr2 = segwit_addr.decode_segwit_address("tb", "tb1q654d0j5m85yk5w882tpqrrn0h3qvmun0eeade2")
print('version is: ',decoded_segwit_addr2[0])
print("decoded_segwit_addr2",decoded_segwit_addr2[1])
script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr2[1]))
print('script_pubkey for change address is: ', script_pubkey.serialize().hex())


change_satoshis = int(change_amount)
tx_outs.append(TxOut(change_satoshis, script_pubkey))

tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True , segwit=True)
print(tx_obj.sign_input(0, priv))
print("signature of the transaction input is:", tx_obj.tx_ins[0].script_sig.cmds[0].hex())
print("------------------------------------------------")
print("tx_obj.serialize().hex():", tx_obj.serialize().hex())
# the signable transaction hash serialization in hex is:
# a952793354e9299436ae91c1cc4f6f0ba666510856df186e4e8929193e6f39f2
# the int() of it or also reffred to it as 'z' is: 76586589365091238788452954561582386286077551076029831532116762774483044874738
# the signe 'z' or just the sig is (in hex): 3045022100d1349394cd0d8fcf5e8e80035dfed9f020fd2086563d95b2933d2084d37c9eea02203bbea030d54c2cca5911dfb192b6f9c699471b2f69e6f8d9e195d35497559fb901
# the public key in sec format (hex) is: 03935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67
# now this looks like compressed sec format since it starts with 03, is the one
# starting with 04 that I figured out above the uncompressed sec format of this?

# combined shit:scrpt_sig+script_pubkey:
#3045022100d1349394cd0d8fcf5e8e80035dfed9f020fd2086563d95b2933d2084d37c9eea02203bbea030d54c2cca5911dfb192b6f9c699471b2f69e6f8d9e195d35497559fb901 03935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67 OP_DUP OP_HASH160 ee52b9449e861d89de31d212cb1a799489598b88 OP_EQUALVERIFY OP_CHECKSIG
# on stack of op_equalverify we have: 
# 0: 