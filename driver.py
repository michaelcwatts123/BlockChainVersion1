import random
from stateControl import *
from chain import *
random.seed(0)
# this will generate the transations that the block chain is meant to record
def makeTransaction(maxValue = 3):
    sign = int(random.getrandbits(1)) * 2 - 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays
    #this gurantees transactions are always equal, no one can create or destroy coins in a transaction
    return {u'Bob':bobPays, u'Alice': alicePays}
def processTransactions(transactionBuffer, blockChain, currState):
    blockSizeLimit = 5
    
    #number of transactions per block an arbitrary amount
    while (len(transactionBuffer) > 0):
        bufferStartSize = len(transactionBuffer)

        transactionList = []
        #holds valid transactions
        while (len(transactionBuffer) > 0) & (len(transactionList) < blockSizeLimit):
            newTransaction = transactionBuffer.pop()
            validTransaction = isValidTransaction(newTransaction, currState)
            #checks to see if transaction is valid holds boolean

            if validTransaction:
                transactionList.append(newTransaction)
                currState = updateState(newTransaction, currState)
                
            else:
                print('Invalid Transaction')
                #ignore transactions that do not pass 
                continue
        newBlock = makeBlock(transactionList, chain)
        #create new block from transaction
        try:
            checkBlockIsValid(newBlock, chain[-1], currState)
            blockChain.append(newBlock)
        except:
            print('Invalid Block rejected')
    


transactionBuffer = [makeTransaction() for i in range(30)]
state = {u'Alice':50,u'Bob':50}
chain = [makeGenesis(state)]
processTransactions(transactionBuffer, chain, state)
print(checkChain(chain))
