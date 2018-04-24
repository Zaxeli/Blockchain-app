╟==============Info==============╟

This is a simple blockchain app. It has an api that can be used to interact with it.
The details regarding api are given further on.

╟==========Instructions==========╟

Just run the app.py file using python3.

╟========API instructions========╟

make requests at
https://localhost:5001/
using Postman or curl

/chain [GET]
	returns the entire blockchain

/last  [GET]
	return only the last block

/mine  [GET]
	used to mine a new block
	block reward is given to the miner
	returns:
		bool: False if the block was not mined
		block mined if successfully mined
/transactions/new [POST]
	make a new transaction
	
	required fields:
		to: the sender of the currency being transferred.
		from: the reciever of the transaction
		amount: the value being transacted

/transactions/all [GET,POST]
	view all the transactions
	
	(optional)
	also make a new transaction along with viewing

/nodes/register [POST]
	used to register new nodes into our list of nodes (i.e. the nodes we are aware of)

	required fields:
		node_list:it should contain a list of nodes
				e.g. 170.60.162.204:5001
	
	returns a node_list containing a list of our known nodes.

/nodes/resolve [GET]
	used to build consensus among nodes
	each node's blockchain is checked to find most valid blockchain and consequently swap to using it in case there is a more valid blockchain than ours found,
	
