from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4


# Create an api using Flask
app = Flask(__name__)

# Creating an adress for node
node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine-block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    mined_proof, timestamp = blockchain.proof_of_work(last_proof)
    last_hash = blockchain.hash(last_block)
    blockchain.add_transaction(
        sender=node_address, receiver='Semih', amount=100)
    mined_block = blockchain.add_block(mined_proof, timestamp, last_hash)

    response = {
        'message': 'Congrats! You\'ve just mined a block!',
        'index': mined_block['index'],
        'timestamp': mined_block['timestamp'],
        'proof': mined_block['proof'],
        'previous_hash': mined_block['previous_hash'],
        'transactions':  mined_block['transactions']
    }

    return jsonify(response), 200


@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.get_chain(),
        'chain_length': len(blockchain.get_chain())
    }

    return jsonify(response), 200


@app.route('/replace-chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    response = None

    if is_chain_replaced:
        response = {
            'message': 'Chain replaced by the longest chain.',
            'new_chain': blockchain.get_chain()
        }
    else:
        response = {
            'message': 'Current chain is already the longest one.',
            'actual_chain': blockchain.get_chain()
        }

    return jsonify(response), 200


@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount'])

    response = {'message': f'This transsaction will be added to block {index}.'}
    return jsonify(response), 201


@app.route('/connect-node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 400

    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are connected.',
                'connected_nodes': list(blockchain.get_nodes())
                }
    return jsonify(response), 201


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
app.run(host='0.0.0.0', port=5001)
