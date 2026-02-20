
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

prev_tx = bytes.fromhex('c64256f081e5347526e531f3ed803887ece4e64bf5881ce2c14a03fb835d4407')
prev_index = 0

#secret = 8675309
#priv = PrivateKey(secret=secret)
priv = 'cVtxe9txC8fDyqYKSvNmfHeDWoSrzLAm9g7T8iWJSunGhXSSbYgX'

# the follwing is what I have done:
# worked out the public key in uncompressed sec format (hex) to be:
#priv.point.sec(compressed=False).hex() # here is went wrong, when I used compressed=False, becuase the 
# public key in the tx above is in compressed format by default.
# '04935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b673296fb8e372dec2f72836d46f17abd994218feefccefd89b6a3dc2b2da9a6375'

# priv.point.sec(compressed=True).hex()
#: '03935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67'

#priv.point.address(compressed=True,testnet=True)
#: 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'

#priv.point.address(compressed=False,testnet=True)
#: 'n3F6DTFFunQZELpeYvmUCpGcR4D5QYbKFR'

# also worked the private key in WIF format to be 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rdcJfsz6iB4Q'
# by doing: priv.wif(compressed=True, testnet=True)
#------ above is just notes to myself ----------------------
target_address= 'mqvq3n4SUuCbT1bnVRdTn7DcCX2NXjNnPS' # 

target_amount = 10000
# I useded the following to get my address and the change address, I alerady have the funds here
# from the previouls tx whose id is the avove one
# my_address = print(priv.point.address(compressed=True, testnet=True)) # which would also be the change address
# did the above in the python shell to get my change address which is our own address
change_address = 'tb1q353vk66k4n5e02xjg70rts0ujrdt792y0yr8ccez6303wrydaldswp69mj'
change_amount = 76000
# fee would be 88600-(10000+76000)=2600 satoshis

#mopVkxp8UhXqRYbCYJsbeE1h1fiF64jcoH
######priv = decode_base58('cUovB5YGerNeAoWh4aG5zaSXVXiBuCERXCwxwbXj83rmLMFLcXHN')# this is the WIF private key I got from the electrum wallet
###### corresponding to the 3 address in that wallet ###
###### or I may have to do: decode_base58(...).hex()?

tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))
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
print(tx_obj.serialize().hex())
################################################
# I just grabbed this pair of address and private key from the electrum wallet 4.7,
#  and I have some testnet coins in that address, so I can use that to test the code above.
#  I will also use the change address from that wallet, which is generated from the
# same private key, so I can be sure that I have the correct private key and addresses.
#tb1qfamdt3nrsrg8rze5xnv7ek2mn4tx9pl77ktpgfsj4268a6wkwmeq693pl9 #this has 88600 sats
#p2wsh:p2wsh:cVtxe9txC8fDyqYKSvNmfHeDWoSrzLAm9g7T8iWJSunGhXSSbYgX

# this is the change address: just a differnt address from the same wallet:
#tb1q353vk66k4n5e02xjg70rts0ujrdt792y0yr8ccez6303wrydaldswp69mj

# using the target address of Electrum 4.5.8 default_wallet:
#mqvq3n4SUuCbT1bnVRdTn7DcCX2NXjNnPS