import sys
print(sys.executable)
""" 
import importlib, sys
sys.path.append("/home/jsalmassi/my_projects/programmingbitcoin/code-ch08")
#hash160 = importlib.import_module('helper.hash160') # that did not work
#helper = importlib.import_module('helper')
script = importlib.import_module('script') 
p2pkh_script = script.p2pkh_script
from tests.test_tx import TxIn, TxOut, Tx """
from io import BytesIO
from script import Script
stream = BytesIO(bytes.fromhex('4d04ffff001d0104455468652054696d6573203033\
2f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64\
206261696c6f757420666f722062616e6b73'))
s = Script.parse(stream)
print(s.cmds[2])
print(s.cmds[1])
print (s)