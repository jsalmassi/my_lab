import socket
import random
from sys import argv
DNS_SEEDS_MAINNET = [
    "seed.bitcoin.sipa.be",
    "dnsseed.bluematt.me",
    "dnsseed.bitcoin.dashjr.org",
    "seed.bitcoinstats.com",
    "seed.bitcoin.jonasschnelli.ch",
    "seed.btc.petertodd.org",
    "seed.bitcoin.sprovoost.nl",
    "dnsseed.emzy.de",
    "seed.bitcoin.wiz.biz",
]
DNS_SEEDS_TESTNET = [
    "testnet-seed.bitcoin.jonasschnelli.ch",
    "seed.tbtc.petertodd.org",
    "seed.testnet.bitcoin.sprovoost.nl",
    "testnet-seed.bluematt.me",
]
PORT_TESTNET = 18333
PORT_MAINNET = 8333

def get_mainnet_peers(max_peers=50):
    peers = set()

    for seed in DNS_SEEDS_MAINNET:
        try:
            infos = socket.getaddrinfo(
                seed,
                PORT_MAINNET,
                type=socket.SOCK_STREAM
            )
            for info in infos:
                ip = info[4][0]
                peers.add(ip)
        except socket.gaierror:
            continue

    peers = list(peers)
    random.shuffle(peers)
    return peers[:max_peers]

def get_testnet_peer(max_peers=50):
    peers = set()

    for seed in DNS_SEEDS_TESTNET:
        try:
            infos = socket.getaddrinfo(
                seed,
                PORT_TESTNET,
                type=socket.SOCK_STREAM
            )
            for info in infos:
                ip = info[4][0]
                peers.add(ip)
        except socket.gaierror:
            continue

    peers = list(peers)
    random.shuffle(peers)
    return peers[:max_peers]
    """     #testnet_list = []
    for seed in DNS_SEEDS_TESTNET:
        
        try:
            infos = socket.getaddrinfo(seed, PORT_TESTNET, type=socket.SOCK_STREAM)
            random.shuffle(infos)
            for info in infos:
                print(f"Found testnet peer {info[4][0]}")
                return info[4][0]
                #testnet_list.append(info[4][0])

        except socket.gaierror:
            continue
        
    raise RuntimeError("No testnet peers found")
                """
if __name__ == "__main__":
        """ if argv[1] == "mainnet":
            print(" the argument is ",argv[1])
            mainnet_peers = get_mainnet_peers()
            for peer in mainnet_peers:
                print(f"Mainnet peer: {peer}")
        else :
            print(" argument is :",argv[1])
            my_testnet_peer = get_testnet_peer()
            for testnet_peer in my_testnet_peer:
                if (nc -vz 93.104.254.235 18333):
                    print(f"Testnet peer is: {testnet_peer}")   """
        if len(argv) < 2:
            print("Usage: script.py [mainnet|testnet]")
        elif argv[1] == "mainnet":
            print(" the argument is ", argv[1])
            mainnet_peers = get_mainnet_peers()
            for peer in mainnet_peers:
                print(f"Mainnet peer: {peer}")
        else :
            print(" argument is :", argv[1])
            my_testnet_peers = get_testnet_peer()
            for testnet_peer in my_testnet_peers:
                try:
                    with socket.create_connection((testnet_peer, PORT_TESTNET), timeout=3):
                        print(f"Testnet reachable peer is: {testnet_peer}")
                except Exception:
                    print(f"Could not connect to testnet peer: {testnet_peer}")