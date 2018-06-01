from hash import *
from stateControl import *
def makeGenesis(state):
    genesisBlockTransactions = [state]
    #The only transactions in the block is the intial state of the coin aka who has some
    genesisBlockContents = {u'blockNumber':0,u'parentHash':None, u'transactionCount':1, u'genesisBlockTransactions':genesisBlockTransactions}
    #Holds contents of block 
    genesisHash = hashMe(genesisBlockContents)
    genesisBlock = {u'hash':genesisHash, u'contents': genesisBlockContents}
    #This wil be the actual block that holds the hash and data
    genesisBlockString = json.dumps(genesisBlock, sort_keys=True)
    return genesisBlock

def makeBlock(transaction, chain):
    parentBlock = chain[-1]
    #finds last block on chain
    parentHash = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    blockContent = {u'blockNumber': blockNumber, u'parentHash': parentHash, u'transactionCount':len(transaction), u'transactions': transaction}
    blockHash = hashMe(blockContent)
    block = {u'hash': blockHash, u'contents': blockContent}
    blockString = json.dumps(block, sort_keys=True)
    return block
def hashCheck(block):
    expectedHash = hashMe(block[u'contents'])
    #generate the hash we expect
    if block[u'hash'] != expectedHash:
        raise Exception('Hash does not match for block %s'%block[u'contents'][u'blockNumber'])
    return
def checkBlockIsValid(block, parent, state):
    #check each transaction is valid according to the current state
    #check each block has a valid hash
    #check current block number is one higher than parent block
    #check current block accurately refers to parent hash

    parentNumber = parent[u'contents'][u'blockNumber']
    parentHash = parent[u'hash']
    blockNumber = block[u'contents'][u'blockNumber']
    transactions = block[u'contents'][u'transactions']
    for i in transactions:
        if isValidTransaction(i, state):
            state = updateState(i, state)
        else:
            raise Exception('Invalid transaction at Block %s: %s'%(blockNumber, i))
    hashCheck(block)

    if blockNumber != (parentNumber+1):
        raise Exception('Block is not the next in sequence')
    if block[u'contents'][u'parentHash'] != parentHash:
        raise Exception('Parent hash not accurate at block %s'%blockNumber)
    return state

def checkChain(chain):
    # Work through the chain from the genesis block (which gets special treatment), 
    #  checking that all transactions are internally valid,
    #    that the transactions do not cause an overdraft,
    #    and that the blocks are linked by their hashes.
    # This returns the state as a dictionary of accounts and balances,
    #   or returns False if an error was detected

    
    ## Data input processing: Make sure that our chain is a list of dicts
 
    if type(chain)==str:
        try:
            chain = json.loads(chain)
            assert( type(chain)==list)
        except:  # This is a catch-all, admittedly crude
            return False
    elif type(chain)!=list:
        return False
  
    state = {}
    # Check the genesis block
    # Each of the transactions are valid updates to the system state
    # Block hash is valid for the block contents

    for transactions in chain[0]['contents']['genesisBlockTransactions']:
        state = updateState(transactions,state)
    hashCheck(chain[0])
    parent = chain[0]
    
    ## Checking subsequent blocks: These additionally need to check
    #    - the reference to the parent block's hash
    #    - the validity of the block number
    for block in chain[1:]:
        state = checkBlockIsValid(block,parent,state)
        parent = block
        
    return state
