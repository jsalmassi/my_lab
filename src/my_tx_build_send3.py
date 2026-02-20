
from ecc import PrivateKey
from helper import decode_base58, SIGHASH_ALL

import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/pybitcointools/cryptos")
segwit_addr = importlib.import_module('segwit_addr')
##import bech32_addr_conversion # very interesting, by importing this file it gets "run"
# but I dont want to import the bech32_addr_conversion file, because I use the 
# segwit_addr code from pybitcointools to do the same thing, which is more concise and easier to use.
sys.path.append("/home/jsalmassi/my_projects/my_lab")
# sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch07")
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch13")
#hash160 = importlib.import_module('helper.hash160') # that did not work
#helper = importlib.import_module('helper')
script = importlib.import_module('script') 
#from script import p2pkh_script
p2pkh_script = script.p2pkh_script

# from tests.test_tx import TxIn, TxOut, Tx
from tx import Tx, TxIn, TxOut

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
# next I am using the segit address decoding code from the pybitcointools library to decode the segwit address I have,
#  which is the change address in this case, to get the witness version and witness program,
#  which will be used in the witness script of the input of the transaction object.
# note that I could have used the bech32_addr_conversion code to do the same thing,
#  but I just want to test the segwit_addr code from pybitcointools, which is more concise and easier to use.
# decode_segwit_address(hrp: tb1, addr: Optional[str])
# decoded_segwit_addr = segwit_addr.decode_segwit_address("tb", "tb1qq82ajthl5mlm50h6x70esvxs7atp3vfnjwp8z5kjdepsjqqw3zcsj5rufw")
decoded_segwit_addr = segwit_addr.decode_segwit_address("tb", "tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg")
print('version is: ',decoded_segwit_addr[0])
print("decoded_segwit_addr",decoded_segwit_addr[1]) # this is the same as h160, which is the same as the
# witness program, which is the same as the hash160 of the public key
h160a = decoded_segwit_addr[1]  
print('witness_script is: ',bytes(decoded_segwit_addr[1]).hex())
# we do the same for change address, which is also a segwit address
decoded_segwit_addr2 = segwit_addr.decode_segwit_address("tb", "tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c")
print('version is: ',decoded_segwit_addr2[0])
print("decoded_segwit_addr2",decoded_segwit_addr2[1]) # this is the same as h160, which is the same as the
# witness program, which is the same as the hash160 of the public key
h160b = decoded_segwit_addr2[1]  
print('witness_script is: ',bytes(decoded_segwit_addr2[1]).hex())

########
# I received some sats in the newly generated single-sig p2wpkh wallet at the address
#  tb1qulcfyq9arwn45fjjag5dwyy8u3wze2mw046r5g, and I want to spend those coins in a transaction that sends some of the coins to the 
# target address: tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg
#  and the rest back to the change address: tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c
# , which is also a segwit address all on the same wallet.
# next is the pervious transaction where I received the coins, which will be used as the input of the transaction I am going to create.
prev_tx = bytes.fromhex('6b570a95f115b5ea884b32e17e1c1422470572e71cd67c2709f35cfdcb4e1439')
prev_index = 1 # the index of the output in the previous transaction that I received the coins in, which will be used as the input of the transaction I am going to create.
# next is the private key corresponding to the address I received the coins in, which will be used to sign the transaction I am going to create.
# priv = 'p2wpkh:cNM78qTBgM99a1Gs1VvG7sajPoGU1cVeE3dBs1MoQeY69VTdVo53' # i dont think I need the p2wpkh: prefix, which is just for the bech32 address,
#  but I can just use the WIF format of the private key, which is KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rdcJfsz6iB4Q,
#  which I can get by doing priv.wif(compressed=True, testnet=True)    
priv = 'cNM78qTBgM99a1Gs1VvG7sajPoGU1cVeE3dBs1MoQeY69VTdVo53'

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
target_address= 'tb1qmgfr28hxq2p76ymjw8v9ag2lsdqfl8vewe4twg' # 

target_amount = 36000
# I useded the following to get my address and the change address, I alerady have the funds here
# from the previouls tx whose id is the avove one
# my_address = print(priv.point.address(compressed=True, testnet=True)) # which would also be the change address
# did the above in the python shell to get my change address which is our own address
change_address = 'tb1qfuwdkf0lr8dvtn9d3za6rg2cg2s88tmggjsq6c'
change_amount = 100000
# fee would be 138616-(100000+36000)=2616 satoshis

tx_ins = []
tx_ins.append(TxIn(prev_tx, prev_index))
tx_outs = []
#h160 = decode_base58(target_address)
#script_pubkey = p2pkh_script(h160)
#script_pubkey = script.p2wpkh_script(bytes.fromhex('da12351ee60283ed137271d85ea15f83409f9d99'))#(witness_program)


# script_pubkey = script.p2wpkh_script(h160a)# same as h160, which is the same as the witness program, which is the same as the hash160 of the public key
script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr[1]))# same as h160, which is the same as the witness program, which is the same as the hash160 of the public key
print('script_pubkey for target address is: ', script_pubkey.serialize().hex())

#h160aBytes = bytes(h160a)
#print('h160aBytes is: ', h160aBytes.hex())


target_satoshis = int(target_amount)
tx_outs.append(TxOut(target_satoshis, script_pubkey))


#h160 = decode_base58(change_address)
#script_pubkey = p2pkh_script(h160)

# script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr2[1]))#(witness_program)
script_pubkey = script.p2wpkh_script(bytes(decoded_segwit_addr2[1]))#(witness_program)
print('script_pubkey for change address is: ', script_pubkey.serialize().hex())

change_satoshis = int(change_amount)
tx_outs.append(TxOut(change_satoshis, script_pubkey))
tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True, segwit=True)

import my_wif2priv_conv as wif2priv

#tx_obj.verify_input(0) # this will return True if the input is valid, which means the signature is correct and the scriptPubKey is correct, otherwise it will return False

# print(tx_obj.sign_input(0, priv))
print(tx_obj.sign_input(0, wif2priv.sk.to_string())) # .wif_to_privkey(priv)))
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