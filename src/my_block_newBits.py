# Exercise 12
import importlib, sys
sys.path.insert(0, '/home/jsalmassi/my_projects/programmingbitcoin/code-ch09')
block = importlib.import_module('block')
helper = importlib.import_module('helper')

from io import BytesIO
from block import Block
from helper import target_to_bits, TWO_WEEKS

block1_hex = '000000203471101bbda3fe307664b3283a9ef0e97d9a38a7eacd8800000000000000000010c8aba8479bbaa5e0848152fd3c2289ca50e1c3e58c9a4faaafbdf5803c5448ddb845597e8b0118e43a81d3'
block2_hex = '02000020f1472d9db4b563c35f97c428ac903f23b7fc055d1cfc26000000000000000000b3f449fcbe1bc4cfbcb8283a0d2c037f961a3fdf2b8bedc144973735eea707e1264258597e8b0118e5f00474'

# parse both blocks
# get the time differential
# if the differential > 8 weeks, set to 8 weeks
# if the differential < 1/2 week, set to 1/2 week
# new target is last target * differential / 2 weeks
# convert new target to bits
# print the new bits hex
block1 = Block.parse(BytesIO(bytes.fromhex(block1_hex)))
block2 = Block.parse(BytesIO(bytes.fromhex(block2_hex)))
time_differential = block2.timestamp - block1.timestamp
if time_differential > TWO_WEEKS * 4:
    time_differential = TWO_WEEKS * 4
if time_differential < TWO_WEEKS // 4:
    time_differential = TWO_WEEKS // 4
old_target = helper.bits_to_target(block1.bits)
new_target = old_target * time_differential // TWO_WEEKS
new_bits = target_to_bits(new_target)
print(new_bits.hex())
print(block1.bits.hex() 
      , block2.bits.hex()   )