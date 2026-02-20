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
print("------------------------------------")
print("------------------------------------")
print ('2**8 =', 2**8) # this is 256 which fits in 2 byte
print('n=256 ');n=256
print('n.to_bytes((n.bit_length()+7)//8,\'big\') =', n.to_bytes((n.bit_length()+7)//8,'big'))
print('n=2**16 or 65536'); n=2**16 # this is 65536 which fits in 3 bytes
print('n.to_bytes((n.bit_length()+7)//8,\'big\') =', n.to_bytes((n.bit_length()+7)//8,'big'))
#print('(2**16).to_bytes(( (2**16).bit_length()+7)//8,\'big\') =', (2**16).to_bytes(( (2**16).bit_length()+7)//8,'big'))
print ('2**32 =', 2**32) # this is 4,294,967,296 which fits in five bytes
print('m=2**32 or 4294967296'); m=2**32
print('m.to_bytes((m.bit_length()+7)//8,\'big\') =', m.to_bytes((m.bit_length()+7)//8,'big'))