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

# my_sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')
my_sig = '3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601'
# public_key = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
public_key = '04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34'

def verify_sig_procedural(my_sig, public_key):
    sig = keyUtils.derSigToHexSig(my_sig[:-2]) # this take the DER sig stuff out and returns the raw r and s concatenated hex string
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=ecdsa.SECP256k1)
    hashToSign = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
    return vk.verify_digest(bytes.fromhex(sig), bytes.fromhex(hashToSign ))
assert(verify_sig_procedural(my_sig, public_key))
""""
sig = keyUtils.derSigToHexSig(my_sig[:-2]) # this take the DER sig stuff out and returns the raw r and s concatenated hex string
#### long_sig = keyUtils.derSigToHexSig(parsed[1][:-2])
#### sig = long_sig[8:]  # removing the first 8 chars which are '30450220' which is part of DER encoding]  
print ('derSigToHexSig is: ',sig)
vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=ecdsa.SECP256k1)
## hashToSign = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
hashToSign = '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d'
assert(vk.verify_digest(bytes.fromhex(sig), bytes.fromhex(hashToSign )))
"""

print ('are we good doing it procedurally (none object orineted)? ....... yes we are good    ')
####################################################################################
# now that we have verified the signature using the public key from the txn above,
# I am gonna verify the signature using bitconprgammingbook's objects and functions
print('****************************************************************************')
def verify_sig_oop(my_sig, public_key):
    """ Verify a DER-encoded signature against the given public key using OOP approach. """
    z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
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