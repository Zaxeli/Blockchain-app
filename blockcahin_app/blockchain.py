import hashlib
import json
import requests

class Blockchain:
    def __init__(self):
        
        #transaction pool
        self.transactions=[]
        
        #list of blocks in blockchain, i.e. blockchain
        self.block_chain=[]
        
        #list (set=no repeating elements) of node in network
        self.nodes = set()
        

        #hard coding the genesis block ------
        
        block={'index':len(self.block_chain)+1,
               'transactions':self.transactions,
               'previous_hash':100,
               'proof':1       
            }
        self.transactions=[]
        self.block_chain.append(block)
        
        #soft coding
        """proof=self.calculate_pow(_last_proof=100)
        self.new_block(_proof=proof)
        """
        
    def register_nodes(self,_nodes):
        self.nodes.update(_nodes)
        return self.nodes
    
    def validate_chain(self,_chain):
        #_chain should be a blockchain
        
        for index in range(1,len(_chain)):
            if not (self.verify(_chain[index]['proof'],_chain[index-1]['proof'])):
                return False
        return True
        
    def resolve_chain(self):
        
        for node in self.nodes:
            
            node_chain = requests.get(url=f'http://{node}/chain').json()
            
            #if node's chain is longer than self.chain and it is a valid chain
            if len(node_chain)>len(self.block_chain) :
                print('got longer chain')
                if self.validate_chain(node_chain):
                
                    #update self.chain into node's chain
                    self.block_chain=node_chain
                    
                    #return True if we changed chain
                    return True
            
        #False is no changes were made to self.chain
        return False

    def new_transaction(self,_from,_to,_amt):
        #append a new transaction to transaction[]
        self.transactions.append({'from':_from,
                                  'to':_to,
                                  'amt':_amt})
    
    @staticmethod
    def hash(block):
        json_block=json.dumps(block,sort_keys=True).encode()
        block_hash=hashlib.sha256(json_block).hexdigest()

        return block_hash

    def new_block(self,_proof):

        #build the block
        block={'index':len(self.block_chain)+1,
               'transactions':self.transactions,
               'previous_hash':self.hash(self.block_chain[-1]) or None,
               'proof':_proof       
            }
        

        #check if the given proof is correct
        if(self.verify(_proof,self.block_chain[-1]['proof'])):

            #clear transaction pool and append block is correct
            self.transactions=[]
            self.block_chain.append(block)

            return block
        return False
        #return the block if successfully appended else return False
    
    def calculate_pow(self,_last_proof):
        #finding the proof which along with the last_proof hashes to "000---"
        proof=0

        #incrementally check for correct proof value
        
        while(self.verify(proof,_last_proof)==False):
            proof+=1

        #return the correct proof value    
        return proof
        
    @staticmethod
    def verify(_proof,_last_proof):
        #combine proof and last_proof
        string=f'{_proof}{_last_proof}'.encode()

        #hash the string
        string_hash=hashlib.sha256(string).hexdigest()

        #return the check val as bool
        return string_hash[:4]=='0000'
        
def test():
    blockchain = Blockchain()
    blockchain.register_nodes({1,2,3,4})
    blockchain.register_nodes({2,3,6,4})
    print(blockchain.nodes)
    

test()    
