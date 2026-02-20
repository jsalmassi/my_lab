
# SPV probe script
# This script connects to a Bitcoin testnet peer and probes its SPV support 
# by sending a filterload message followed by a getdata request for a merkleblock.
# It analyzes the peer's response to determine if SPV is supported, ignored, or rejected
####################### please read ########################
# To use this script, change the 'peer_ip' variable to the target peer's IP address.
# You can find testnet peers using DNS seeds or other methods.
# The script sends a filterload message to set up a bloom filter and then requests
# a merkleblock for a specific block hash. It waits for the peer's response and
# categorizes the SPV support based on the received messages or timeouts.
############################################################
# I have, for now, cocluded that the SPV support probe is very spotty at best.
# Some peers may not respond as expected, so results can vary.
# Experiment with different peers to see how they handle SPV requests.
############################################################    
# I have for now concluded that the SPV support is very spoty at best.
# I was not able to see completely how it works. Spent enough time and effort
# for now. I leave this here and maybe pick it back up later.
# I may even switch to what they say is better (more private) spv version
# called Nuetrino.


import socket, struct, hashlib, time
NODE_BLOOM = 1 << 2
MSG_TIMEOUT = 5  # seconds
TESTNET_MAGIC = 0x0709110B
#---- helpers----
def sha256d(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()
#---
def serialize_varint(i):
    if i < 0xfd:
        return struct.pack('B', i)
    elif i <= 0xffff:
        return b'\xfd' + struct.pack('<H', i)
    elif i <= 0xffffffff:
        return b'\xfe' + struct.pack('<I', i)
    else:
        return b'\xff' + struct.pack('<Q', i)
#---
def recv_exact(sock, n):
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("socket closed")
        data += chunk
    return data

def send_message(sock, command, payload=b''):
    assert len(command) <= 12

    command = command.ljust(12, b'\x00')
    length = len(payload)
    checksum = sha256d(payload)[:4]

    header = (
        struct.pack('<I', TESTNET_MAGIC) +
        command +
        struct.pack('<I', length) +
        checksum
    )

    sock.sendall(header + payload)
#---
def recv_message(sock):
    header = recv_exact(sock, 24)

    magic, = struct.unpack('<I', header[:4])
    if magic != TESTNET_MAGIC:
        raise ValueError("wrong network magic")

    command = header[4:16].rstrip(b'\x00')
    length, = struct.unpack('<I', header[16:20])
    checksum = header[20:24]

    payload = recv_exact(sock, length)

    if sha256d(payload)[:4] != checksum:
        raise ValueError("bad payload checksum")

    return command, payload
#---
def send_version(sock):
    version = 70015
    services = 0
    timestamp = int(time.time())

    addr_recv = b'\x00' * 26
    addr_from = b'\x00' * 26

    nonce = 0
    user_agent = b'\x00'
    start_height = 0
    relay = 0

    payload = (
        struct.pack('<iQQ', version, services, timestamp) +
        addr_recv +
        addr_from +
        struct.pack('<Q', nonce) +
        user_agent +
        struct.pack('<i?', start_height, relay)
    )

    send_message(sock, b'version', payload)
#---
def recv_version(sock):
    while True:
        cmd, payload = recv_message(sock)
        if cmd == b'version':
            return payload
#---
def send_verack(sock):
    send_message(sock, b'verack')

def recv_verack(sock):
    while True:
        cmd, _ = recv_message(sock)
        if cmd == b'verack':
            return
#---
def send_ping(sock, nonce):
    payload = struct.pack('<Q', nonce)
    send_message(sock, b'ping', payload)
def recv_ping(sock):
    while True:
        cmd, payload = recv_message(sock)
        if cmd == b'ping':
            return struct.unpack('<Q', payload)[0]    
#--
def recv_pong(sock):
    while True:
        cmd, payload = recv_message(sock)
        if cmd == b'pong':
            return struct.unpack('<Q', payload)[0]  
def send_pong(sock, nonce):
    payload = struct.pack('<Q', nonce)
    send_message(sock, b'pong', payload)                 
#---
def send_filterload(sock):
    filter_bytes = b'\x00' * 10
    hash_funcs = 3
    tweak = 0
    flags = 0

    payload = (
        serialize_varint(len(filter_bytes)) +
        filter_bytes +
        struct.pack('<I', hash_funcs) +
        struct.pack('<I', tweak) +
        struct.pack('B', flags)
    )

    send_message(sock, b'filterload', payload)
#---
MSG_MERKLEBLOCK = 2

def send_getdata_merkleblock(sock, block_hash_le):
    inv = struct.pack('<I', MSG_MERKLEBLOCK) + block_hash_le
    payload = serialize_varint(1) + inv
    send_message(sock, b'getdata', payload)
#----
#end helpers ----
#peer_ip = '116.202.225.152'  # change to target peer IP, this one works somewhat
peer_ip = '69.59.18.23'  # change to target peer IP
port = 18333  # testnet port
sock = socket.create_connection((peer_ip, port))#, timeout=10)
##sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##sock.connect((peer_ip, port))
sock.settimeout(10)

send_version(sock)
recv_version(sock)
send_verack(sock)
recv_verack(sock)

def probe_spv_support(sock, block_hash_le):
    #sock.settimeout(5)

    send_filterload(sock)
    send_getdata_merkleblock(sock, block_hash_le)

    try:
        while True:
            cmd, _ = recv_message(sock)

            if cmd == b'merkleblock':
                return "SPV_SUPPORTED"

            if cmd == b'block':
                return "SPV_IGNORED_FULL_BLOCK"
            #--- js
            if cmd in [b"inv", b"feefilter", b"sendheaders"]:
                print('ignoring command during SPV probe: {}'.format(cmd))
                continue   # ignore
            
            elif cmd == b'ping':
                # send pong
                #nonce = recv_pong(sock)
                nonce = struct.unpack('<Q', _)[0]
                send_pong(sock, nonce)
            #--- end js

    except socket.timeout:
        return "SPV_IGNORED_TIMEOUT"

    except ConnectionError:
        return "SPV_REJECTED"
    
# Example block hash (little-endian) to request
block_hash_le = bytes.fromhex('00000000000000001a2b770231f73a5b7ecad90ab08d5f948068687d95d225f2') #tsetnet last block 4839657
result = probe_spv_support(sock, block_hash_le[::-1])  # reverse to little-endian
print(f"SPV probe result for {peer_ip}: {result}")

#---- some testnet peers to try, I got these from DNS seeds by
# modifying the get_testnet_peer() function in my_get_seed.py
# and printing out all the found peers.
# You can try these IPs one by one by changing the peer_ip variable above.
"""
Testnet reachable peer is: 65.21.203.146
Testnet reachable peer is: 69.59.18.23
Testnet reachable peer is: 194.95.66.129
Testnet reachable peer is: 91.123.182.164
Testnet reachable peer is: 95.213.143.91
Testnet reachable peer is: 45.50.223.112
Testnet reachable peer is: 54.236.59.55
Testnet reachable peer is: 150.136.77.157
Testnet reachable peer is: 141.98.219.199
Testnet reachable peer is: 45.55.132.91
Testnet reachable peer is: 23.227.223.209
Testnet reachable peer is: 116.202.225.152 *
Testnet reachable peer is: 129.226.198.211
Testnet reachable peer is: 44.237.38.26
Testnet reachable peer is: 3.253.163.14
Testnet reachable peer is: 157.90.95.170
Testnet reachable peer is: 44.226.91.66
Testnet reachable peer is: 178.21.118.82
Testnet reachable peer is: 148.251.87.112
 """