import datetime
import hashlib
import json

# Create a blockchain class


class Blockchain:
    def __init__(self):
        self._chain = []
        self._LEADING_ZEROS = '0000'
        # Creates genesis block
        self.create_block(proof=1, previous_hash='0')

    def get_chain(self):
        return self._chain

    def create_block(self, proof, previous_hash):
        block = {'index': len(self._chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }
        self._chain.append(block)
        return block

    def get_last_block(self):
        return self._chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if(hash_operation[:4] == self._LEADING_ZEROS):
                check_proof = True
            else:
                new_proof += 1

        return new_proof

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
            hash_operation = hashlib.sha256(
                str(current_proof**2 - previous_proof**2).encode()).hexdigest()

            if(hash_operation[:4] != self._LEADING_ZEROS):
                return False

            previous_block = current_block
            current_block_index += 1

        return True
