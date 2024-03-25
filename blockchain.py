import datetime
import hashlib
import json
from urllib.parse import urlparse
import requests

# Create a blockchain class


class Blockchain:
    def __init__(self):
        self.__LEADING_ZEROS = '0000'
        self.__chain = []
        self.__transactions = []
        # Creates genesis block
        self.add_block(proof=1, timestamp=str(
            datetime.datetime.now()), previous_hash='0')
        self.__nodes = set()

    def get_chain(self):
        return self.__chain

    def get_nodes(self):
        return self.__nodes

    def add_block(self, proof, timestamp, previous_hash):
        block = {'index': len(self.__chain) + 1,
                 'timestamp': timestamp,
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.__transactions
                 }
        self.__transactions = []
        self.__chain.append(block)
        return block

    def get_last_block(self):
        return self.__chain[-1]

    def proof_of_work(self, previous_proof):
        timestamp = datetime.datetime.now()

        new_proof = 1

        while True:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode() + str(timestamp).encode()).hexdigest()

            if hash_operation[:len(self.__LEADING_ZEROS)] == self.__LEADING_ZEROS:
                return new_proof, str(timestamp)

            new_proof += 1

            # Check if one second has elapsed
            current_time = datetime.datetime.now()
            if current_time - timestamp >= datetime.timedelta(seconds=1):
                timestamp = current_time
                new_proof = 1

    # Hashes block with all properties of block object(index, timestamp, proof, previous_hash etc.)

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        current_block_index = 1

        while current_block_index < len(chain):
            current_block = chain[current_block_index]

            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            timestamp = current_block['timestamp']

            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode() + str(timestamp).encode()).hexdigest()

            if(hash_operation[:len(self.__LEADING_ZEROS)] != self.__LEADING_ZEROS):
                return False

            previous_block = current_block
            current_block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):
        self.__transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        )

        last_block = self.get_last_block()
        return last_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.__nodes.add(parsed_url.netloc)

    def replace_chain(self):
        longest_chain = None
        max_length = len(self.__chain)

        for node in self.__nodes:
            response = requests(f'https://{node}/get_chain')
            if response.status_code == 200:
                chain_length = response.json()['chain_length']
                chain = response.json()['chain']
                if chain_length > max_length and self.is_chain_valid(chain):
                    max_length = chain_length
                    longest_chain = chain
        if longest_chain:
            self.__chain = longest_chain
            return True
        return False
