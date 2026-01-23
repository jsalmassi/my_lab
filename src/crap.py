print("------------------------------------")
print('num = 12345 ')
num = 12345
print('hex(num): ',hex(num))
print('format(num,\'x\'): ',format(num,'x')) 
print('int(\'3039\',16): ',int('3039',16))
print("------------------------------------")
print('bytes.fromhex(\'3039\'): ',bytes.fromhex('3039')) # b'09'
print('num.to_bytes(2,\'little\'): ', num.to_bytes(2,'little')) #b'90'
print('int.from_bytes(b\'90\',\'little\'): ',int.from_bytes(b'90','little')) #12345
print('num.to_bytes(2,\'big\'): ',num.to_bytes(2,'big')) #b'09
print('int.from_bytes(b\'09\',\'big\'): ', int.from_bytes(b'09','big')) #12345

