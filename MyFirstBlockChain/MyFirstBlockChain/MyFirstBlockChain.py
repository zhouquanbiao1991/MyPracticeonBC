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

    def new_trans():
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

app_flask = app(__name__)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
