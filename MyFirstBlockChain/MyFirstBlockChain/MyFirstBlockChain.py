import json
import hashlib
from time import time

class MyBlockChain:
    def __init__(self, *args, **kwargs):
        self.current_trans = []
        self.chain = []

        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp':time(),
            'transation':current_trans,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
            }
        self.current_trans = []
        self.chain.append(block)
        return block

    def new_trans(sender, recipient, amount):
        self.current_trans.append(
            {
                'sender':sender,
                'recipient':recipient,
                'amount':amount,
            })
        return last_block('index')+1

    def last_block():
        return self.chain[-1]
        
    def hash(block):
        block_string = json.dump(block,sort_key=True).encode
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(last_proof):
        current_proof = 0
        while valid_proof(last_proof, current_proof) == False:
            current_proof+=1
        return current_proof

    @staticmethod
    def valid_proof(last_proof, current_proof):
        guess = f'{last_proof}{current_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

app = Falsk(__name__)

blockchain = MyBlockChain()

node_identifier = str(uuid4()).replace('-','')

@app.route('/mine', method=['GET'])
def mine():
    last_block = blockchain.chain[-1]
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    new_trans(sender=0, recipient=node_identifier, amount=1)

    block = new_block(proof=proof, previous_hash=blockchain.hash(last_block))

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
@app.route('/transcation/new', method=['POST'])
def new_transcation():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'missing value', 400
    index = new_trans(sender=values['sender'], 
                      recipient=values['recipient'], 
                      amount=values['amount'])
    response = 'we will add a new trancation index:' + index
    return jsonify(response), 201

@app.route('/full_chain', method=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response),200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
