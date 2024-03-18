import hashlib
import datetime

from dataclasses import dataclass

HASH_TARGET: str = "0000"


@dataclass(frozen=True)
class Block:

    index: int
    timestamp: str
    data: str
    previous_hash: str
    nonce: int = 0
    hash: str = "0"

    @property
    def hash_data(self) -> bytes:
        return f"{str(self.index)}{str(self.data)}{str(self.timestamp)}{str(self.previous_hash)}{str(self.nonce)}".encode(
            "utf-8"
        )

    def __str__(self) -> str:
        return f"{self.data}\nindex={self.index}\ntime={self.timestamp}\nprevious_hash={self.previous_hash}\nhash={self.hash}\nnonce={self.nonce}\n"


class Chain:

    __blockchain: list[Block] = []

    @property
    def blockchain(self) -> list:
        """blockchain getter

        Returns:
            list: copy of the blockchain
        """
        return self.__blockchain[:]

    def __init__(self) -> None:
        self.__blockchain.append(
            self.proof_of_work(
                Block(0, datetime.datetime.now(), "Genesis Block", "0" * 64)
            )
        )

    def proof_of_work(self, block: Block) -> Block:
        """hash block data until hash target is met

        Args:
            block (Block): new Block

        Returns:
            Block: new block with a new nonce that meets hash target requirements
        """
        new_hash: str = ""
        _nonce: int = block.nonce

        while new_hash[: len(HASH_TARGET)] != HASH_TARGET:
            new_hash = hashlib.sha256(
                f"{str(block.index)}{str(block.data)}{str(block.timestamp)}{str(block.previous_hash)}{str(_nonce)}".encode(
                    "utf-8"
                )
            ).hexdigest()
            _nonce += 1

        return Block(
            block.index,
            block.timestamp,
            block.data,
            block.previous_hash,
            nonce=_nonce - 1,
            hash=new_hash,
        )

    def add_block(self, data: str) -> None:
        """adds a new block to the chain with the given data attached

        Args:
            data (str): data to attach to the new block
        """
        previous_block: Block = self.__blockchain[-1]

        new_block = self.proof_of_work(
            Block(
                len(self.__blockchain),
                datetime.datetime.now(),
                data,
                previous_hash=previous_block.hash,
            )
        )

        self.__blockchain.append(new_block)

    def check_validity(self) -> bool:
        """test that each blocks hash matches the value in the classes hash variable

        Returns:
            bool: pass/fail
        """
        current_block: Block = self.__blockchain[0]
        previous_block: Block = None

        # check that the first block's hash is correct before checking the rest of the chain
        if current_block.hash != hashlib.sha256(current_block.hash_data).hexdigest():
            return False

        for i in range(1, len(self.__blockchain)):
            current_block = self.__blockchain[i]
            previous_block = self.__blockchain[i - 1]

            if (
                current_block.hash
                != hashlib.sha256(current_block.hash_data).hexdigest()
                or current_block.previous_hash != previous_block.hash
            ):
                return False

        return True


if __name__ == "__main__":
    new_chain = Chain()

    for i in range(10):
        new_chain.add_block(f"Block {i}")

    for _block in new_chain.blockchain:
        print(_block)

    print("Checking validity...")
    print(f"Validity = {new_chain.check_validity()}")
