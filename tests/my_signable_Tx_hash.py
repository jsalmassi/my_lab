import unittest

## js
# the next lines will make the modues in /home/jsalmassi/my_projects/programmingbitcoin/code-ch07avaiable 
# to this script, since that file lives outside of my_lab package.
import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch07")
#hash160 = importlib.import_module('helper.hash160') # that did not work
helper = importlib.import_module('helper')
script = importlib.import_module('script')
theTx = importlib.import_module('tx')
#from theTx import TxFetcher
TxFetcher = theTx.TxFetcher
sys.path.append("/home/jsalmassi/my_projects/pybitcointools/cryptos")
ripemd160 = importlib.import_module('ripemd')

import keyUtils
import base58
# assign names from the dynamically imported helper module so linters and runtime can resolve them
##encode_varint = helper.encode_varint
hash256 = helper.hash256
""" 
int_to_little_endian = helper.int_to_little_endian
little_endian_to_int = helper.little_endian_to_int
read_varint = helper.read_varint
SIGHASH_ALL = helper.SIGHASH_ALL
#from script import Script
 """
# end js
# this is a file that implements and tests for transaction signature hashing
# we declare this tx here globally so that all tests can use it
theTx = TxFetcher.fetch('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
##theTx = '0100000001a97830933769fe33c6155286ffae34db44c6b8783a2d8ca52ebee6414d399ec3000000008a47304402202c2e1a746c556546f2c959e92f2d0bd2678274823cc55e11628284e4a13016f80220797e716835f9dbcddb752cd0115a970a022ea6f2d8edafff6e087f928e41baac014104392b964e911955ed50e4e368a9476bc3f9dcc134280e15636430eb91145dab739f0d68b82cf33003379d885a0b212ac95e9cddfd2d391807934d25995468bc55ffffffff02015f0000000000001976a914c8e90996c7c6080ee06284600c684ed904d14c5c88ac204e0000000000001976a914348514b329fda7bd33c7b2336cf7cd1fc9544c0588ac00000000'
#----------------------------------------
# next parse a txn into its components came directly from txnUtils.py 
# Returns [first, sig, pub, rest]

def parseTxn(txn):
    first = txn[0:41*2]
    scriptLen = int(txn[41*2:42*2], 16)
    script = txn[42*2:42*2+2*scriptLen]
    sigLen = int(script[0:2], 16)
    sig = script[2:2+sigLen*2]
    pubLen = int(script[2+sigLen*2:2+sigLen*2+2], 16)
    pub = script[2+sigLen*2+2:]
            
    assert(len(pub) == pubLen*2)
    rest = txn[42*2+2*scriptLen:]
    return [first, sig, pub, rest]         

def makeSignableTx(tx, input_index):
    parsed = parseTxn(tx)
    first, sig, pub, rest = parsed
    inputAddr = base58.b58decode_check(keyUtils.pubKeyToAddr(pub))
    # for some reason inputaddr has 2 extra bytes in the begining. so we skip them, 2 zero
    print("inputAddr is:"+inputAddr[1:].hex())
    print("singableTxn in getSingableTxn is: " + first + "1976a914" + inputAddr[1:].hex() + "88ac" + rest + "01000000") 
    #return first + "1976a914" + inputAddr[1:].hex() + "88ac" + rest + "01000000"
    signableTxn = first + "1976a914" + inputAddr[1:].hex() + "88ac" + rest + "01000000"
    signableTxn_bytes = bytes.fromhex(signableTxn)
    h256 = hash256(signableTxn_bytes) 
    return int.from_bytes(h256, 'big') #very interesting, we have to return an int here to match the oop version
    # and that is why in the test we have to convert the expected value to int too. whereas, we could return bytes here
    # and compare bytes in the test. So they both ways work, but I try to be consistent with the oop version.
    #return h256
class TestSignableTx(unittest.TestCase):
    """ def test_make_signable_tx(self):
        from my_tx import Tx, TxIn, TxOut
        from my_script import Script
        # Create a sample transaction
        tx_in = TxIn(
            prev_tx=b'\x00' * 32,
            prev_index=0,
            script_sig=Script([b'some_signature', b'some_pubkey']),
            sequence=0xffffffff
        )
        tx_out = TxOut(
            amount=1000,
            script_pubkey=Script([b'some_pubkey_hash'])
        )
        tx = Tx(
            version=1,
            tx_ins=[tx_in],
            tx_outs=[tx_out],
            locktime=0
        )

        # Make the signable transaction
        signable_tx = makeSignableTx(tx, 0)

        # Check that the script_sig of the input is set to the previous output's scriptPubKey
        self.assertEqual(signable_tx.tx_ins[0].script_sig, tx_out.script_pubkey)

        # Check that other inputs (if any) have empty script_sigs
        for i, tx_in in enumerate(signable_tx.tx_ins):
            if i != 0:
                self.assertEqual(tx_in.script_sig, b'')
    """
   
    def test_sig_hash(self):
            want = int('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6', 16)
            # self.assertEqual(tx.sig_hash(0), want);print('test_sig_hash passed')
            self.assertEqual(theTx.sig_hash(0), want);print('test_sig_hash passed')
            #self.assertEqual(tx.makeSignableTx_oop(0), want)
    # this next (commented out) test works with test_sig_hash,before I modified makeSignableTx to return the hash directly
    # (after making an int from the hash bytes), I did this to match the way the object oriented version does it.
    """ def test_make_signable_tx(self):
            txn2_serialized = txn2.serialize().hex()
            print("txn2_serialized is: "+ txn2_serialized)
            want = '0100000001a97830933769fe33c6155286ffae34db44c6b8783a2d8ca52ebee6414d399ec3000000001976a914167c74f7491fe552ce9e1912810a984355b8ee0788acffffffff02015f0000000000001976a914c8e90996c7c6080ee06284600c684ed904d14c5c88ac204e0000000000001976a914348514b329fda7bd33c7b2336cf7cd1fc9544c0588ac0000000001000000'
            self.assertEqual(makeSignableTx(txn2.serialize().hex(), 0), want);print('test_make_signable_tx passed') """ 

    def test_make_signable_tx3(self):
            txn3_serialized = theTx.serialize().hex()
            print("txn3_serialized is: "+ txn3_serialized)
            want = int('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6', 16)
            #want = bytes.fromhex('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6')
            self.assertEqual(makeSignableTx(theTx.serialize().hex(), 0), want);print('test_make_signable_tx passed') 

if __name__ == '__main__':
    unittest.main()


