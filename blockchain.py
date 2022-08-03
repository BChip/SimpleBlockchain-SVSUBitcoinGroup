import hashlib as hasher
import datetime as date

# https://guggero.github.io/blockchain-demo/#!/hash

HASH_TARGET = "0000"


class Block:

    def __init__(self, index, timestamp, data, hash="0", previous_hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previous_hash
        self.nonce = 0
        self.hash = hash

    def hashBlock(self):
        data = (str(self.index) + str(self.data) + str(self.timestamp) +
                str(self.previousHash) + str(self.nonce)).encode('utf-8')
        return hasher.sha256(data).hexdigest()


class Chain:

    def __init__(self):
        self.blockchain = []
        self.addBlock("Genesis Block")

    def addBlock(self, data):
        if(len(self.blockchain) == 0):
            previous_hash = "0"*64
            newBlock = Block(len(self.blockchain),
                             date.datetime.now(), data, previous_hash=previous_hash)
        else:
            previousBlock = self.blockchain[-1]
            newBlock = Block(len(self.blockchain),
                             date.datetime.now(), data, previous_hash=previousBlock.hash)
        newBlock.hash = self.proofOfWork(newBlock)
        self.blockchain.append(newBlock)

    def getChain(self):
        return self.blockchain

    def proofOfWork(self, block):
        while block.hash[:len(HASH_TARGET)] != HASH_TARGET:
            block.nonce += 1
            block.hash = block.hashBlock()
        return block.hash

    def isValid(self):
        for i in range(1, len(self.blockchain)):
            currentBlock = self.blockchain[i]
            previousBlock = self.blockchain[i-1]
            if currentBlock.hash != currentBlock.hashBlock():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True


def main():
    blockchain = Chain()
    blockchain.addBlock("New Block 1")
    blockchain.addBlock("New Block 2")
    blockchain.addBlock("New Block 3")
    for block in blockchain.getChain():
        print(block.index, block.timestamp, block.previousHash,
              block.hash, block.data, block.nonce)
    print(blockchain.isValid())


main()
