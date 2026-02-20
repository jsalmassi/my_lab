from io import BytesIO #js
import socket
import struct
from network import SimpleNode, GetHeadersMessage, HeadersMessage
from block import Block, GENESIS_BLOCK, LOWEST_BITS
from helper import calculate_new_bits, encode_varint
##############
def hex_to_wire_hash(hash_hex):
    return bytes.fromhex(hash_hex)[::-1]

def my_get_headers(start_hash_hex, stop_hash_hex):
    payload  = struct.pack("<i", 70015)
    payload += encode_varint(1)
    payload += hex_to_wire_hash(start_hash_hex)
    payload += hex_to_wire_hash(stop_hash_hex)
    return payload

##########
# previous = Block.parse(BytesIO(GENESIS_BLOCK))
#stop_hash_wire = bytes.fromhex(stop_hash_hex)[::-1]

previous = Block.parse(BytesIO(bytes.fromhex('00000000000000000000be909ce3f23ac184ae2d583a5efa3e686311986adefb')))#933925
print('Starting from block:', previous.hash().hex())
#theStart = bytes.fromhex('00000000000000000000be909ce3f23ac184ae2d583a5efa3e686311986adefb')[::-1]
#theStop = bytes.fromhex('0000000000000000000035d9689c5ce036bb6f97b92ea87b49d23c525170ad56')[::-1]
Start = '00000000000000000000be909ce3f23ac184ae2d583a5efa3e686311986adefb'
Stop = '0000000000000000000035d9689c5ce036bb6f97b92ea87b49d23c525170ad56'

end_block = Block.parse(BytesIO(bytes.fromhex('0000000000000000000035d9689c5ce036bb6f97b92ea87b49d23c525170ad56')))#933929

#first_epoch_timestamp = previous.timestamp
expected_bits = LOWEST_BITS
count = 1
# node = SimpleNode('mainnet.programmingbitcoin.com', testnet=False)
# node = SimpleNode('195.201.246.33', testnet=True, logging=True)
node = SimpleNode('65.108.102.41', testnet=False, logging=True)
node.handshake()
# for _ in range(1):
for _ in range(1):
    # getheaders = ("getheaders", my_get_headers(previous.hash().hex(), end_block.hash().hex()))
    getheaders = ("getheaders", my_get_headers(Start, Stop))
    #getheaders = GetHeadersMessage(start_block=previous.hash(), end_block=end_block.hash())
    # node.send(getheaders)
    node.socket.sendall(getheaders)
    headers = node.wait_for(HeadersMessage)

    print('len(headers.blocks)',len(headers.blocks))
    # for header in headers.blocks:
    for header in headers.blocks[:5]:
        #print('Block #{}: {}'.format(count, header.hash().hex()))
        if not header.check_pow():
            raise RuntimeError('bad PoW at block {}'.format(count))
        """ if header.prev_block != previous.hash():
            raise RuntimeError('discontinuous block at {}'.format(count))
        if count % 2016 == 0:
            time_diff = previous.timestamp - first_epoch_timestamp
            expected_bits = calculate_new_bits(previous.bits, time_diff)
            print(expected_bits.hex())
            first_epoch_timestamp = header.timestamp
        if header.bits != expected_bits:
            raise RuntimeError('bad bits at block {}'.format(count)) """
        previous = header
        count += 1
        print('Block #{}: {}'.format(count, header.hash().hex()))
        #if __name__ == "__main__":
           ##
