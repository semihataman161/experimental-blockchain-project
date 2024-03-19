from flask import Flask, jsonify
from blockchain import Blockchain

# Create web app using Flask
blockchain = Blockchain()
app = Flask(__name__)


@app.route('/mine-block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    mined_proof = blockchain.proof_of_work(last_proof)
    last_hash = blockchain.hash(last_block)
    mined_block = blockchain.create_block(mined_proof, last_hash)

    response = {
        'message': 'Congrats! You\'ve just mined a block!',
        'index': mined_block['index'],
        'timestamp': mined_block['timestamp'],
        'proof': mined_block['proof'],
        'previous_hash': mined_block['previous_hash']
    }

    return jsonify(response), 200


@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.get_chain(),
        'chain_length': len(blockchain.get_chain())
    }

    return jsonify(response), 200


@app.route('/is-chain-valid', methods=['GET'])
def is_chain_valid():
    is_valid = blockchain.is_chain_valid(blockchain.get_chain())
    validation_message = ''

    if is_valid:
        validation_message = 'No problem. Blockchain is valid :)'
    else:
        validation_message = 'ERROR: Blockchain is invalid :('

    response = {
        'message': validation_message
    }

    return jsonify(response), 200


# Run the Flask app
app.run(host='0.0.0.0', port=5000)
