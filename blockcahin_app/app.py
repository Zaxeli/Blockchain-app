from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4


app = Flask(__name__)

node_identifier=str(uuid4()).replace('-','')

blkchain = Blockchain()

@app.route('/chain',methods=['GET'])
def blockchain():
    response = jsonify(blkchain.block_chain)
    return response

@app.route('/last',methods=['GET'])
def last_block():
    block = blkchain.block_chain[-1]
    
    response=jsonify(block)
    
    return response

@app.route('/mine',methods=['GET'])
def mine():
    proof=blkchain.calculate_pow(_last_proof=blkchain.block_chain[-1]['proof'])
    blkchain.new_transaction(_from=0,_to=node_identifier,_amt=50)
    response = blkchain.new_block(_proof=proof)
    
    return jsonify(response)

@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    """
    Get a new transaction.
    """
    transaction=request.get_json()
    
    response={'message':'Invalid transaction'}
    
    required=['to','amount', 'from']
    
    if all(values in transaction for values in required):
        print('good request')
        
        blkchain.new_transaction(_from=transaction['from'],_to=transaction['to'],_amt=transaction['amount'])
        response['message']=f"Transaction in queue for Block {blkchain.block_chain[-1]['index']}"
    return jsonify(response)

@app.route('/transactions/all',methods=['GET','POST'])
def all_transactions():
    if request.method=='POST':
        new_transaction()
        
    response={'count':len(blkchain.transactions),
              'transactions':blkchain.transactions}
    
    return jsonify(response)

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    details=request.get_json()
    port=request.environ.get('REMOTE_PORT')
    
    required=['node_list']
    if all(values in details for values in required):

        details['node_list'].append(request.remote_addr+':'+str(port))
        blkchain.register_nodes(details['node_list'])
    
    nodes=list(blkchain.nodes)
    response={'node_list':nodes}
    
    return jsonify(response)
        
        
    
@app.route('/nodes/resolve',methods=['GET'])
def consensus():
    
    change=blkchain.resolve_chain()
    
    #if our chain was not authoritative then it is replaced
    if change:
        message='Blockchain replaced'

    #if our chain was authoritative then it is not replaced
    else:
        message='Blockchain retained'
        
    response={'message':message,'chain':blkchain.block_chain}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
    
