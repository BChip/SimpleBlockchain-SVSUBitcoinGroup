import hashlib as hasher
import datetime as date
import time

HASH_TARGET = "00000"

class Block:

    #nonce is a 32-bit field (32 leading zeros in hash target)
    #hash is 64-bit field
    def __init__(self, index, timestamp, data, previousHash, nonce):
        self.solved = False
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        if nonce:
            hash = self.verifyBlock(nonce)
            if hash:
                self.hash = hash
        elif index == 0:
            self.hash = self.hashGenesis()
        else:
            return

    def verifyBlock(self, nonce):
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previousHash) + str(nonce))
        hash = sha.hexdigest()
        if hash.startswith(HASH_TARGET):
            return hash
        return None

    def hashGenesis(self):
        nonce = 0
        while not self.solved:
            sha = hasher.sha256()
            sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previousHash) + str(nonce))
            hash = sha.hexdigest()
            nonce += 1
            if hash.startswith(HASH_TARGET):
                self.solved = True
                return hash
        return

class Chain:

    def __init__(self):
        self.blockchain = [self.createGenesisBlock()]
        self.previousBlock = self.blockchain[0]

    def createGenesisBlock(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0", None)

    def nextBlock(self, last_block, timestamp, data, nonce):
        index = last_block.index + 1
        return Block(index, timestamp, data, last_block.hash, nonce)

    def add(self, data, nonce=None, timestamp = None):
        if nonce:
            blockToAdd = self.nextBlock(self.previousBlock, timestamp, data, nonce)
            if blockToAdd.hash:
                self.blockchain.append(blockToAdd)
                self.previousBlock = blockToAdd
        else:
            return self.nextBlock(self.previousBlock, date.datetime.now(), data, nonce)

    def get(self, index):
        return self.blockchain[index]

    def getChain(self):
        return self.blockchain


######## CLIENT ########
def add(data, chain):
    addBlock = chain.add(data)
    if addBlock:
        hash(addBlock, chain)

def hash(block, chain):
    sha = hasher.sha256()
    solved = False
    nonce = 0

    while not solved:
        sha = hasher.sha256()
        sha.update(str(block.index) + str(block.timestamp) + str(block.data) + str(block.previousHash) + str(nonce))
        hash = sha.hexdigest()
        if hash.startswith(HASH_TARGET):
            solved = True
            chain.add(block.data, nonce, block.timestamp)
        nonce += 1


####### MAIN #######
devChain = Chain()
prodChain = Chain()

add("This is my developer chain dawg!", devChain)
add("Rockin on the prod chain!!!!", prodChain)
add("SVSU Rulez", prodChain)

for block in devChain.getChain():
    print(block.index, block.data, block.timestamp, block.hash)
print("---------------------------------------------------------")
for block in prodChain.getChain():
    print(block.index, block.data, block.timestamp, block.hash)
