import hashlib as hasher
import datetime as date
from multiprocessing.pool import ThreadPool
import time

pool = ThreadPool(8)

class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.solved = False
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        l = pool.map_async(self.hash_block, [0,100000,1000000,10000000,100000000, 105000000]).get()
        if l[0]:
            self.hash = l[0]
        elif l[1]:
            self.hash = l[1]
        elif l[2]:
            self.hash = l[2]
        elif l[3]:
            self.hash = l[3]
        elif l[4]:
            self.hash = l[4]


    def hash_block(self, nonce):
        sha = hasher.sha256()
        while not self.solved:
            sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(nonce))
            hash = sha.hexdigest()
            nonce += 1
            if hash.startswith("000000"):
                self.solved = True
                print hash, nonce
                return hash
        return

class Blockchain:

    def __init__(self):
        self.blockchain = [self.create_genesis_block()]
        self.previous_block = self.blockchain[0]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def next_block(self, last_block, data):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = data
        this_hash = last_block.hash
        return Block(this_index, this_timestamp, this_data, this_hash)

    def add(self, data):
        block_to_add = self.next_block(self.previous_block, data)
        self.blockchain.append(block_to_add)
        self.previous_block = block_to_add

    def get(self, index):
        return self.blockchain[index]

    def returnChain(self):
        return self.blockchain

blockchain = Blockchain()
num_of_blocks_to_add = 2

for i in range (1, num_of_blocks_to_add):
    blockchain.add(date.datetime.now())

b = blockchain.returnChain()
for block in b:
    print block.hash
