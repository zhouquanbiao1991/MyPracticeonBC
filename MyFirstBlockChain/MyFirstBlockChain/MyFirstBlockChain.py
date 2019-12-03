import json
import hashlib
from time import time
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import sys

class MyBlockChain:
    def __init__(self, *args, **kwargs):
        self.current_trans = []
        self.chain = []
        self.nodes = set()

        self.new_block(proof=100, previous_hash=1)

    def register_node(self, address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)

    @staticmethod
    def valid_chain(chain):
        index = 1
        last_block = chain[0]
        block = chain[1]
        while index < len(chain):
            block = chain[index]
            #valid block hash
            if self.hash(last_block) != block['previous_hash']:
                return False
            #valid proof
            if valid_proof(last_block['proof'], block['proof']) is False:
                return False
            index+=1
            last_block = block            
        return True

    def resolve_confict():
        # function: replace the node's chain with longest and valid chain
        # return: <boolean> if chain is replaced return true, else return false

        neighbous = self.nodes

        max_length = len(self.chain)
        max_chain = None
        
        for node in neighbous:
            response = request.get(f"http://{node}/full_chain")
            if response.status_code == 200:
                node_length = response.json()['length']
                node_chain = response.json()['chain']
                if node_length>max_length and self.valid_chain(node_chain) is True:
                    max_length = node_length
                    max_chain = node_chain

        if max_chain is None:
            return False
        else: 
            self.chain = max_chain
            return True 

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp':time(),
            'transactions':self.current_trans,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
            }
        self.current_trans = []
        self.chain.append(block)
        return block

    def new_trans(self,sender, recipient, amount):
        self.current_trans.append(
            {
                'sender':sender,
                'recipient':recipient,
                'amount':amount,
            })
        return self.last_block()['index']+1

    def last_block(self):
        return self.chain[-1]
        
    @staticmethod
    def hash(block):
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        current_proof = 0
        while self.valid_proof(last_proof, current_proof) == False:
            current_proof+=1
        return current_proof

    @staticmethod
    def valid_proof(last_proof, current_proof):
        guess = f'{last_proof}{current_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

app = Flask(__name__)

blockchain = MyBlockChain()

node_identifier = str(uuid4()).replace('-','')

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.chain[-1]
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_trans(sender=0, recipient=node_identifier, amount=1)

    block = blockchain.new_block(proof=proof, previous_hash=blockchain.hash(last_block))

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# post data format:
# {
#    sender: xxxx,
#    recipient: xxxx,
#    amount: xxxx,
# }
@app.route('/transaction/new', methods=['POST'])
def new_transcation():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'missing value', 400
    index = blockchain.new_trans(sender=values['sender'], 
                      recipient=values['recipient'], 
                      amount=values['amount'])
    response = f'we will add a new trancation index:{index}'
    return jsonify(response), 201

@app.route('/full_chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response),200

@app.route('/register_node', methods=['POST'])
def register_node():
    value = request.get_json()
    nodes = value['nodes']

    if nodes is None:
        return 'register node list is null', 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message' : 'register some new node',
        'total_nodes' : list(blockchain.nodes),
    }
    return response, 200

@app.route('/consensus', methods=['GET'])
def consensus():
    if blockchain.resolve_confict() is True:
        return 'chain is replaced', 200
    else:
        return 'our chain is authoried', 200

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=sys.argv[1])
    app.run(host='0.0.0.0', port=5002)
