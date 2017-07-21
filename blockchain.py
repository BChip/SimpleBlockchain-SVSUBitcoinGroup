import hashlib as hasher
import datetime as date
import time

HASH_TARGET = "0000"

class Block:

    def __init__(self, index, timestamp, data, previous_hash, nonce):
        self.solved = False
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        if nonce:
            hash = self.hash_block(nonce)
            if hash:
                self.hash = hash
        elif data == "Genesis Block":
            self.hash = self.hash_genesis()
        else:
            return

    def hash_block(self, nonce):
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(nonce))
        hash = sha.hexdigest()
        if hash.startswith(HASH_TARGET):
            return hash
        return None

    def hash_genesis(self):
        nonce = 0
        while not self.solved:
            sha = hasher.sha256()
            sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(nonce))
            hash = sha.hexdigest()
            nonce += 1
            if hash.startswith(HASH_TARGET):
                self.solved = True
                return hash
        return

class Blockchain:

    def __init__(self):
        self.blockchain = [self.create_genesis_block()]
        self.previous_block = self.blockchain[0]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0", None)

    def next_block(self, last_block, timestamp, data, nonce):
        index = last_block.index + 1
        if nonce:
            return Block(index, timestamp, data, last_block.hash, nonce)
        else:
            return Block(index, timestamp, data, last_block.hash, nonce)

    def add(self, data, nonce=None, timestamp = date.datetime.now()):
        if nonce:
            block_to_add = self.next_block(self.previous_block, timestamp, data, nonce)
            if block_to_add.hash:
                self.blockchain.append(block_to_add)
                self.previous_block = block_to_add
                print "success!"
        else:
            return self.next_block(self.previous_block, timestamp, data, nonce)

    def get(self, index):
        return self.blockchain[index]

    def getChain(self):
        return self.blockchain










blockchain = Blockchain()
num_of_blocks_to_add = 1

addBlock = blockchain.add("yo")
if addBlock:
    sha = hasher.sha256()
    solved = False
    nonce = 0

    while not solved:
        sha = hasher.sha256()
        sha.update(str(addBlock.index) + str(addBlock.timestamp) + str(addBlock.data) + str(addBlock.previous_hash) + str(nonce))
        hash = sha.hexdigest()
        if hash.startswith(HASH_TARGET):
            solved = True
            blockchain.add(addBlock.data, nonce, addBlock.timestamp)
        nonce += 1

chain = blockchain.getChain()
for block in chain:
    print block.data
