# this needs to be run with python 2.7 at this point, simply right click on anywhere on this file in editor
# and select 'commnad pallet' and then find the 'Python: select interpreter', the active python interpreter is shown
# on the bottome of this IED's status line.

import ecdsa
##import hashlib
##import struct
import unittest
import keyUtils
##import txnUtils
##import utils
##import os
import sys

""" # ensure the local project directory is on sys.path so local modules like ecc can be imported
# sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname('/home/jsalmassi/my_projects/programmingbitcoin/code-ch05/ecc.py'))
import ecc """

import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch05")
my_ecc = importlib.import_module('ecc')
S256Point = my_ecc.S256Point
Signature = my_ecc.Signature

""" from my_ecc import (
    S256Point,
    Signature,
) """

my_sig = '3045022100d1349394cd0d8fcf5e8e80035dfed9f020fd2086563d95b2933d2084d37c9eea02203bbea030d54c2cca5911dfb192b6f9c699471b2f69e6f8d9e195d35497559fb901'
public_key = '04935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b673296fb8e372dec2f72836d46f17abd994218feefccefd89b6a3dc2b2da9a6375'

def verify_sig_procedural(my_sig, public_key):
    sig = keyUtils.derSigToHexSig(my_sig[:-2]) # this take the DER sig stuff out and returns the raw r and s concatenated hex string
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=ecdsa.SECP256k1)
    hashToSign = 'a952793354e9299436ae91c1cc4f6f0ba666510856df186e4e8929193e6f39f2'
    return vk.verify_digest(bytes.fromhex(sig), bytes.fromhex(hashToSign ))
assert(verify_sig_procedural(my_sig, public_key))

print ('are we good doing it procedurally (none object orineted)? ....... yes we are good    ')
####################################################################################
# now that we have verified the signature using the public key from the txn above,
# I am gonna verify the signature using bitconprgammingbook's objects and functions
print('****************************************************************************')
def verify_sig_oop(my_sig, public_key):
    """ Verify a DER-encoded signature against the given public key using OOP approach. """
    z = 0xa952793354e9299436ae91c1cc4f6f0ba666510856df186e4e8929193e6f39f2
    try:
        point = S256Point.parse(bytes.fromhex(public_key))
        sig = Signature.parse(bytes.fromhex(my_sig[:-2]))  # it take a DER signature less the hashtype byte at the end
    except (ValueError, SyntaxError) as e:
        print("Failed to parse sec_pubkey or der_signature:", e )
        return False
    return point.verify(z, sig)  # removing the last byte which is the hashtype
assert(verify_sig_oop(my_sig, public_key))
print ('are we good doing it oop (object oriented programming)?  ....**.... yes we are good ')
""" z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
#hashToSign = bytes.fromhex('7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d')
try:
    point = S256Point.parse(bytes.fromhex(public_key))
    sig = Signature.parse(bytes.fromhex(my_sig[:-2]))  # it take a DER signature less the hashtype byte at the end
except (ValueError, SyntaxError) as e:
    print("Failed to parse sec_pubkey or der_signature:", e )
if point.verify(z, sig):  # removing the last byte which is the hashtype
   print("Success: signature is correct!")
else:
    print("Failure: signature is wrong!")  """
class TestMy_verify_sig(unittest.TestCase):

    def test_verify_sig_oop(self):
        """Test verify_sig_oop(my_sig, public_key)"""
        self.assertEqual(verify_sig_oop(my_sig, public_key), True)
        print('OOP signature verification passed.')
        #self.fail('Not implemented')

    def test_verify_sig_procedural(self):
        """Test verify_sig_procedural(my_sig, public_key)"""
        self.assertEqual(verify_sig_procedural(my_sig, public_key), True)
        print('Procedural signature verification passed.')
        #self.fail('Not implemented')

if __name__ == '__main__':
    unittest.main()