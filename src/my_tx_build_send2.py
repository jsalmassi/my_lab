
from ecc import PrivateKey
from helper import decode_base58, SIGHASH_ALL

import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch07")
#hash160 = importlib.import_module('helper.hash160') # that did not work
#helper = importlib.import_module('helper')
script = importlib.import_module('script') 
#from script import p2pkh_script
p2pkh_script = script.p2pkh_script
from tests.test_tx import TxIn, TxOut, Tx

cache_file = '/home/jsalmassi/my_projects/my_lab/tx.cache'  #js



# Create 2 TxIns, 1 from the Exercise 4 and 1 from a testnet faucet
# Creat 1 TxOut to the address above
target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'

# get the private key from the exercise in Chapter 4

# get the prev_tx and prev_index from the transaction where you got
# some testnet coins
# create the first transaction input with the default ScriptSig and
# sequence
# get the prev_tx and prev_index from the transaction in Exercise 4
# create the second transaction input with the default ScriptSig and
# sequence

# set the fee to some reasonable amount
# target amount should be the sum of the inputs - fee

# create a transaction output for the amount and address

# sign the first input using the private key
# sign the second input using the private key 
# print the transaction's serialization in hex
##################################################

prev_tx1 = bytes.fromhex('ed79275562a29afdb6dc50616e38e278537b6263d744fc09d594c842648b3cfa') #from a testnet faucet
prev_index1 = 0
prev_tx2 = bytes.fromhex('bfb1ca5a408a91dbd1ae1fd0102ad7b00976d40d7d7ab426546b388103df9542') # 100000 satoshis from wallet on legacy elctrum
# on pc side called default wallet
prev_index2 = 1

secret = 8675309
priv = PrivateKey(secret=secret)

# the follwing is what I have done:
# worked out the public key in uncompressed sec format (hex) to be:
#priv.point.sec(compressed=False).hex() # here is went wrong, when I used compressed=False, becuase the 
# '04935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b673296fb8e372dec2f72836d46f17abd994218feefccefd89b6a3dc2b2da9a6375'
# but I need compressed sec format for the tx above.

## public key in the tx above is in compressed format by default.
# priv.point.sec(compressed=True).hex() :
# '03935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67'
# the next line is for my own address, note it is compressed sec format
#priv.point.address(compressed=True,testnet=True):
# 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
# so now after 2 sends to this address, the balance is 160000 satoshis+100000 satoshis = 260000 satoshis


# also worked the private key in WIF format to be 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rdcJfsz6iB4Q'
# by doing: priv.wif(compressed=True, testnet=True)
#------ above is just notes to myself ----------------------
target_address= 'mgTFdsFv2MsbeGXEsnoDBsNTcGTGQ6rSe4' # this is the 3rd address on the electurm-legacy wallet

target_amount = 200000
# I useded the following to get my address and the change address, I alerady have the funds here
# from the previouls tx whose id is the avove one
# my_address = print(priv.point.address(compressed=True, testnet=True)) # which would also be the change address
# did the above in the python shell to get my change address which is our own address
change_address = 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'
change_amount = 60000
# fee would be 270000 -(200000+60000)=10000satoshis

tx_ins = []
tx_ins.append(TxIn(prev_tx1, prev_index1))
tx_ins.append(TxIn(prev_tx2, prev_index2))
tx_outs = []
h160 = decode_base58(target_address)
script_pubkey = p2pkh_script(h160)
#target_satoshis = int(target_amount*100000000)
target_satoshis = int(target_amount)
tx_outs.append(TxOut(target_satoshis, script_pubkey))
h160 = decode_base58(change_address)
script_pubkey = p2pkh_script(h160)
# change_satoshis = int(change_amount*100000000)
change_satoshis = int(change_amount)
tx_outs.append(TxOut(change_satoshis, script_pubkey))
tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
print(tx_obj.sign_input(0, priv))
print(tx_obj.sign_input(1, priv))
print(tx_obj.serialize().hex())
# the tx id is:'816eefd27181cde026bde29115f658d2adabd236f35cf9ec721fe6022b88b5b3'
# go this going to legacy electrum wallet on testnet and using the 'Tools/Load Transaction/From Hex'
# paste the above hex serialization in there and click ok
# then go to the 'History' tab and right click on the transaction and choose 'Details'
# you will see the details of the transaction including the tx id above