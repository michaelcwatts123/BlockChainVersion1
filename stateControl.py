#this function is invoked if the transactions are valid
def updateState(transactionBuffer, currState):
    stateCheck = currState.copy()
    for key in transactionBuffer:
        if key in stateCheck.keys():
            stateCheck[key] += transactionBuffer[key]
            # if the user already exist change their current amount of coins
        else:
            stateCheck[key] = transactionBuffer[key]
            #if they do not, add the new coins to the new account
    return stateCheck


def isValidTransaction(transactionBuffer, currState):
    if sum(transactionBuffer.values()) is not 0:
        return False
    # this checks that no coins are created or destoryed 
    for key in transactionBuffer.keys():
        if key in currState.keys():
            accountBalance = currState[key]
        else:
            accountBalance = 0
        if (accountBalance + transactionBuffer[key] < 0):
            return False
       
    return True
